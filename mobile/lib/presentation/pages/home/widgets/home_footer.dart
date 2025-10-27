/// Home Footer - Molecule
///
/// Footer con información del propietario y créditos.
/// Atomic Design: Molecule
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../core/config/app_config.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Footer informativo del home
class HomeFooter extends StatelessWidget {
  const HomeFooter({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: [
          Text(
            AppConfig.ownerName,
            style: TextStyle(
              fontSize: AppSpacing.fontSizeSmall,
              color: AppColors.grey600,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            AppConfig.location,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: AppSpacing.fontSizeSmall,
              color: AppColors.grey500,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          _buildUniversityBadge(),
        ],
      ),
    );
  }

  Widget _buildUniversityBadge() {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        color: AppColors.infoLight,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: const Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.school,
            size: AppSpacing.iconSizeSmall,
            color: AppColors.info,
          ),
          SizedBox(width: AppSpacing.sm),
          Text(
            'Taller de Grado - UAGRM',
            style: TextStyle(
              fontSize: AppSpacing.fontSizeSmall,
              color: AppColors.info,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

