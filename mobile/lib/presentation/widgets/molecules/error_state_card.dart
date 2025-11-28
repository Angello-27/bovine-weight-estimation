/// Molecule: ErrorStateCard
///
/// Card de estado de error con mensaje y botón de reintento.
/// Single Responsibility: Mostrar estado de error consistente.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../l10n/app_localizations.dart';

/// Card de estado de error
class ErrorStateCard extends StatelessWidget {
  /// Título del error
  final String title;

  /// Mensaje de error
  final String message;

  /// Callback al presionar reintentar
  final VoidCallback? onRetry;

  const ErrorStateCard({
    required this.title,
    required this.message,
    this.onRetry,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.screenPadding),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(
                Icons.error_outline,
                size: AppSpacing.iconSizeXXLarge,
                color: AppColors.error,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                title,
                style: Theme.of(context).textTheme.titleLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(
                message,
                style: Theme.of(
                  context,
                ).textTheme.bodyMedium?.copyWith(color: AppColors.grey600),
                textAlign: TextAlign.center,
              ),
              if (onRetry != null) ...[
                const SizedBox(height: AppSpacing.lg),
                ElevatedButton.icon(
                  onPressed: onRetry,
                  icon: const Icon(Icons.refresh),
                  label: Text(AppLocalizations.of(context)!.retry),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
