"""
PDF Generator - Core Layer
Generador de reportes en formato PDF con diseños profesionales y personalizados

Single Responsibility: Generar archivos PDF con estilos avanzados

Nota: reportlab no tiene stubs de tipos oficiales, se ignoran errores de type checking
"""

# pyright: reportMissingTypeStubs=false

import io
from datetime import datetime

from reportlab.lib import colors  # type: ignore[import-untyped]
from reportlab.lib.pagesizes import letter  # type: ignore[import-untyped]
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore[import-untyped]
from reportlab.lib.units import inch  # type: ignore[import-untyped]
from reportlab.platypus import (  # type: ignore[import-untyped]
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PDFGenerator:
    """
    Generador de reportes PDF con diseños profesionales.

    Single Responsibility: Crear PDFs con estilos avanzados, colores y diseño personalizado.
    """

    # Paleta de colores - Tema Light App Móvil (Hacienda Gamelera)
    COLOR_PRIMARY = colors.HexColor("#255946")  # Verde marca principal
    COLOR_PRIMARY_LIGHT = colors.HexColor("#49A760")  # Verde claro
    COLOR_PRIMARY_DARK = colors.HexColor("#1F4E3D")  # Verde oscuro
    COLOR_ACCENT = colors.HexColor("#EFB443")  # Dorado accent
    COLOR_SUCCESS = colors.HexColor("#49A760")  # Verde claro (success)
    COLOR_ERROR = colors.HexColor("#EF4444")  # Rojo (error)
    COLOR_WARNING = colors.HexColor("#EFB443")  # Dorado (warning)
    COLOR_HEADER = colors.HexColor("#255946")  # Verde primario para headers
    COLOR_LIGHT = colors.HexColor("#FAFAFA")  # Surface (gris muy claro)
    COLOR_DARK = colors.HexColor("#212121")  # Texto principal (gris oscuro)
    COLOR_BACKGROUND = colors.HexColor("#FFFFFF")  # Blanco (background)
    COLOR_TEXT_SECONDARY = colors.HexColor("#757575")  # Gris texto secundario

    @staticmethod
    def generate_traceability_report(data: dict) -> bytes:
        """Genera reporte PDF de trazabilidad con diseño profesional."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter, topMargin=0.4 * inch, bottomMargin=0.4 * inch
        )
        story = []
        styles = getSampleStyleSheet()

        # Título principal con estilo
        title_style = styles["Title"]
        title_style.textColor = PDFGenerator.COLOR_PRIMARY
        title_style.fontSize = 18
        title_style.alignment = 1  # Center
        story.append(Paragraph("📋 REPORTE DE TRAZABILIDAD", title_style))
        story.append(Spacer(1, 0.3 * inch))

        animal = data["animal"]

        # Información del animal con tabla estilizada
        story.append(
            Paragraph(
                '<font color="#255946" size="14"><b>INFORMACIÓN DEL ANIMAL</b></font>',
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))

        animal_info = [
            ["<b>Caravana:</b>", animal.ear_tag],
            ["<b>Raza:</b>", animal.breed],
            ["<b>Género:</b>", animal.gender],
            ["<b>Fecha de Nacimiento:</b>", animal.birth_date.strftime("%Y-%m-%d")],
            ["<b>Edad (meses):</b>", str(animal.calculate_age_months())],
            ["<b>Estado:</b>", animal.status.upper()],
        ]

        if animal.name:
            animal_info.insert(1, ["<b>Nombre:</b>", animal.name])

        table = Table(animal_info, colWidths=[2.2 * inch, 4.3 * inch])
        table.setStyle(
            TableStyle(
                [
                    # Header styling
                    ("BACKGROUND", (0, 0), (0, -1), PDFGenerator.COLOR_HEADER),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (0, -1), 10),
                    # Data styling
                    ("BACKGROUND", (1, 0), (1, -1), PDFGenerator.COLOR_BACKGROUND),
                    ("TEXTCOLOR", (1, 0), (1, -1), PDFGenerator.COLOR_DARK),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (1, 0), (1, -1), 10),
                    # Alignment
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # Padding
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    # Borders
                    ("GRID", (0, 0), (-1, -1), 1, PDFGenerator.COLOR_DARK),
                    ("LINEBELOW", (0, -1), (-1, -1), 2, PDFGenerator.COLOR_PRIMARY),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))

        # Resumen de estimaciones
        summary = data["summary"]
        story.append(
            Paragraph(
                '<font color="#255946" size="14"><b>RESUMEN DE PESOS</b></font>',
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))

        summary_info = [
            [
                "<b>Total de Estimaciones:</b>",
                f'<font color="#255946"><b>{summary["total_weight_estimations"]}</b></font>',
            ],
            [
                "<b>Peso Actual:</b>",
                (
                    f'<font color="#49A760"><b>{summary["current_weight"]:.2f} kg</b></font>'
                    if summary["current_weight"]
                    else "<i>N/A</i>"
                ),
            ],
            [
                "<b>Primer Peso:</b>",
                (
                    f'<font color="#EFB443"><b>{summary["first_weight"]:.2f} kg</b></font>'
                    if summary["first_weight"]
                    else "<i>N/A</i>"
                ),
            ],
        ]

        summary_table = Table(summary_info, colWidths=[2.5 * inch, 4 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), PDFGenerator.COLOR_LIGHT),
                    ("BACKGROUND", (1, 0), (1, -1), PDFGenerator.COLOR_BACKGROUND),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 1, PDFGenerator.COLOR_DARK),
                    (
                        "ROWBACKGROUNDS",
                        (0, 0),
                        (-1, -1),
                        [PDFGenerator.COLOR_BACKGROUND, PDFGenerator.COLOR_LIGHT],
                    ),
                ]
            )
        )
        story.append(summary_table)

        # Footer
        story.append(Spacer(1, 0.4 * inch))
        footer_style = styles["Normal"]
        footer_style.fontSize = 8
        footer_style.textColor = PDFGenerator.COLOR_TEXT_SECONDARY
        footer_style.alignment = 1  # Center
        story.append(
            Paragraph(
                f"Generado el {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | "
                f"Sistema de Estimación de Peso Bovino",
                footer_style,
            )
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_inventory_report(data: dict) -> bytes:
        """Genera reporte PDF de inventario con diseño profesional."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter, topMargin=0.4 * inch, bottomMargin=0.4 * inch
        )
        story = []
        styles = getSampleStyleSheet()

        # Título
        title_style = styles["Title"]
        title_style.textColor = PDFGenerator.COLOR_PRIMARY
        title_style.fontSize = 18
        title_style.alignment = 1
        story.append(Paragraph("📊 REPORTE DE INVENTARIO", title_style))
        story.append(Spacer(1, 0.3 * inch))

        stats = data["statistics"]

        # Estadísticas por raza
        if stats["by_breed"]:
            story.append(
                Paragraph(
                    '<font color="#2C3E50" size="14"><b>DISTRIBUCIÓN POR RAZA</b></font>',
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 0.15 * inch))

            breed_rows = [["RAZA", "CANTIDAD", "PORCENTAJE"]]
            total = data["total_animals"]
            for breed, count in sorted(
                stats["by_breed"].items(), key=lambda x: x[1], reverse=True
            ):
                percentage = (count / total * 100) if total > 0 else 0
                breed_rows.append([breed, str(count), f"{percentage:.1f}%"])

            breed_table = Table(
                breed_rows, colWidths=[3 * inch, 1.5 * inch, 1.5 * inch]
            )
            breed_table.setStyle(
                TableStyle(
                    [
                        # Header
                        ("BACKGROUND", (0, 0), (-1, 0), PDFGenerator.COLOR_HEADER),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 11),
                        # Data
                        ("BACKGROUND", (1, 1), (-1, -1), PDFGenerator.COLOR_LIGHT),
                        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 1, PDFGenerator.COLOR_DARK),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [PDFGenerator.COLOR_BACKGROUND, PDFGenerator.COLOR_LIGHT],
                        ),
                    ]
                )
            )
            story.append(breed_table)
            story.append(Spacer(1, 0.3 * inch))

        # Resumen total
        story.append(
            Paragraph(
                f'<font color="#49A760" size="16"><b>TOTAL DE ANIMALES: {data["total_animals"]}</b></font>',
                styles["Normal"],
            )
        )

        # Footer
        story.append(Spacer(1, 0.4 * inch))
        footer_style = styles["Normal"]
        footer_style.fontSize = 8
        footer_style.textColor = PDFGenerator.COLOR_TEXT_SECONDARY
        footer_style.alignment = 1
        story.append(
            Paragraph(
                f"Generado el {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | "
                f"Sistema de Estimación de Peso Bovino",
                footer_style,
            )
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_movements_report(data: dict) -> bytes:
        """Genera reporte PDF de movimientos con diseño profesional."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter, topMargin=0.4 * inch, bottomMargin=0.4 * inch
        )
        story = []
        styles = getSampleStyleSheet()

        # Título
        title_style = styles["Title"]
        title_style.textColor = PDFGenerator.COLOR_PRIMARY
        title_style.fontSize = 18
        title_style.alignment = 1
        story.append(Paragraph("🔄 REPORTE DE MOVIMIENTOS", title_style))
        story.append(Spacer(1, 0.3 * inch))

        summary = data["summary"]

        # Resumen con colores según tipo
        story.append(
            Paragraph(
                '<font color="#2C3E50" size="14"><b>RESUMEN DE MOVIMIENTOS</b></font>',
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.15 * inch))

        summary_info = [
            [
                "<b>Total de Movimientos:</b>",
                f'<font color="#255946"><b>{summary["total_movements"]}</b></font>',
            ],
            [
                "<b>Vendidos:</b>",
                f'<font color="#49A760"><b>{summary["total_sold"]}</b></font>',
            ],
            [
                "<b>Fallecidos:</b>",
                f'<font color="#EF4444"><b>{summary["total_deceased"]}</b></font>',
            ],
        ]

        summary_table = Table(summary_info, colWidths=[2.5 * inch, 4 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), PDFGenerator.COLOR_LIGHT),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("GRID", (0, 0), (-1, -1), 1, PDFGenerator.COLOR_DARK),
                    (
                        "ROWBACKGROUNDS",
                        (0, 0),
                        (-1, -1),
                        [
                            PDFGenerator.COLOR_BACKGROUND,
                            PDFGenerator.COLOR_LIGHT,
                            PDFGenerator.COLOR_BACKGROUND,
                        ],
                    ),
                ]
            )
        )
        story.append(summary_table)

        # Footer
        story.append(Spacer(1, 0.4 * inch))
        footer_style = styles["Normal"]
        footer_style.fontSize = 8
        footer_style.textColor = PDFGenerator.COLOR_TEXT_SECONDARY
        footer_style.alignment = 1
        story.append(
            Paragraph(
                f"Generado el {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | "
                f"Sistema de Estimación de Peso Bovino",
                footer_style,
            )
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_growth_report(data: dict) -> bytes:
        """Genera reporte PDF de crecimiento con diseño profesional."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter, topMargin=0.4 * inch, bottomMargin=0.4 * inch
        )
        story = []
        styles = getSampleStyleSheet()

        # Título
        title_style = styles["Title"]
        title_style.textColor = PDFGenerator.COLOR_PRIMARY
        title_style.fontSize = 18
        title_style.alignment = 1
        story.append(Paragraph("📈 REPORTE DE CRECIMIENTO", title_style))
        story.append(Spacer(1, 0.3 * inch))

        if data["type"] == "individual":
            metrics = data["growth_metrics"]
            story.append(
                Paragraph(
                    '<font color="#2C3E50" size="14"><b>MÉTRICAS DE CRECIMIENTO</b></font>',
                    styles["Normal"],
                )
            )
            story.append(Spacer(1, 0.15 * inch))

            growth_info = [
                [
                    "<b>GDP (Ganancia Diaria Promedio):</b>",
                    (
                        f'<font color="#49A760"><b>{metrics["gdp"]:.2f} kg/día</b></font>'
                        if metrics["gdp"]
                        else "<i>N/A</i>"
                    ),
                ],
                [
                    "<b>Total de Mediciones:</b>",
                    f'<font color="#255946"><b>{metrics["total_measurements"]}</b></font>',
                ],
                [
                    "<b>Peso Actual:</b>",
                    (
                        f'<font color="#EFB443"><b>{metrics["current_weight"]:.2f} kg</b></font>'
                        if metrics["current_weight"]
                        else "<i>N/A</i>"
                    ),
                ],
                [
                    "<b>Ganancia Total:</b>",
                    (
                        f'<font color="#49A760"><b>{metrics["weight_gain"]:.2f} kg</b></font>'
                        if metrics["weight_gain"]
                        else "<i>N/A</i>"
                    ),
                ],
            ]

            growth_table = Table(growth_info, colWidths=[3 * inch, 3.5 * inch])
            growth_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (0, -1), PDFGenerator.COLOR_LIGHT),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 11),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, PDFGenerator.COLOR_DARK),
                        (
                            "ROWBACKGROUNDS",
                            (0, 0),
                            (-1, -1),
                            [PDFGenerator.COLOR_BACKGROUND, PDFGenerator.COLOR_LIGHT]
                            * 2,
                        ),
                    ]
                )
            )
            story.append(growth_table)

        # Footer
        story.append(Spacer(1, 0.4 * inch))
        footer_style = styles["Normal"]
        footer_style.fontSize = 8
        footer_style.textColor = PDFGenerator.COLOR_TEXT_SECONDARY
        footer_style.alignment = 1
        story.append(
            Paragraph(
                f"Generado el {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | "
                f"Sistema de Estimación de Peso Bovino",
                footer_style,
            )
        )

        doc.build(story)
        buffer.seek(0)
        return buffer.read()
