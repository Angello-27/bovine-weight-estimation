/// Widget: ExportOptionsBottomSheet
///
/// Bottom sheet con opciones de exportación (PDF/CSV).
/// Single Responsibility: Mostrar opciones de exportación.
///
/// Page-specific Widget (Weight History)
library;

import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:printing/printing.dart';

import '../../../../core/config/dependency_injection.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/usecases/export_csv_usecase.dart';
import '../../../../domain/usecases/export_pdf_usecase.dart';
import '../../../../l10n/app_localizations.dart';

/// Bottom sheet de opciones de exportación
class ExportOptionsBottomSheet extends StatelessWidget {
  /// ID del animal
  final String cattleId;

  /// Nombre del animal
  final String cattleName;

  const ExportOptionsBottomSheet({
    required this.cattleId,
    required this.cattleName,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            AppLocalizations.of(context)!.export,
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppSpacing.md),
          ListTile(
            leading: const Icon(Icons.picture_as_pdf, color: AppColors.error),
            title: Text(
              AppLocalizations.of(context)!.exportAsPdf,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            subtitle: Text(
              AppLocalizations.of(context)!.forPrinting,
              style: Theme.of(context).textTheme.bodySmall,
            ),
            onTap: () {
              Navigator.pop(context);
              _exportPdf(context);
            },
          ),
          ListTile(
            leading: const Icon(Icons.table_chart, color: AppColors.success),
            title: Text(
              AppLocalizations.of(context)!.exportAsCsv,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            subtitle: Text(
              AppLocalizations.of(context)!.forExcelAnalysis,
              style: Theme.of(context).textTheme.bodySmall,
            ),
            onTap: () {
              Navigator.pop(context);
              _exportCsv(context);
            },
          ),
        ],
      ),
    );
  }

  /// Exportar a PDF
  Future<void> _exportPdf(BuildContext context) async {
    try {
      // Mostrar loading
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              ),
              const SizedBox(width: 12),
              Text(AppLocalizations.of(context)!.generatingPdf(cattleName)),
            ],
          ),
          backgroundColor: AppColors.info,
          duration: const Duration(seconds: 2),
        ),
      );

      // Obtener use case desde DI
      final di = DependencyInjection();
      final exportPdfUseCase = di.exportPdfUseCase;

      // Generar PDF
      final params = ExportPdfParams(cattleId: cattleId);
      final result = await exportPdfUseCase(params);

      result.fold(
        (failure) {
          if (!context.mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${failure.message}'),
              backgroundColor: AppColors.error,
            ),
          );
        },
        (pdfBytes) async {
          // Mostrar opciones de compartir/imprimir
          if (!context.mounted) return;
          await _showPdfOptions(context, pdfBytes);
        },
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error inesperado: ${e.toString()}'),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }

  /// Exportar a CSV
  Future<void> _exportCsv(BuildContext context) async {
    try {
      // Mostrar loading
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              ),
              const SizedBox(width: 12),
              Text(AppLocalizations.of(context)!.generatingCsv(cattleName)),
            ],
          ),
          backgroundColor: AppColors.success,
          duration: const Duration(seconds: 2),
        ),
      );

      // Obtener use case desde DI
      final di = DependencyInjection();
      final exportCsvUseCase = di.exportCsvUseCase;

      // Generar CSV
      final params = ExportCsvParams(cattleId: cattleId);
      final result = await exportCsvUseCase(params);

      result.fold(
        (failure) {
          if (!context.mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error: ${failure.message}'),
              backgroundColor: AppColors.error,
            ),
          );
        },
        (csvContent) async {
          // Guardar y compartir archivo CSV
          await _shareCsvFile(context, csvContent);
        },
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error inesperado: ${e.toString()}'),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }

  /// Muestra opciones para el PDF generado
  Future<void> _showPdfOptions(BuildContext context, List<int> pdfBytes) async {
    if (!context.mounted) return;

    await showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(AppSpacing.borderRadiusLarge),
        ),
      ),
      builder: (context) => Container(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('PDF Generado', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: AppSpacing.md),
            ListTile(
              leading: const Icon(Icons.share, color: AppColors.info),
              title: Text(
                'Compartir',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              subtitle: Text(
                'Enviar por WhatsApp, Email, etc.',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              onTap: () async {
                Navigator.pop(context);
                await _sharePdfFile(context, pdfBytes);
              },
            ),
            ListTile(
              leading: const Icon(Icons.print, color: AppColors.secondary),
              title: Text(
                'Imprimir',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              subtitle: Text(
                'Enviar a impresora',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              onTap: () async {
                Navigator.pop(context);
                await _printPdf(context, pdfBytes);
              },
            ),
            ListTile(
              leading: const Icon(Icons.preview, color: AppColors.primary),
              title: Text(
                'Vista Previa',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
              subtitle: Text(
                'Ver antes de compartir',
                style: Theme.of(context).textTheme.bodySmall,
              ),
              onTap: () {
                Navigator.pop(context);
                _previewPdf(context, pdfBytes);
              },
            ),
          ],
        ),
      ),
    );
  }

  /// Compartir archivo PDF
  Future<void> _sharePdfFile(BuildContext context, List<int> pdfBytes) async {
    try {
      // Obtener directorio temporal
      final tempDir = await getTemporaryDirectory();
      final fileName = 'historial_${cattleName.replaceAll(' ', '_')}.pdf';
      final file = File('${tempDir.path}/$fileName');

      // Escribir bytes al archivo
      await file.writeAsBytes(pdfBytes);

      // Compartir archivo usando Printing
      final uint8listBytes = Uint8List.fromList(pdfBytes);
      await Printing.sharePdf(bytes: uint8listBytes, filename: fileName);

      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(AppLocalizations.of(context)!.pdfSharedSuccessfully),
          backgroundColor: AppColors.success,
        ),
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            AppLocalizations.of(context)!.errorSharingPdf(e.toString()),
          ),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }

  /// Imprimir PDF
  Future<void> _printPdf(BuildContext context, List<int> pdfBytes) async {
    try {
      final uint8listBytes = Uint8List.fromList(pdfBytes);
      await Printing.layoutPdf(
        onLayout: (format) async => uint8listBytes,
        name: 'historial_${cattleName.replaceAll(' ', '_')}.pdf',
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            AppLocalizations.of(context)!.errorPrintingPdf(e.toString()),
          ),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }

  /// Vista previa del PDF
  Future<void> _previewPdf(BuildContext context, List<int> pdfBytes) async {
    try {
      final uint8listBytes = Uint8List.fromList(pdfBytes);
      await Printing.sharePdf(
        bytes: uint8listBytes,
        filename: 'historial_${cattleName.replaceAll(' ', '_')}.pdf',
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            AppLocalizations.of(context)!.errorShowingPdf(e.toString()),
          ),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }

  /// Compartir archivo CSV
  Future<void> _shareCsvFile(BuildContext context, String csvContent) async {
    try {
      // Obtener directorio temporal
      final tempDir = await getTemporaryDirectory();
      final fileName = 'historial_${cattleName.replaceAll(' ', '_')}.csv';
      final file = File('${tempDir.path}/$fileName');

      // Escribir contenido CSV al archivo
      await file.writeAsString(csvContent);

      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(AppLocalizations.of(context)!.csvSavedAt(file.path)),
          backgroundColor: AppColors.success,
          duration: const Duration(seconds: 4),
          action: SnackBarAction(
            label: 'OK',
            textColor: Colors.white,
            onPressed: () {},
          ),
        ),
      );
    } catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            AppLocalizations.of(context)!.errorSharingCsv(e.toString()),
          ),
          backgroundColor: AppColors.error,
        ),
      );
    }
  }
}
