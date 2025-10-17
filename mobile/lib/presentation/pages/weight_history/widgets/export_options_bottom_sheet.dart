/// Widget: ExportOptionsBottomSheet
///
/// Bottom sheet con opciones de exportación (PDF/CSV).
/// Single Responsibility: Mostrar opciones de exportación.
///
/// Page-specific Widget (Weight History)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

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
            'Exportar Historial',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: AppSpacing.md),
          ListTile(
            leading: const Icon(Icons.picture_as_pdf, color: AppColors.error),
            title: const Text('Exportar como PDF'),
            subtitle: const Text('Documento profesional con gráficos'),
            onTap: () {
              Navigator.pop(context);
              _exportPdf(context);
            },
          ),
          ListTile(
            leading: const Icon(Icons.table_chart, color: AppColors.success),
            title: const Text('Exportar como CSV'),
            subtitle: const Text('Para análisis en Excel'),
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
    // TODO: Implementar exportación PDF
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Exportando historial de $cattleName a PDF...'),
        backgroundColor: AppColors.info,
      ),
    );
  }

  /// Exportar a CSV
  Future<void> _exportCsv(BuildContext context) async {
    // TODO: Implementar exportación CSV
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Exportando historial de $cattleName a CSV...'),
        backgroundColor: AppColors.success,
      ),
    );
  }
}
