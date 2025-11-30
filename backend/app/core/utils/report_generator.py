"""
Report Generator - Core Layer (Facade)
Facade para generar reportes en diferentes formatos

Single Responsibility: Coordinar la generación de reportes delegando a generadores especializados
"""

from .excel_generator import ExcelGenerator
from .pdf_generator import PDFGenerator


class ReportGenerator:
    """
    Facade para generadores de reportes.

    Delega la generación a generadores especializados (PDF, Excel).
    """

    @staticmethod
    def generate_pdf(data: dict, report_type: str) -> bytes:
        """
        Genera reporte en formato PDF.

        Args:
            data: Datos del reporte
            report_type: Tipo de reporte (traceability, inventory, movements, growth)

        Returns:
            Bytes del archivo PDF
        """
        if report_type == "traceability":
            return PDFGenerator.generate_traceability_report(data)
        if report_type == "inventory":
            return PDFGenerator.generate_inventory_report(data)
        if report_type == "movements":
            return PDFGenerator.generate_movements_report(data)
        if report_type == "growth":
            return PDFGenerator.generate_growth_report(data)
        raise ValueError(f"Tipo de reporte no soportado: {report_type}")

    @staticmethod
    def generate_excel(data: dict, report_type: str) -> bytes:
        """
        Genera reporte en formato Excel.

        Args:
            data: Datos del reporte
            report_type: Tipo de reporte (traceability, inventory, movements, growth)

        Returns:
            Bytes del archivo Excel
        """
        if report_type == "traceability":
            return ExcelGenerator.generate_traceability_report(data)
        if report_type == "inventory":
            return ExcelGenerator.generate_inventory_report(data)
        if report_type == "movements":
            return ExcelGenerator.generate_movements_report(data)
        if report_type == "growth":
            return ExcelGenerator.generate_growth_report(data)
        raise ValueError(f"Tipo de reporte no soportado: {report_type}")
