# Build and status

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in this directory. Output `main.pdf` is copied to the deliverable `report.pdf` after validation. The document uses 12-point Times-compatible text with numerical IEEEtran citations. XeLaTeX requires a Times New Roman installation; pdfLaTeX uses the bundled TeX Times-compatible fonts.

`IEEEtran.bst` is Michael Shell's unmodified version1.14, LPPL1.3, retrieved from https://raw.githubusercontent.com/DanySK/Template-LaTeX-IEEE-Computer-Society-Magazines/master/IEEEtran.bst on11 October2026. Its license and notices are retained. Upstream: https://ctan.org/pkg/ieeetran . The style is code, not a research reference.

The PDF is the intermediate search/evidence deliverable; the final20–30-page CEP report remains pending coverage, access and detailed extraction. Do not label this PDF the final SLR.

Six-paper update: rebuild recorded assessments with `python groups/group-a/scripts/build_evidence.py`, then `python groups/group-a/scripts/build_uploaded_review.py` (uses committed private-source receipt hashes), then `python groups/group-a/scripts/build_report.py`; validate with `python groups/group-a/scripts/validate_evidence.py`. Optional `--source-dir <private-conversions-directory>` on the uploaded-review builder verifies/refreshes source hashes. The licensed conversions are not required for a register rebuild and must never be committed. Regenerate the workbook with the Codex primary runtime Node and the existing artifact-tool builder before compiling/checking the PDF.
