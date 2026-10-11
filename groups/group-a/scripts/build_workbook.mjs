import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const report=path.resolve(root,'../../report');
const data=JSON.parse(await fs.readFile(path.join(root,'evidence/workbook_source.json'),'utf8'));
const wb=Workbook.create();
for(const name of Object.keys(data))wb.worksheets.add(name);
for(const [name,matrix] of Object.entries(data)){
 const sh=wb.worksheets.getItem(name);sh.showGridLines=false;
 const rows=matrix.length,cols=Math.max(...matrix.map(r=>r.length));
 sh.getRangeByIndexes(0,0,rows,cols).values=matrix;
 const body=sh.getRangeByIndexes(0,0,rows,cols);
 body.format.font={name:'Calibri',size:11};body.format.wrapText=true;
 body.format.columnWidth=22;body.format.rowHeight=48;
 sh.getRangeByIndexes(0,0,1,cols).format={fill:'#17324D',font:{name:'Calibri',bold:true,color:'#FFFFFF',size:11},rowHeight:32};
 sh.freezePanes.freezeRows(1);
 if(name!=='Summary')sh.tables.add(sh.getRangeByIndexes(0,0,rows,cols),true,name+'Table');
 if(name==='Decisions'){sh.getRange('D:D').format.columnWidth=65;sh.getRange('H:H').format.columnWidth=95;sh.getRange('L:L').format.columnWidth=65;body.format.rowHeight=80;}
 if(name==='Included'){sh.getRange('C:G').format.columnWidth=60;body.format.rowHeight=95;}
 if(name==='Downloads'){sh.getRange('C:C').format.columnWidth=70;sh.getRange('E:F').format.columnWidth=65;body.format.rowHeight=65;}
 if(name==='Searches'){sh.getRange('G:H').format.columnWidth=80;body.format.rowHeight=120;}
 if(name==='Received'){
  sh.getRange('A:B').format.columnWidth=16;sh.getRange('C:C').format.columnWidth=65;
  sh.getRange('D:D').format.columnWidth=35;sh.getRange('E:E').format.columnWidth=10;
  sh.getRange('F:F').format.columnWidth=75;body.format.rowHeight=70;
 }
 if(name==='Quality'){
  sh.getRange('B:K').format.columnWidth=7;sh.getRange('N:N').format.columnWidth=65;
  sh.getRange(`L2:L${rows}`).formulas=Array.from({length:rows-1},(_,i)=>[`=SUM(B${i+2}:K${i+2})`]);
  sh.getRange(`M2:M${rows}`).formulas=Array.from({length:rows-1},(_,i)=>[`=IF(L${i+2}>=8,"high",IF(L${i+2}>=6,"moderate","low"))`]);
 }
 if(name==='Summary'){
  sh.getRange('A:A').format.columnWidth=36;sh.getRange('B:B').format.columnWidth=50;
  sh.getRange('B3:B10').setNumberFormat('0');
  sh.getRange('B11').formulas=[['=B3-B4+B5-B6-B7-B8']];
  sh.getRange('B12').formulas=[['=B7-B9-B10']];
  sh.getRange('A11:B12').format.fill='#DDEFE7';
 }
}
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:'Summary',range:'A1:B12',maxChars:3000,tableMaxRows:12,tableMaxCols:2})).ndjson);
const preview=await wb.render({sheetName:'Summary',autoCrop:'all',scale:1,format:'png'});
await fs.writeFile(path.join(report,'workbook-preview.png'),new Uint8Array(await preview.arrayBuffer()));
for(const [sheetName,range] of [['Quality','A17:N22'],['Received','A1:E7']]){
 console.log((await wb.inspect({kind:'region',sheetId:sheetName,range,maxChars:7000,tableMaxRows:7,tableMaxCols:14})).ndjson);
 const picture=await wb.render({sheetName,range,scale:1,format:'png'});
 await fs.writeFile(path.join(report,sheetName.toLowerCase()+'-preview.png'),new Uint8Array(await picture.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(report,'query_review_workbook.xlsx'));
