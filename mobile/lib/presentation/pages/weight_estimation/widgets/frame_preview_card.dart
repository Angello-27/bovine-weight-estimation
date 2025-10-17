/// Widget: FramePreviewCard
///
/// Card con preview de la imagen del fotograma.
/// Single Responsibility: Mostrar preview con placeholder de error.
///
/// Page-specific Widget (Weight Estimation)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

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
        child: Image.asset(
          imagePath,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) {
            return Container(
              color: AppColors.grey300,
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.image,
                    size: AppSpacing.iconSizeXXLarge,
                    color: AppColors.grey500,
                  ),
                  SizedBox(height: AppSpacing.sm),
                  Text(
                    'Fotograma seleccionado',
                    style: TextStyle(
                      color: AppColors.grey600,
                      fontSize: AppSpacing.fontSizeMedium,
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
