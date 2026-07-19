"""Genera el documento de referencia usado por Pandoc para Word APA 7."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "docs" / "informe" / "referencia-apa7.docx"


def configurar_fuente(estilo, nombre="Times New Roman", tamano=12, negrita=False):
    estilo.font.name = nombre
    estilo.font.size = Pt(tamano)
    estilo.font.bold = negrita


def main():
    documento = Document()
    seccion = documento.sections[0]
    seccion.top_margin = Inches(1)
    seccion.bottom_margin = Inches(1)
    seccion.left_margin = Inches(1)
    seccion.right_margin = Inches(1)
    seccion.header_distance = Inches(0.5)
    seccion.footer_distance = Inches(0.5)

    normal = documento.styles["Normal"]
    configurar_fuente(normal)
    normal.paragraph_format.line_spacing = 2
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.first_line_indent = Inches(0.5)

    titulo = documento.styles["Title"]
    configurar_fuente(titulo, negrita=True)
    titulo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    titulo.paragraph_format.line_spacing = 2
    titulo.paragraph_format.space_after = Pt(0)

    for nombre in ("Subtitle", "Author", "Date"):
        if nombre in documento.styles:
            estilo = documento.styles[nombre]
            configurar_fuente(estilo)
            estilo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            estilo.paragraph_format.line_spacing = 2
            estilo.paragraph_format.space_after = Pt(0)

    encabezado_uno = documento.styles["Heading 1"]
    configurar_fuente(encabezado_uno, negrita=True)
    encabezado_uno.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    encabezado_uno.paragraph_format.line_spacing = 2
    encabezado_uno.paragraph_format.space_before = Pt(0)
    encabezado_uno.paragraph_format.space_after = Pt(0)

    encabezado_dos = documento.styles["Heading 2"]
    configurar_fuente(encabezado_dos, negrita=True)
    encabezado_dos.paragraph_format.line_spacing = 2
    encabezado_dos.paragraph_format.space_before = Pt(0)
    encabezado_dos.paragraph_format.space_after = Pt(0)

    encabezado_tres = documento.styles["Heading 3"]
    configurar_fuente(encabezado_tres, negrita=True)
    encabezado_tres.font.italic = True
    encabezado_tres.paragraph_format.line_spacing = 2

    leyenda = documento.styles["Caption"]
    configurar_fuente(leyenda, tamano=11)
    leyenda.paragraph_format.line_spacing = 2
    leyenda.paragraph_format.space_after = Pt(0)

    if "Bibliography" in documento.styles:
        bibliografia = documento.styles["Bibliography"]
        configurar_fuente(bibliografia)
        bibliografia.paragraph_format.line_spacing = 2
        bibliografia.paragraph_format.left_indent = Inches(0.5)
        bibliografia.paragraph_format.first_line_indent = Inches(-0.5)
        bibliografia.paragraph_format.space_after = Pt(0)

    documento.core_properties.title = "Referencia APA 7 - Mundial Trivia Challenge"
    documento.core_properties.subject = "Plantilla de estilos para Pandoc"
    documento.save(SALIDA)
    print(f"Referencia Word creada: {SALIDA}")


if __name__ == "__main__":
    main()
