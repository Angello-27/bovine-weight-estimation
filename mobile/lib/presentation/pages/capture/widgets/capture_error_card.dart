/// Widget: CaptureErrorCard
///
/// Card con mensaje de error.
/// Single Responsibility: Mostrar error de captura.
///
/// Page-specific Widget
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Card de error de captura
class CaptureErrorCard extends StatelessWidget {
  final String errorMessage;

  const CaptureErrorCard({super.key, required this.errorMessage});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.error.withValues(alpha: 0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        child: Row(
          children: [
            const Icon(
              Icons.error,
              color: AppColors.error,
              size: AppSpacing.iconSizeLarge,
            ),

            const SizedBox(width: AppSpacing.md),

            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Error',
                    style: Theme.of(
                      context,
                    ).textTheme.titleMedium?.copyWith(color: AppColors.error),
                  ),

                  const SizedBox(height: AppSpacing.xs),

                  Text(
                    errorMessage,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
