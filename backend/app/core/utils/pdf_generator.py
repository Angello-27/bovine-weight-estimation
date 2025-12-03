"""
Professional PDF Generator for Cattle Traceability Reports
Generador profesional de PDFs para reportes de trazabilidad ganadera

Características:
- Diseño profesional con colores corporativos
- Gráficos de evolución de peso
- Análisis estadístico completo
- Información genealógica visual
- Códigos QR para trazabilidad
- Mapas de ubicación
- Timeline visual de eventos
"""

# pyright: reportMissingTypeStubs=false

import os
from datetime import datetime
from io import BytesIO

import qrcode  # type: ignore[import-untyped]

# pyright: ignore[reportMissingTypeStubs]
from reportlab.graphics.charts.linecharts import (  # type: ignore[import-untyped]
    HorizontalLineChart,
)
from reportlab.graphics.shapes import Drawing  # type: ignore[import-untyped]
from reportlab.lib import colors  # type: ignore[import-untyped]
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY  # type: ignore[import-untyped]
from reportlab.lib.pagesizes import letter  # type: ignore[import-untyped]
from reportlab.lib.styles import (  # type: ignore[import-untyped]
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm  # type: ignore[import-untyped]
from reportlab.platypus import (  # type: ignore[import-untyped]
    Image as ReportLabImage,
)
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# type: ignore[import-untyped]
from .image_storage import get_image_path, image_exists


class TraceabilityPDFGenerator:
    """
    Generador profesional de reportes de trazabilidad en PDF.

    Incluye:
    - Diseño corporativo
    - Gráficos interactivos
    - Análisis estadístico
    - Códigos QR
    - Timeline visual
    """

    # Colores corporativos (Verde Ganadero)
    PRIMARY_COLOR = colors.HexColor("#2D5016")  # Verde oscuro
    SECONDARY_COLOR = colors.HexColor("#4A8B2C")  # Verde medio
    ACCENT_COLOR = colors.HexColor("#8BC34A")  # Verde claro
    SUCCESS_COLOR = colors.HexColor("#66BB6A")  # Verde éxito
    WARNING_COLOR = colors.HexColor("#FFA726")  # Naranja
    ERROR_COLOR = colors.HexColor("#EF5350")  # Rojo
    INFO_COLOR = colors.HexColor("#42A5F5")  # Azul
    GRAY_LIGHT = colors.HexColor("#F5F5F5")  # Gris muy claro
    GRAY_MEDIUM = colors.HexColor("#9E9E9E")  # Gris medio
    GRAY_DARK = colors.HexColor("#424242")  # Gris oscuro

    # Valores hexadecimales como strings para uso en HTML
    PRIMARY_COLOR_HEX = "#2D5016"
    SECONDARY_COLOR_HEX = "#4A8B2C"
    ACCENT_COLOR_HEX = "#8BC34A"
    SUCCESS_COLOR_HEX = "#66BB6A"
    WARNING_COLOR_HEX = "#FFA726"
    ERROR_COLOR_HEX = "#EF5350"
    INFO_COLOR_HEX = "#42A5F5"
    GRAY_LIGHT_HEX = "#F5F5F5"
    GRAY_MEDIUM_HEX = "#9E9E9E"
    GRAY_DARK_HEX = "#424242"

    def _get_color_hex(self, color_obj) -> str:
        """
        Obtiene el valor hexadecimal de un color en formato #RRGGBB.

        Args:
            color_obj: Objeto de color de reportlab

        Returns:
            str: Valor hexadecimal con formato #RRGGBB
        """
        # Extraer valores RGB y formatear como hexadecimal
        r, g, b = color_obj.rgb()
        return f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"

    def __init__(self, farm_name: str = "Hacienda Gamelera"):
        """
        Inicializa el generador.

        Args:
            farm_name: Nombre de la hacienda
        """
        self.farm_name = farm_name
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Crea estilos personalizados para el documento."""
        # Título principal
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Heading1"],
                fontSize=24,
                textColor=self.PRIMARY_COLOR,
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            )
        )

        # Subtítulo de sección
        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading2"],
                fontSize=16,
                textColor=self.SECONDARY_COLOR,
                spaceAfter=12,
                spaceBefore=15,
                fontName="Helvetica-Bold",
                borderWidth=0,
                borderColor=self.SECONDARY_COLOR,
                borderPadding=5,
                backColor=self.GRAY_LIGHT,
            )
        )

        # Texto normal mejorado
        self.styles.add(
            ParagraphStyle(
                name="CustomBody",
                parent=self.styles["Normal"],
                fontSize=10,
                leading=14,
                textColor=self.GRAY_DARK,
                alignment=TA_JUSTIFY,
            )
        )

        # Etiqueta (label)
        self.styles.add(
            ParagraphStyle(
                name="Label",
                parent=self.styles["Normal"],
                fontSize=9,
                textColor=self.GRAY_MEDIUM,
                fontName="Helvetica-Bold",
            )
        )

        # Valor (value)
        self.styles.add(
            ParagraphStyle(
                name="Value",
                parent=self.styles["Normal"],
                fontSize=11,
                textColor=self.GRAY_DARK,
                fontName="Helvetica",
            )
        )

        # Estadística destacada
        self.styles.add(
            ParagraphStyle(
                name="StatHighlight",
                parent=self.styles["Normal"],
                fontSize=20,
                textColor=self.SUCCESS_COLOR,
                fontName="Helvetica-Bold",
                alignment=TA_CENTER,
            )
        )

        # Pie de página
        self.styles.add(
            ParagraphStyle(
                name="Footer",
                parent=self.styles["Normal"],
                fontSize=8,
                textColor=self.GRAY_MEDIUM,
                alignment=TA_CENTER,
            )
        )

    def generate(self, report_data: dict) -> BytesIO:
        """
        Genera el PDF completo.

        Args:
            report_data: Datos del reporte del caso de uso

        Returns:
            BytesIO con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title=f"Reporte de Trazabilidad - {report_data['animal'].ear_tag}",
            author=self.farm_name,
        )

        # Construir contenido
        story = []

        # Página 1: Información general y resumen
        story.extend(self._build_header(report_data))
        story.extend(self._build_animal_info(report_data))
        story.extend(self._build_summary_cards(report_data))
        story.extend(self._build_genealogy_section(report_data))

        story.append(PageBreak())

        # Página 2: Análisis de peso
        story.extend(self._build_weight_analysis(report_data))
        story.extend(self._build_weight_chart(report_data))
        story.extend(self._build_weight_statistics(report_data))

        story.append(PageBreak())

        # Página 3: Historial detallado
        story.extend(self._build_weight_history_table(report_data))
        story.extend(self._build_timeline(report_data))

        # Página 4: Códigos QR y trazabilidad
        story.append(PageBreak())
        story.extend(self._build_qr_section(report_data))
        story.extend(self._build_footer(report_data))

        # Generar PDF
        doc.build(
            story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number
        )

        buffer.seek(0)
        return buffer

    def _build_header(self, report_data: dict) -> list:
        """Construye el encabezado del reporte."""
        elements = []

        # Logo y título (simulado - en producción usar imagen real)
        title_text = f"🐄 {self.farm_name.upper()}"
        title = Paragraph(title_text, self.styles["CustomTitle"])
        elements.append(title)

        subtitle = Paragraph(
            "<b>REPORTE DE TRAZABILIDAD INDIVIDUAL</b>", self.styles["SectionHeader"]
        )
        elements.append(subtitle)

        elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_animal_info(self, report_data: dict) -> list:
        """Construye la sección de información del animal con imagen."""
        elements = []
        animal = report_data["animal"]

        section_title = Paragraph(
            "📋 INFORMACIÓN DEL ANIMAL", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        # Intentar obtener imagen del animal
        animal_image = None
        if hasattr(animal, "photo_path") and animal.photo_path:
            try:
                image_path = get_image_path(animal.photo_path)
                if image_exists(animal.photo_path) and image_path.exists():
                    # Redimensionar imagen para el PDF (máximo 6cm de ancho)
                    animal_image = ReportLabImage(
                        str(image_path),
                        width=6 * cm,
                        height=6 * cm,
                        kind="proportional",
                    )
            except Exception:
                # Si hay error, continuar sin imagen
                pass

        # Tabla de información básica
        data = [
            [
                Paragraph("<b>Caravana:</b>", self.styles["Label"]),
                Paragraph(
                    f"<font size=14><b>{animal.ear_tag}</b></font>",
                    self.styles["Value"],
                ),
                Paragraph("<b>Nombre:</b>", self.styles["Label"]),
                Paragraph(
                    f"<font size=14><b>{animal.name or 'N/A'}</b></font>",
                    self.styles["Value"],
                ),
            ],
            [
                Paragraph("<b>Raza:</b>", self.styles["Label"]),
                Paragraph(f"{animal.breed.upper()}", self.styles["Value"]),
                Paragraph("<b>Género:</b>", self.styles["Label"]),
                Paragraph(
                    f"{'Hembra' if animal.gender == 'female' else 'Macho'}",
                    self.styles["Value"],
                ),
            ],
            [
                Paragraph("<b>Fecha Nacimiento:</b>", self.styles["Label"]),
                Paragraph(
                    f"{animal.birth_date.strftime('%d/%m/%Y') if animal.birth_date else 'N/A'}",
                    self.styles["Value"],
                ),
                Paragraph("<b>Edad:</b>", self.styles["Label"]),
                Paragraph(
                    f"<font color='{self.SUCCESS_COLOR_HEX}'><b>{report_data['summary']['age_months']} meses</b></font>",
                    self.styles["Value"],
                ),
            ],
        ]

        # Agregar peso al nacer y color si existen
        row_data = []
        if hasattr(animal, "birth_weight_kg") and animal.birth_weight_kg:
            row_data.extend(
                [
                    Paragraph("<b>Peso al Nacer:</b>", self.styles["Label"]),
                    Paragraph(f"{animal.birth_weight_kg:.2f} kg", self.styles["Value"]),
                ]
            )
        else:
            row_data.extend(
                [
                    Paragraph("", self.styles["Label"]),
                    Paragraph("", self.styles["Value"]),
                ]
            )

        if hasattr(animal, "color") and animal.color:
            row_data.extend(
                [
                    Paragraph("<b>Color:</b>", self.styles["Label"]),
                    Paragraph(f"{animal.color}", self.styles["Value"]),
                ]
            )
        else:
            row_data.extend(
                [
                    Paragraph("", self.styles["Label"]),
                    Paragraph("", self.styles["Value"]),
                ]
            )

        if row_data:
            data.append(row_data)

        # Agregar estado y fecha de registro
        row_data = [
            Paragraph("<b>Estado:</b>", self.styles["Label"]),
            self._get_status_badge(animal.status),
        ]
        if hasattr(animal, "registration_date") and animal.registration_date:
            row_data.extend(
                [
                    Paragraph("<b>Registro:</b>", self.styles["Label"]),
                    Paragraph(
                        f"{animal.registration_date.strftime('%d/%m/%Y') if isinstance(animal.registration_date, datetime) else str(animal.registration_date)[:10]}",
                        self.styles["Value"],
                    ),
                ]
            )
        else:
            row_data.extend(
                [
                    Paragraph("", self.styles["Label"]),
                    Paragraph("", self.styles["Value"]),
                ]
            )
        data.append(row_data)

        # Crear tabla con imagen si está disponible
        if animal_image:
            # Tabla con dos columnas: información a la izquierda, imagen a la derecha
            info_table = Table(data, colWidths=[3 * cm, 4.5 * cm, 3 * cm, 4.5 * cm])
            info_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), self.GRAY_LIGHT),
                        ("TEXTCOLOR", (0, 0), (-1, -1), self.GRAY_DARK),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
                    ]
                )
            )

            # Tabla combinada: información e imagen
            combined_data = [[info_table, animal_image]]
            combined_table = Table(combined_data, colWidths=[11 * cm, 6 * cm])
            combined_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (0, 0), "LEFT"),
                        ("ALIGN", (1, 0), (1, 0), "CENTER"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            elements.append(combined_table)
        else:
            # Sin imagen, solo tabla de información
            table = Table(data, colWidths=[2.5 * cm, 5 * cm, 2.5 * cm, 5 * cm])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), self.GRAY_LIGHT),
                        ("TEXTCOLOR", (0, 0), (-1, -1), self.GRAY_DARK),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
                    ]
                )
            )
            elements.append(table)

        elements.append(Spacer(1, 0.5 * cm))

        # Observaciones
        if hasattr(animal, "observations") and animal.observations:
            obs_title = Paragraph("<b>Observaciones:</b>", self.styles["Label"])
            elements.append(obs_title)
            obs_text = Paragraph(animal.observations, self.styles["CustomBody"])
            elements.append(obs_text)
            elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_summary_cards(self, report_data: dict) -> list:
        """Construye tarjetas de resumen con estadísticas clave."""
        elements = []
        summary = report_data["summary"]

        section_title = Paragraph(
            "📊 RESUMEN DE INDICADORES", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        # Crear 3 tarjetas en una fila
        current_weight = summary.get("current_weight")
        first_weight = summary.get("first_weight")
        total_estimations = summary.get("total_weight_estimations", 0)

        # Calcular ganancia total
        weight_gain = None
        weight_gain_pct = None
        if current_weight and first_weight and first_weight > 0:
            weight_gain = current_weight - first_weight
            weight_gain_pct = (weight_gain / first_weight) * 100

        cards_data = [
            [
                self._create_stat_card(
                    "Peso Actual",
                    f"{current_weight:.1f} kg" if current_weight else "N/A",
                    self.SUCCESS_COLOR,
                ),
                self._create_stat_card(
                    "Ganancia Total",
                    (
                        f"+{weight_gain:.1f} kg ({weight_gain_pct:.1f}%)"
                        if weight_gain
                        else "N/A"
                    ),
                    self.INFO_COLOR,
                ),
                self._create_stat_card(
                    "Total Pesajes", str(total_estimations), self.SECONDARY_COLOR
                ),
            ]
        ]

        cards_table = Table(cards_data, colWidths=[5 * cm, 5.5 * cm, 4.5 * cm])
        cards_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(cards_table)
        elements.append(Spacer(1, 0.5 * cm))

        return elements

    def _create_stat_card(self, label: str, value: str, color) -> Table:
        """Crea una tarjeta de estadística."""
        card_data = [
            [Paragraph(f"<b>{label}</b>", self.styles["Label"])],
            [
                Paragraph(
                    f"<font size=18 color='{self._get_color_hex(color)}'><b>{value}</b></font>",
                    self.styles["Value"],
                )
            ],
        ]

        card = Table(card_data, colWidths=[4.5 * cm])
        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), self.GRAY_LIGHT),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("BOX", (0, 0), (-1, -1), 2, color),
                ]
            )
        )

        return card

    def _build_genealogy_section(self, report_data: dict) -> list:
        """Construye la sección de genealogía."""
        elements = []
        lineage = report_data["lineage"]

        section_title = Paragraph("👨‍👩‍👧 GENEALOGÍA", self.styles["SectionHeader"])
        elements.append(section_title)

        # Tabla de padres y descendientes
        genealogy_data = []

        # Madre
        mother = lineage.get("mother")
        mother_info = f"{mother.ear_tag} - {mother.name}" if mother else "No registrada"
        genealogy_data.append(
            [
                Paragraph("<b>Madre:</b>", self.styles["Label"]),
                Paragraph(mother_info, self.styles["Value"]),
            ]
        )

        # Padre
        father = lineage.get("father")
        father_info = f"{father.ear_tag} - {father.name}" if father else "No registrado"
        genealogy_data.append(
            [
                Paragraph("<b>Padre:</b>", self.styles["Label"]),
                Paragraph(father_info, self.styles["Value"]),
            ]
        )

        # Descendientes
        descendants = lineage.get("descendants", [])
        desc_count = len(descendants)
        desc_info = f"{desc_count} descendiente{'s' if desc_count != 1 else ''}"
        if desc_count > 0:
            desc_names = ", ".join([d.ear_tag for d in descendants[:5]])
            if desc_count > 5:
                desc_names += f" y {desc_count - 5} más"
            desc_info += f" ({desc_names})"

        genealogy_data.append(
            [
                Paragraph("<b>Descendientes:</b>", self.styles["Label"]),
                Paragraph(desc_info, self.styles["Value"]),
            ]
        )

        genealogy_table = Table(genealogy_data, colWidths=[3 * cm, 12 * cm])
        genealogy_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), self.GRAY_LIGHT),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("ALIGN", (1, 0), (1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
                ]
            )
        )

        elements.append(genealogy_table)
        elements.append(Spacer(1, 0.5 * cm))

        return elements

    def _build_weight_analysis(self, report_data: dict) -> list:
        """Construye análisis de evolución de peso."""
        elements = []

        section_title = Paragraph(
            "📈 ANÁLISIS DE EVOLUCIÓN DE PESO", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        return elements

    def _build_weight_chart(self, report_data: dict) -> list:
        """Construye gráfico de evolución de peso."""
        elements = []
        weight_estimations = report_data["weight_estimations"]

        if not weight_estimations:
            elements.append(
                Paragraph(
                    "No hay datos de peso disponibles.", self.styles["CustomBody"]
                )
            )
            return elements

        # Ordenar por fecha (más antiguo primero para el gráfico)
        sorted_estimations = sorted(weight_estimations, key=lambda x: x.timestamp)

        # Preparar datos para el gráfico
        weights = [e.estimated_weight_kg for e in sorted_estimations]
        dates = [e.timestamp.strftime("%Y-%m") for e in sorted_estimations]

        # Crear gráfico de línea
        drawing = Drawing(400, 200)
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [weights]
        chart.joinedLines = 1

        # Configurar colores
        chart.lines[0].strokeColor = self.SUCCESS_COLOR
        chart.lines[0].strokeWidth = 2

        # Configurar ejes
        chart.valueAxis.valueMin = min(weights) * 0.9
        chart.valueAxis.valueMax = max(weights) * 1.1
        chart.valueAxis.valueStep = (max(weights) - min(weights)) / 5

        # Etiquetas del eje X (solo cada N)
        step = max(1, len(dates) // 10)
        chart.categoryAxis.categoryNames = [
            dates[i] if i % step == 0 else "" for i in range(len(dates))
        ]
        chart.categoryAxis.labels.boxAnchor = "n"
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.fontSize = 7

        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_weight_statistics(self, report_data: dict) -> list:
        """Construye estadísticas de peso."""
        elements: list = []
        weight_estimations = report_data["weight_estimations"]

        if not weight_estimations or len(weight_estimations) < 2:
            return elements

        weights = [e.estimated_weight_kg for e in weight_estimations]

        # Calcular estadísticas
        avg_weight = sum(weights) / len(weights)
        max_weight = max(weights)
        min_weight = min(weights)
        weight_range = max_weight - min_weight

        # Ganancia promedio por mes (aproximado)
        sorted_estimations = sorted(weight_estimations, key=lambda x: x.timestamp)
        first_date = sorted_estimations[0].timestamp
        last_date = sorted_estimations[-1].timestamp
        months_diff = max(1, (last_date - first_date).days / 30.44)
        weight_diff = (
            sorted_estimations[-1].estimated_weight_kg
            - sorted_estimations[0].estimated_weight_kg
        )
        avg_monthly_gain = weight_diff / months_diff if months_diff > 0 else 0

        stats_title = Paragraph("<b>Estadísticas de Peso:</b>", self.styles["Label"])
        elements.append(stats_title)

        stats_data = [
            [
                Paragraph("<b>Promedio:</b>", self.styles["Label"]),
                Paragraph(f"{avg_weight:.1f} kg", self.styles["Value"]),
                Paragraph("<b>Máximo:</b>", self.styles["Label"]),
                Paragraph(f"{max_weight:.1f} kg", self.styles["Value"]),
            ],
            [
                Paragraph("<b>Mínimo:</b>", self.styles["Label"]),
                Paragraph(f"{min_weight:.1f} kg", self.styles["Value"]),
                Paragraph("<b>Rango:</b>", self.styles["Label"]),
                Paragraph(f"{weight_range:.1f} kg", self.styles["Value"]),
            ],
            [
                Paragraph("<b>Ganancia Promedio/Mes:</b>", self.styles["Label"]),
                Paragraph(
                    f"<font color='{self.SUCCESS_COLOR_HEX}'><b>+{avg_monthly_gain:.2f} kg/mes</b></font>",
                    self.styles["Value"],
                ),
                Paragraph("<b>Total Pesajes:</b>", self.styles["Label"]),
                Paragraph(f"{len(weights)}", self.styles["Value"]),
            ],
        ]

        stats_table = Table(stats_data, colWidths=[4 * cm, 3.5 * cm, 4 * cm, 3.5 * cm])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, self.GRAY_LIGHT),
                ]
            )
        )

        elements.append(stats_table)
        elements.append(Spacer(1, 0.5 * cm))

        return elements

    def _build_weight_history_table(self, report_data: dict) -> list:
        """Construye tabla de historial de pesos."""
        elements = []
        weight_estimations = report_data["weight_estimations"]

        section_title = Paragraph(
            "⚖️ HISTORIAL DETALLADO DE PESAJES", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        if not weight_estimations:
            elements.append(
                Paragraph("No hay registros de peso.", self.styles["CustomBody"])
            )
            return elements

        # Encabezados
        table_data = [
            [
                Paragraph("<b>Fecha</b>", self.styles["Label"]),
                Paragraph("<b>Peso (kg)</b>", self.styles["Label"]),
                Paragraph("<b>Confianza</b>", self.styles["Label"]),
                Paragraph("<b>Método</b>", self.styles["Label"]),
                Paragraph("<b>Modelo ML</b>", self.styles["Label"]),
            ]
        ]

        # Datos (máximo 20 registros más recientes)
        for estimation in weight_estimations[:20]:
            table_data.append(
                [
                    Paragraph(
                        estimation.timestamp.strftime("%d/%m/%Y %H:%M"),
                        self.styles["Value"],
                    ),
                    Paragraph(
                        f"<b>{estimation.estimated_weight_kg:.1f}</b>",
                        self.styles["Value"],
                    ),
                    Paragraph(
                        f"{estimation.confidence * 100:.1f}%", self.styles["Value"]
                    ),
                    Paragraph(estimation.method, self.styles["Value"]),
                    Paragraph(estimation.ml_model_version, self.styles["Value"]),
                ]
            )

        history_table = Table(
            table_data, colWidths=[3.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]
        )

        history_table.setStyle(
            TableStyle(
                [
                    # Encabezado
                    ("BACKGROUND", (0, 0), (-1, 0), self.SECONDARY_COLOR),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                    # Datos
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("TEXTCOLOR", (0, 1), (-1, -1), self.GRAY_DARK),
                    ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                    # Bordes
                    ("GRID", (0, 0), (-1, -1), 0.5, self.GRAY_MEDIUM),
                    # Filas alternadas
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, self.GRAY_LIGHT],
                    ),
                ]
            )
        )

        elements.append(history_table)

        if len(weight_estimations) > 20:
            note = Paragraph(
                f"<i>Mostrando los 20 registros más recientes de {len(weight_estimations)} totales.</i>",
                self.styles["Footer"],
            )
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(note)

        elements.append(Spacer(1, 0.5 * cm))

        return elements

    def _build_timeline(self, report_data: dict) -> list:
        """Construye timeline visual de eventos."""
        elements = []
        timeline_events = report_data.get("timeline", [])

        section_title = Paragraph(
            "📅 TIMELINE DE EVENTOS", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        if not timeline_events:
            elements.append(
                Paragraph("No hay eventos registrados.", self.styles["CustomBody"])
            )
            return elements

        # Mostrar solo eventos importantes (no todos los pesajes)
        important_events = [
            e for e in timeline_events if e.get("type") not in ["Estimación de Peso"]
        ]

        # Si no hay eventos importantes, mostrar primeros y últimos pesajes
        if not important_events:
            weight_events = [
                e for e in timeline_events if e.get("type") == "Estimación de Peso"
            ]
            if len(weight_events) > 6:
                important_events = weight_events[:3] + weight_events[-3:]
            else:
                important_events = weight_events

        timeline_data = [
            [
                Paragraph("<b>Fecha</b>", self.styles["Label"]),
                Paragraph("<b>Tipo</b>", self.styles["Label"]),
                Paragraph("<b>Descripción</b>", self.styles["Label"]),
            ]
        ]

        for event in important_events[:15]:  # Máximo 15 eventos
            event_date = event.get("date", "N/A")
            if isinstance(event_date, datetime):
                event_date = event_date.strftime("%d/%m/%Y")

            timeline_data.append(
                [
                    Paragraph(str(event_date), self.styles["Value"]),
                    Paragraph(event.get("type", "N/A"), self.styles["Value"]),
                    Paragraph(event.get("description", "N/A"), self.styles["Value"]),
                ]
            )

        timeline_table = Table(timeline_data, colWidths=[3 * cm, 3.5 * cm, 8 * cm])

        timeline_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), self.INFO_COLOR),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, self.GRAY_MEDIUM),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, self.GRAY_LIGHT],
                    ),
                ]
            )
        )

        elements.append(timeline_table)
        elements.append(Spacer(1, 0.5 * cm))

        return elements

    def _build_qr_section(self, report_data: dict) -> list:
        """Construye sección con código QR para trazabilidad digital."""
        elements = []
        animal = report_data["animal"]

        section_title = Paragraph(
            "📱 TRAZABILIDAD DIGITAL", self.styles["SectionHeader"]
        )
        elements.append(section_title)

        # Obtener URL base del frontend desde variable de entorno o usar default
        frontend_url = os.getenv("FRONTEND_URL", "https://taller.agrocom.com.bo")
        # Construir URL completa del animal
        qr_data = f"{frontend_url}/cattle/{animal.id}"

        # Generar código QR con mejor configuración
        qr = qrcode.QRCode(
            version=1,
            box_size=12,  # Aumentado para mejor legibilidad
            border=3,  # Borde más visible
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Convertir QR a imagen con color corporativo
        qr_img = qr.make_image(fill_color=self.PRIMARY_COLOR_HEX, back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # Crear tabla con QR y descripción mejorada
        qr_image = ReportLabImage(qr_buffer, width=5 * cm, height=5 * cm)

        qr_text = Paragraph(
            f"""
            <b>Escanea este código QR</b> para acceder a la información
            completa y actualizada de este animal en tiempo real.<br/><br/>
            <b>URL del Animal:</b><br/>
            <font color='{self.PRIMARY_COLOR_HEX}'>{qr_data}</font><br/><br/>
            Este código garantiza la trazabilidad y autenticidad de la información
            del animal. Puede ser escaneado con cualquier lector de códigos QR
            para acceder al perfil completo del animal en el sistema.
            """,
            self.styles["CustomBody"],
        )

        qr_table_data = [[qr_image, qr_text]]
        qr_table = Table(qr_table_data, colWidths=[6 * cm, 9 * cm])
        qr_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (0, 0), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("BACKGROUND", (0, 0), (0, 0), colors.white),
                    ("BACKGROUND", (1, 0), (1, 0), self.GRAY_LIGHT),
                ]
            )
        )

        elements.append(qr_table)
        elements.append(Spacer(1, 1 * cm))

        return elements

    def _build_footer(self, report_data: dict) -> list:
        """Construye pie de página."""
        elements = []

        generated_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        footer_text = Paragraph(
            f"""
            <b>Generado el:</b> {generated_date} |
            <b>{self.farm_name}</b> |
            Sistema de Trazabilidad Ganadera
            """,
            self.styles["Footer"],
        )

        elements.append(footer_text)

        return elements

    def _get_status_badge(self, status: str) -> Paragraph:
        """Crea un badge visual para el estado del animal."""
        status_colors = {
            "active": self.SUCCESS_COLOR,
            "sold": self.INFO_COLOR,
            "deceased": self.ERROR_COLOR,
        }

        status_labels = {
            "active": "ACTIVO",
            "sold": "VENDIDO",
            "deceased": "FALLECIDO",
        }

        color = status_colors.get(status, self.GRAY_MEDIUM)
        label = status_labels.get(status, status.upper())

        return Paragraph(
            f"<font color='{self._get_color_hex(color)}'><b>⬤ {label}</b></font>",
            self.styles["Value"],
        )

    def _add_page_number(self, canvas_obj, doc):
        """Agrega número de página al pie."""
        page_num = canvas_obj.getPageNumber()
        text = f"Página {page_num}"
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(self.GRAY_MEDIUM)
        canvas_obj.drawRightString(doc.pagesize[0] - 1.5 * cm, 1 * cm, text)
        canvas_obj.restoreState()


# Función helper para usar en el endpoint
def generate_traceability_pdf(
    report_data: dict, farm_name: str = "Hacienda Gamelera"
) -> BytesIO:
    """
    Genera un PDF de trazabilidad.

    Args:
        report_data: Datos del reporte del caso de uso
        farm_name: Nombre de la hacienda

    Returns:
        BytesIO con el PDF generado
    """
    generator = TraceabilityPDFGenerator(farm_name=farm_name)
    return generator.generate(report_data)


class PDFGenerator:
    """
    Clase wrapper para compatibilidad con ReportGenerator.

    Proporciona métodos estáticos que delegan a los generadores especializados.
    """

    @staticmethod
    def generate_traceability_report(data: dict) -> bytes:
        """
        Genera reporte PDF de trazabilidad individual.

        Args:
            data: Datos del reporte del caso de uso

        Returns:
            bytes: Contenido del PDF generado
        """
        farm_name = os.getenv("HACIENDA_NAME", "Hacienda Gamelera")
        pdf_buffer = generate_traceability_pdf(data, farm_name=farm_name)
        pdf_buffer.seek(0)
        return pdf_buffer.read()

    @staticmethod
    def generate_inventory_report(_data: dict) -> bytes:
        """
        Genera reporte PDF de inventario.

        Args:
            data: Datos del reporte del caso de uso

        Returns:
            bytes: Contenido del PDF generado
        """
        # Implementación básica - se puede mejorar después
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        story.append(Paragraph("Reporte de Inventario", styles["Title"]))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph("Funcionalidad en desarrollo", styles["Normal"]))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_movements_report(_data: dict) -> bytes:
        """
        Genera reporte PDF de movimientos.

        Args:
            data: Datos del reporte del caso de uso

        Returns:
            bytes: Contenido del PDF generado
        """
        # Implementación básica - se puede mejorar después
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        story.append(Paragraph("Reporte de Movimientos", styles["Title"]))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph("Funcionalidad en desarrollo", styles["Normal"]))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    @staticmethod
    def generate_growth_report(_data: dict) -> bytes:
        """
        Genera reporte PDF de crecimiento.

        Args:
            data: Datos del reporte del caso de uso

        Returns:
            bytes: Contenido del PDF generado
        """
        # Implementación básica - se puede mejorar después
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        story.append(Paragraph("Reporte de Crecimiento", styles["Title"]))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph("Funcionalidad en desarrollo", styles["Normal"]))

        doc.build(story)
        buffer.seek(0)
        return buffer.read()
