/// Molecule: WeightRecordCard
///
/// Card de registro de peso con información de pesaje.
/// Single Responsibility: Mostrar un registro individual de peso.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Tarjeta de registro de peso individual
class WeightRecordCard extends StatelessWidget {
  /// Peso estimado en kg
  final double weight;

  /// Fecha y hora del pesaje
  final DateTime timestamp;

  /// Confidence score (0.0 - 1.0)
  final double confidence;

  /// Método de estimación (ia, manual, bascula)
  final String method;

  /// Coordenadas GPS (opcional)
  final String? gpsCoordinates;

  /// Callback al tocar
  final VoidCallback? onTap;

  const WeightRecordCard({
    required this.weight,
    required this.timestamp,
    required this.confidence,
    required this.method,
    this.gpsCoordinates,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationLow,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        side: BorderSide(
          color: _getConfidenceColor().withValues(alpha: 0.3),
          width: 1.5,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.md),
          child: Row(
            children: [
              // Peso con ícono
              _buildWeightSection(context),
              const SizedBox(width: AppSpacing.md),

              // Información del pesaje
              Expanded(child: _buildInfoSection(context)),

              // Indicador de confianza
              _buildConfidenceBadge(context),
            ],
          ),
        ),
      ),
    );
  }

  /// Sección de peso
  Widget _buildWeightSection(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        gradient: AppColors.primaryGradient,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Column(
        children: [
          const Icon(
            Icons.monitor_weight,
            color: Colors.white,
            size: AppSpacing.iconSizeLarge,
          ),
          const SizedBox(height: 4),
          Text(
            '${weight.toStringAsFixed(1)}',
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
          Text(
            'kg',
            style: Theme.of(
              context,
            ).textTheme.bodySmall?.copyWith(color: Colors.white70),
          ),
        ],
      ),
    );
  }

  /// Sección de información
  Widget _buildInfoSection(BuildContext context) {
    final dateFormatter = DateFormat('dd/MM/yyyy HH:mm');

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Fecha y hora
        Row(
          children: [
            const Icon(
              Icons.calendar_today,
              size: AppSpacing.iconSizeSmall,
              color: AppColors.grey600,
            ),
            const SizedBox(width: 4),
            Text(
              dateFormatter.format(timestamp),
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.grey900,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.xs),

        // Método
        Row(
          children: [
            Icon(
              _getMethodIcon(),
              size: AppSpacing.iconSizeSmall,
              color: AppColors.secondary,
            ),
            const SizedBox(width: 4),
            Text(
              _getMethodLabel(),
              style: Theme.of(
                context,
              ).textTheme.bodySmall?.copyWith(color: AppColors.grey700),
            ),
          ],
        ),

        // GPS (si existe)
        if (gpsCoordinates != null) ...[
          const SizedBox(height: AppSpacing.xs),
          Row(
            children: [
              const Icon(
                Icons.location_on,
                size: AppSpacing.iconSizeSmall,
                color: AppColors.info,
              ),
              const SizedBox(width: 4),
              Expanded(
                child: Text(
                  gpsCoordinates!,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppColors.grey600,
                    fontSize: 10,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ],
      ],
    );
  }

  /// Badge de confianza
  Widget _buildConfidenceBadge(BuildContext context) {
    final color = _getConfidenceColor();
    final percentage = (confidence * 100).toStringAsFixed(0);

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.sm,
        vertical: AppSpacing.xs,
      ),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusSmall),
        border: Border.all(color: color, width: 1),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(_getConfidenceIcon(), color: color, size: AppSpacing.iconSize),
          const SizedBox(height: 2),
          Text(
            '$percentage%',
            style: Theme.of(context).textTheme.labelSmall?.copyWith(
              color: color,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  /// Color según confidence (>90% verde, 80-90% ámbar, <80% rojo)
  Color _getConfidenceColor() {
    if (confidence >= 0.90) return AppColors.success;
    if (confidence >= 0.80) return AppColors.warning;
    return AppColors.error;
  }

  /// Ícono según nivel de confianza
  IconData _getConfidenceIcon() {
    if (confidence >= 0.90) return Icons.check_circle;
    if (confidence >= 0.80) return Icons.warning_amber;
    return Icons.error;
  }

  /// Etiqueta del método
  String _getMethodLabel() {
    switch (method.toLowerCase()) {
      case 'ia':
      case 'tflite':
        return 'Estimación IA';
      case 'manual':
        return 'Manual';
      case 'bascula':
      case 'scale':
        return 'Báscula';
      default:
        return method;
    }
  }

  /// Ícono del método
  IconData _getMethodIcon() {
    switch (method.toLowerCase()) {
      case 'ia':
      case 'tflite':
        return Icons.psychology;
      case 'manual':
        return Icons.edit;
      case 'bascula':
      case 'scale':
        return Icons.scale;
      default:
        return Icons.help_outline;
    }
  }
}
