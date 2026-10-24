"""Build the sprint report from one source, "Apart Research/report.md".

  python scripts/build_report.py [--template PATH] [--no-pdf] [--no-tex]

Writes into "Apart Research/":
  report.docx   the official Apart template format: its fonts (Old Standard TT, embedded), its title
                block and sprint footnote, its section headings
  report.pdf    LibreOffice export of report.docx: the file to submit
  main3.tex     the same text as LaTeX (pdflatex + bibtex; apalike style, references.bib)

Needs pandoc (3.x) and, for the PDF, LibreOffice. The template is the official sprint template
(Apart_Research_hackathon_submission_template.docx in the same folder); only its styles, page
setup and fonts are used, never its guidance text.
"""

from __future__ import annotations

import argparse
import copy
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "Apart Research"
SOURCE = FOLDER / "report.md"
TEMPLATE = FOLDER / "Apart_Research_hackathon_submission_template.docx"
FONT = "Old Standard TT"
BLACK = RGBColor(0, 0, 0)


def split_front_matter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise SystemExit("report.md must start with a YAML front-matter block")
    return yaml.safe_load(match.group(1)), text[match.end() :]


# ---------------------------------------------------------------- reference document (styles)


def _set_font(style, size: float | None = None, bold: bool | None = None, italic: bool | None = None) -> None:
    font = style.font
    font.name = FONT
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), FONT)
    if size is not None:
        font.size = Pt(size)
    if bold is not None:
        font.bold = bold
    if italic is not None:
        font.italic = italic
    font.color.rgb = BLACK


def _normal(doc):
    """The template (a Google Docs export) names its Normal style "normal"; look it up by id."""
    return next(st for st in doc.styles if st.style_id == "Normal")


def _style(doc, name: str, kind: int = 1):
    try:
        return doc.styles[name]
    except KeyError:
        style = doc.styles.add_style(name, kind)
        if kind == 1:
            style.base_style = _normal(doc)
        return style


def _rule(paragraph_format_element, edges: tuple[str, ...], size: int = 8) -> None:
    """Add a black horizontal rule above and/or below a paragraph (style or paragraph pPr)."""
    pbdr = OxmlElement("w:pBdr")
    for edge in edges:
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "8")
        el.set(qn("w:color"), "000000")
        pbdr.append(el)
    paragraph_format_element.append(pbdr)


def make_reference(template: Path, out: Path) -> None:
    """The template's page setup and theme, with pandoc's style names mapped to the template look:
    body text 11 pt Old Standard TT at 1.15 line spacing, numbered section headings 14 pt bold,
    subsections 13 pt bold, title 20 pt bold between two rules."""
    doc = Document(str(template))
    body = doc.element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)

    normal = _normal(doc)
    _set_font(normal, 11)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(0)

    for name in ("Body Text", "First Paragraph", "Compact"):
        st = _style(doc, name)
        _set_font(st, 11)
        st.paragraph_format.space_before = Pt(0)
        st.paragraph_format.space_after = Pt(4)
        st.paragraph_format.line_spacing = 1.15
    doc.styles["Compact"].paragraph_format.space_after = Pt(2)

    # Heading 1 (sections 1-6, Code and Data, References, Appendix) gets one blank line (about 13 pt)
    # more space before it than a subsection, so the sections stand apart.
    for name, size, before in (("Heading 1", 14, 24), ("Heading 2", 13, 6), ("Heading 3", 11, 6)):
        st = _style(doc, name)
        _set_font(st, size, bold=True, italic=False)
        pf = st.paragraph_format
        pf.space_before = Pt(before)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.15
        pf.keep_with_next = True

    title = _style(doc, "Title")
    _set_font(title, 20, bold=True)
    title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(16)
    title.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    _rule(title.element.get_or_add_pPr(), ("top", "bottom"))

    author = _style(doc, "Author Block")
    _set_font(author, 11)
    author.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author.paragraph_format.space_after = Pt(10)
    author.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    head = _style(doc, "Abstract Heading")
    _set_font(head, 14, bold=True)
    head.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    head.paragraph_format.space_before = Pt(12)
    head.paragraph_format.space_after = Pt(8)

    abstract = _style(doc, "Abstract Body")
    _set_font(abstract, 11)
    pf = abstract.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.left_indent = Pt(27)  # 540 twips, as in the template
    pf.right_indent = Pt(27)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    pf.space_after = Pt(12)

    for name in ("Table Caption", "Image Caption", "Caption"):
        st = _style(doc, name)
        _set_font(st, 9.5, italic=False)
        st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        st.paragraph_format.space_before = Pt(4)
        st.paragraph_format.space_after = Pt(8)
    doc.styles["Table Caption"].paragraph_format.keep_with_next = True

    figure = _style(doc, "Captioned Figure")
    figure.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    figure.paragraph_format.keep_with_next = True

    bib = _style(doc, "Bibliography")
    _set_font(bib, 10)
    bib.paragraph_format.left_indent = Pt(18)
    bib.paragraph_format.first_line_indent = Pt(-18)
    bib.paragraph_format.space_after = Pt(4)
    bib.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    code = _style(doc, "Source Code")
    code.font.name = "Courier New"
    code.font.size = Pt(7.5)
    code.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    code.paragraph_format.space_after = Pt(6)
    code.paragraph_format.keep_together = True  # the agent prompt stays on one page

    verbatim = _style(doc, "Verbatim Char", kind=2)
    verbatim.font.name = "Courier New"
    verbatim.font.size = Pt(9)

    for name in ("Footnote Text",):
        st = _style(doc, name)
        _set_font(st, 9)
        st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    link = _style(doc, "Hyperlink", kind=2)
    link.font.color.rgb = RGBColor(0x11, 0x55, 0xCC)
    link.font.underline = True
    doc.save(str(out))


# ---------------------------------------------------------------- docx


def _lines(value: str | list[str]) -> list[str]:
    """A front-matter field that may be one line or a list of lines (e.g. a two-line affiliation)."""
    return [value] if isinstance(value, str) else list(value)


def front_markdown(meta: dict) -> str:
    affiliation = "\\\n".join(_lines(meta["affiliation"]))  # markdown hard line breaks
    title = "\\\n".join(_lines(meta["title"]))
    return f"""::: {{custom-style="Title"}}
{title}[^sprint]
:::

::: {{custom-style="Author Block"}}
**{meta["author"]}**\\
{affiliation}\\
{meta["email"]}
:::

::: {{custom-style="Author Block"}}
**With**\\
Apart Research
:::

::: {{custom-style="Abstract Heading"}}
Abstract
:::

::: {{custom-style="Abstract Body"}}
{meta["abstract"].strip()}
:::

[^sprint]: Research conducted at the [AI Collusion Research Sprint]({meta["sprint_url"]}), October 2026

"""


def _cell_borders(cell, top: int = 0, bottom: int = 0) -> None:
    tcpr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge, size in (("top", top), ("bottom", bottom), ("left", 0), ("right", 0)):
        el = OxmlElement(f"w:{edge}")
        if size:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(size))
            el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)
    for old in tcpr.findall(qn("w:tcBorders")):
        tcpr.remove(old)
    tcpr.append(borders)


def _cell_margins(table, twips: int = 60) -> None:
    tblpr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(twips if edge in ("left", "right") else 0))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    for old in tblpr.findall(qn("w:tblCellMar")):
        tblpr.remove(old)
    tblpr.append(mar)


def style_tables(doc) -> None:
    """Booktabs look: a rule above and below the table and under the header, 8 pt text. Each table
    stays on one page."""
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        _cell_margins(table)
        follower = table._tbl.getnext()
        if follower is not None and follower.tag == qn("w:p"):
            ppr = follower.get_or_add_pPr()
            spacing = ppr.find(qn("w:spacing"))
            if spacing is None:
                spacing = OxmlElement("w:spacing")
                ppr.append(spacing)
            spacing.set(qn("w:before"), "160")  # 8 pt between a table and the text after it
        rows = table.rows
        for r, row in enumerate(rows):
            trpr = row._tr.get_or_add_trPr()
            cant = OxmlElement("w:cantSplit")
            trpr.append(cant)
            if r == 0:
                header = OxmlElement("w:tblHeader")
                trpr.append(header)
            seen = set()
            for cell in row.cells:
                if id(cell._tc) in seen:  # a merged cell appears once per grid column it spans
                    continue
                seen.add(id(cell._tc))
                _cell_borders(
                    cell,
                    top=8 if r == 0 else 0,
                    bottom=8 if r == len(rows) - 1 else (4 if r == 0 else 0),
                )
                for par in cell.paragraphs:
                    par.paragraph_format.space_after = Pt(1)
                    par.paragraph_format.space_before = Pt(1)
                    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    par.paragraph_format.keep_with_next = r < len(rows) - 1
                    for run in par.runs:
                        run.font.size = Pt(8)
                        if r == 0:
                            run.font.bold = True


def embed_fonts(docx_path: Path, template: Path) -> None:
    """Copy the template's embedded Old Standard TT files into the output, so the document shows
    the template font on machines without it (Word: File > Options > Save > Embed fonts)."""
    with zipfile.ZipFile(template) as t:
        fonts = {n: t.read(n) for n in t.namelist() if n.startswith("word/fonts/")}
        rels = t.read("word/_rels/fontTable.xml.rels")
        ttable = t.read("word/fontTable.xml").decode()
    entry = re.search(r'<w:font w:name="Old Standard TT">.*?</w:font>', ttable, re.S)
    if not fonts or entry is None:
        return
    tmp = docx_path.with_suffix(".tmp")
    replaced = set(fonts) | {"word/_rels/fontTable.xml.rels"}
    with zipfile.ZipFile(docx_path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            if item.filename in replaced:
                continue
            data = src.read(item.filename)
            if item.filename == "word/fontTable.xml":
                text = data.decode()
                text = re.sub(r'<w:font w:name="Old Standard TT">.*?</w:font>', "", text, flags=re.S)
                if 'xmlns:r="' not in text.split(">", 2)[1]:
                    text = text.replace(
                        "<w:fonts ",
                        '<w:fonts xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
                        1,
                    )
                data = text.replace("</w:fonts>", entry.group(0) + "</w:fonts>").encode()
            elif item.filename == "[Content_Types].xml":
                text = data.decode()
                if 'Extension="ttf"' not in text:
                    text = text.replace(
                        "<Default ", '<Default Extension="ttf" ContentType="application/x-font-ttf"/><Default ', 1
                    )
                data = text.encode()
            elif item.filename == "word/settings.xml":
                text = data.decode()
                if "embedTrueTypeFonts" not in text:
                    text = re.sub(r"(<w:settings[^>]*>)", r"\1<w:embedTrueTypeFonts/>", text, count=1)
                data = text.encode()
            dst.writestr(item, data)
        for name, data in fonts.items():
            dst.writestr(name, data)
        dst.writestr("word/_rels/fontTable.xml.rels", rels)
    tmp.replace(docx_path)


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# Child order required by the OOXML schema (ECMA-376) for the elements this script edits.
ORDER = {
    "pPr": "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr "
    "shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN "
    "bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc "
    "textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange",
    "tblPr": "tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc "
    "tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription tblPrChange",
    "tcPr": "cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign "
    "hideMark headers cellIns cellDel cellMerge tcPrChange",
    "tcBorders": "top start left bottom end right insideH insideV tl2br tr2bl",
    "settings": "writeProtection view zoom removePersonalInformation removeDateAndTime "
    "doNotDisplayPageBoundaries displayBackgroundShape printPostScriptOverText printFractionalCharacterWidth "
    "printFormsData embedTrueTypeFonts embedSystemFonts saveSubsetFonts saveFormsData mirrorMargins "
    "alignBordersAndEdges bordersDoNotSurroundHeader bordersDoNotSurroundFooter gutterAtTop hideSpellingErrors "
    "hideGrammaticalErrors activeWritingStyle proofState formsDesign attachedTemplate linkStyles "
    "stylePaneFormatFilter stylePaneSortMethod documentType mailMerge revisionView trackRevisions "
    "doNotTrackMoves doNotTrackFormatting documentProtection autoFormatOverride styleLockTheme styleLockQFSet "
    "defaultTabStop autoHyphenation consecutiveHyphenLimit hyphenationZone doNotHyphenateCaps showEnvelope "
    "summaryLength clickAndTypeStyle defaultTableStyle evenAndOddHeaders bookFoldRevPrinting bookFoldPrinting "
    "bookFoldPrintingSheets drawingGridHorizontalSpacing drawingGridVerticalSpacing "
    "displayHorizontalDrawingGridEvery displayVerticalDrawingGridEvery doNotUseMarginsForDrawingGridOrigin "
    "drawingGridHorizontalOrigin drawingGridVerticalOrigin doNotShadeFormData noPunctuationKerning "
    "characterSpacingControl printTwoOnOne strictFirstAndLastChars noLineBreaksAfter noLineBreaksBefore "
    "savePreviewPicture doNotValidateAgainstSchema saveInvalidXml ignoreMixedContent alwaysShowPlaceholderText "
    "doNotDemarcateInvalidXml saveXmlDataOnly useXSLTWhenSaving saveThroughXslt showXMLTags "
    "alwaysMergeEmptyNamespace updateFields hdrShapeDefaults footnotePr endnotePr compat docVars rsids mathPr "
    "attachedSchema themeFontLang clrSchemeMapping doNotIncludeSubdocsInStats doNotAutoCompressPictures "
    "forceUpgrade captions readModeInkLockDown smartTagType schemaLibrary shapeDefaults doNotEmbedSmartTags "
    "decimalSymbol listSeparator",
}


def _local(tag: str) -> str:
    """Element name without its namespace (settings mixes w: and m: elements, e.g. m:mathPr)."""
    return tag.rsplit("}", 1)[-1]


def _reorder(root) -> None:
    for name, order in ORDER.items():
        rank = {tag: i for i, tag in enumerate(order.split())}
        for el in root.iter(W + name):
            kids = list(el)
            known = [k for k in kids if isinstance(k.tag, str) and _local(k.tag) in rank]
            tail = [k for k in kids if k not in known]
            ordered = sorted(known, key=lambda k: rank[_local(k.tag)]) + tail
            for k in kids:
                el.remove(k)
            for k in ordered:
                el.append(k)


def fix_schema(docx_path: Path) -> None:
    """Put edited elements into schema order and repair two values that strict validators reject."""
    from lxml import etree

    tmp = docx_path.with_suffix(".fix")
    with zipfile.ZipFile(docx_path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename in ("word/document.xml", "word/styles.xml", "word/settings.xml", "word/numbering.xml"):
                root = etree.fromstring(data)
                _reorder(root)
                for nsid in root.iter(W + "nsid"):  # must be 8 hex digits
                    nsid.set(W + "val", nsid.get(W + "val").rjust(8, "0")[-8:])
                for mar in root.iter(W + "pgMar"):
                    if mar.get(W + "gutter") is None:
                        mar.set(W + "gutter", "0")
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            dst.writestr(item, data)
    tmp.replace(docx_path)


# Display equations in report.md are written as  $$ <LaTeX> \qquad (n)$$
EQUATION = re.compile(r"\$\$([^$]+?)\\qquad \((\d+)\)\$\$")  # [^$]: never spans two equations
EQUATION_TEX = r"""\documentclass[11pt]{article}
\usepackage[paperwidth=6.5in,paperheight=4in,margin=0in]{geometry}
\usepackage{amsmath}
\pagestyle{empty}
\setlength{\abovedisplayskip}{0pt}
\setlength{\belowdisplayskip}{0pt}
\begin{document}
\noindent\begin{minipage}{\textwidth}
\vspace*{4pt}
\begin{equation*}
%s \tag{%s}
\end{equation*}
\vspace*{4pt}
\end{minipage}
\end{document}
"""


def render_equation(tex: str, number: str, out: Path) -> None:
    """Typeset one display equation with LaTeX into a PNG as wide as the text block (6.5 in), so
    the equation is centred and its number sits at the right margin in Word, LibreOffice and
    Google Docs alike."""
    from PIL import Image, ImageOps

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "eq.tex"
        src.write_text(EQUATION_TEX % (tex.strip(), number), encoding="utf-8")
        res = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "eq.tex"], cwd=tmp, capture_output=True, text=True
        )
        if res.returncode != 0:
            sys.exit(f"LaTeX failed on equation ({number}):\n{res.stdout[-1500:]}")
        subprocess.run(["pdftoppm", "-r", "600", "-png", "-singlefile", "eq.pdf", "eq"], cwd=tmp, check=True)
        image = Image.open(Path(tmp) / "eq.png").convert("L")
        box = ImageOps.invert(image).point(lambda v: 255 if v > 5 else 0).getbbox()
        if box is None:
            sys.exit(f"Equation ({number}) rendered as an empty image; check its LaTeX in report.md")
        top, bottom = max(0, box[1] - 30), min(image.height, box[3] + 30)
        image.crop((0, top, image.width, bottom)).save(out)  # full width keeps the number at the margin


def equations_to_images(body: str, folder: Path) -> str:
    """Replace each display equation with a full-width image (docx build only)."""

    def swap(match: re.Match) -> str:
        out = folder / f"eq{match.group(2)}.png"
        render_equation(match.group(1), match.group(2), out)
        return f"![](<{out.as_posix()}>){{width=100%}}"  # <...>: paths may contain spaces

    return EQUATION.sub(swap, body)


def equations_to_latex(body: str) -> str:
    """Replace each display equation with an equation environment carrying its number."""

    def swap(match: re.Match) -> str:
        return (
            "```{=latex}\n\\begin{equation*}\n"
            + match.group(1).strip()
            + " \\tag{"
            + match.group(2)
            + "}\n\\end{equation*}\n```"
        )

    return EQUATION.sub(swap, body)


def build_docx(meta: dict, body: str, template: Path, out: Path, work: Path) -> None:
    ref = work / "reference.docx"
    make_reference(template, ref)
    md = work / "report_docx.md"
    body = equations_to_images(body, work)
    md.write_text(front_markdown(meta) + body, encoding="utf-8")
    raw = work / "raw.docx"
    subprocess.run(
        [
            "pandoc",
            str(md),
            "--from=markdown",
            "--to=docx",
            f"--reference-doc={ref}",
            "--citeproc",
            f"--bibliography={FOLDER / 'references.bib'}",
            f"--resource-path={FOLDER}",
            "-o",
            str(raw),
        ],
        check=True,
        cwd=FOLDER,
    )
    # pandoc copies the template's font table and its relationships, but not the font files.
    embed_fonts(raw, template)
    doc = Document(str(raw))
    style_tables(doc)
    for previous, par in zip(doc.paragraphs, doc.paragraphs[1:], strict=False):
        if par.style.name == "Source Code":
            previous.paragraph_format.keep_with_next = True  # the sentence that introduces the code
    for par in doc.paragraphs:
        if par.style.name in ("Captioned Figure", "Figure"):
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.paragraph_format.keep_with_next = True  # a figure stays with its caption
        elif par._p.xpath(".//pic:pic"):
            # An equation image: no keep-with-next, so a heading block can end a page before it.
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(str(out))
    fix_schema(out)


def build_pdf(docx_path: Path) -> Path:
    pdf = docx_path.with_suffix(".pdf")
    pdf.unlink(missing_ok=True)  # never leave a stale PDF that looks like a fresh one
    res = subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(docx_path.parent), str(docx_path)],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0 or not pdf.exists():
        sys.exit(f"LibreOffice did not write {pdf.name} (close any open LibreOffice window and retry):\n{res.stderr}")
    return pdf


# ---------------------------------------------------------------- LaTeX

# OT1 (no fontenc line): T1 needs the cm-super or lmodern packages for vector fonts, which a basic
# TeX Live lacks; without them pdflatex embeds blurry bitmap fonts.
LATEX_PREAMBLE = r"""% Generated by scripts/build_report.py from report.md. Edit report.md, then rebuild.
\documentclass[11pt]{article}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{2020}{\dag}
\DeclareUnicodeCharacter{03BC}{\ensuremath{\mu}}
\DeclareUnicodeCharacter{03C0}{\ensuremath{\pi}}
\DeclareUnicodeCharacter{03A3}{\ensuremath{\Sigma}}
\DeclareUnicodeCharacter{0394}{\ensuremath{\Delta}}
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
\DeclareUnicodeCharacter{2032}{\ensuremath{'}}
\usepackage{amsmath}
\usepackage{xcolor}
\definecolor{linkblue}{HTML}{1155CC}
\usepackage{graphicx}
\setkeys{Gin}{keepaspectratio}
\usepackage{float}
\floatplacement{figure}{H}
\usepackage{longtable,booktabs,array,calc}
\usepackage{etoolbox}
\makeatletter
\patchcmd\longtable{\par}{\if@noskipsec\mbox{}\fi\par}{}{}
\def\verbatim@font{\scriptsize\ttfamily}
\makeatother
\AtBeginEnvironment{longtable}{\footnotesize}
\usepackage{caption}
\captionsetup{font=small,labelformat=empty,skip=4pt}
\usepackage{enumitem}
\setlist{itemsep=1pt,topsep=3pt,parsep=0pt}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\usepackage{natbib}
\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=linkblue]{hyperref}
\setlength{\parskip}{4pt}
\setlength{\parindent}{0pt}
"""


def _latex(markdown: str) -> str:
    """Markdown to LaTeX through pandoc, so special characters (& % # _ $) are escaped."""
    return subprocess.run(
        ["pandoc", "--from=markdown", "--to=latex"], input=markdown, capture_output=True, text=True, check=True
    ).stdout


def build_tex(meta: dict, body: str, out: Path) -> None:
    refs = re.compile(r"# References \{-\}\s*::: \{#refs\}\s*:::\s*", re.S)
    if not refs.search(body):
        raise SystemExit("report.md needs a '# References {-}' heading followed by '::: {#refs}'")
    bib = "```{=latex}\n\\bibliographystyle{apalike}\n\\bibliography{references}\n```\n\n"
    body = refs.sub(lambda _match: bib, body)  # a function: re.sub would read "\\b" as a backspace
    body = equations_to_latex(body)
    # Combining accents (macron, circumflex) cannot be typeset by pdflatex; use math accents.
    body = re.sub("(\\w)\u0304", lambda m: "$\\bar{" + m.group(1) + "}$", body)
    body = re.sub("(\\w)\u0302", lambda m: "$\\hat{" + m.group(1) + "}$", body)
    res = subprocess.run(
        ["pandoc", "--from=markdown", "--to=latex", "--natbib", "--wrap=preserve"],
        input=body,
        capture_output=True,
        text=True,
        check=True,
    )
    latex_body = res.stdout.replace("\\section*{References}", "")
    abstract = _latex(meta["abstract"])
    affiliation = "\\\\".join(_latex(line).strip() for line in _lines(meta["affiliation"]))
    title_lines = "\\\\".join(_latex(line).strip() for line in _lines(meta["title"]))
    meta = {
        key: _latex(value).strip() if key != "sprint_url" else value
        for key, value in meta.items()
        if key not in ("affiliation", "title")
    }
    meta["affiliation"] = affiliation
    meta["title"] = title_lines
    title = (
        "\\title{\\bfseries "
        + meta["title"]
        + "\\thanks{Research conducted at the \\href{"
        + meta["sprint_url"]
        + "}{AI Collusion Research Sprint}, October 2026.}}\n"
        + "\\author{\\textbf{"
        + meta["author"]
        + "}\\\\[2pt]\\small "
        + meta["affiliation"]
        + "\\\\\\small\\texttt{"
        + meta["email"]
        + "}\\\\[8pt]\\textbf{With}\\\\Apart Research}\n\\date{}\n"
    )
    text = (
        LATEX_PREAMBLE
        + "\\renewcommand{\\refname}{References}\n"
        + title
        + "\\begin{document}\n\\maketitle\n\\begin{abstract}\n"
        + abstract
        + "\\end{abstract}\n\n"
        + latex_body
        + "\n\\end{document}\n"
    )
    out.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", type=Path, default=TEMPLATE)
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--no-tex", action="store_true")
    args = parser.parse_args()
    for tool in ("pandoc", "pdflatex", "pdftoppm"):  # pdflatex and pdftoppm typeset the equations
        if shutil.which(tool) is None:
            sys.exit(f"{tool} is required (pandoc; a TeX distribution; poppler-utils)")
    meta, body = split_front_matter(SOURCE.read_text(encoding="utf-8"))
    words = len(re.sub(r"\$[^$]*\$", "X", meta["abstract"]).split())
    print(f"abstract: {words} words (required: 150-250)")
    with tempfile.TemporaryDirectory() as tmp:
        out = FOLDER / "report.docx"
        build_docx(meta, body, args.template, out, Path(tmp))
        print(f"wrote {out.relative_to(ROOT)}")
    if not args.no_pdf:
        pdf = build_pdf(out)
        print(f"wrote {pdf.relative_to(ROOT)}")
    if not args.no_tex:
        tex = FOLDER / "main3.tex"
        build_tex(copy.deepcopy(meta), body, tex)
        print(f"wrote {tex.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
