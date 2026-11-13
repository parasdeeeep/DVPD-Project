from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

path = Path('Part_E_Product_EDA_Report.docx')
output = Path('Part_E_Product_EDA_Report_formatted.docx')
doc = Document(path)
black = RGBColor(0, 0, 0)

styles = doc.styles
styles['Normal'].font.name = 'Calibri'
styles['Normal'].font.size = Pt(12)
styles['Normal'].font.color.rgb = black

for name, size in [('Heading 1', 16), ('Heading 2', 14), ('Heading 3', 13)]:
    style = styles[name]
    style.font.name = 'Calibri'
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = black

for index, paragraph in enumerate(doc.paragraphs):
    text = paragraph.text.strip()
    if not text:
        continue

    # Convert all headings into ordinary paragraphs so Word does not show
    # expand/collapse triangles beside them.
    if paragraph.style.name.startswith('Heading') or index == 0:
        size = 18 if index == 0 else 16
        paragraph.style = styles['Normal']
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if index == 0 else WD_ALIGN_PARAGRAPH.LEFT
        for run in paragraph.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(size)
            run.font.bold = True
            run.font.color.rgb = black
        paragraph.paragraph_format.space_before = Pt(10)
        paragraph.paragraph_format.space_after = Pt(5)
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in paragraph.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.font.color.rgb = black

try:
    doc.save(path)
    print(f'Formatted {path} in place')
except PermissionError:
    doc.save(output)
    print(f'Original is locked; saved formatted copy as {output}')
