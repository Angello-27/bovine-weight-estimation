/// Widget: FramePreviewCard
///
/// Card con preview de la imagen del fotograma.
/// Single Responsibility: Mostrar preview con placeholder de error.
///
/// Page-specific Widget (Weight Estimation)
library;

import 'dart:io';

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';

/// Card de preview de fotograma
class FramePreviewCard extends StatelessWidget {
  /// Path de la imagen
  final String imagePath;

  const FramePreviewCard({required this.imagePath, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      clipBehavior: Clip.antiAlias,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: AspectRatio(
        aspectRatio: 16 / 9,
        child: Image.file(
          File(imagePath),
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Container(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.image_not_supported_rounded,
                    size: AppSpacing.iconSizeXXLarge,
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    AppLocalizations.of(context)!.selectedFrame,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
