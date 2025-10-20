/// Molecule: CattleCard
///
/// Card de animal bovino con foto, información básica y último peso.
/// Single Responsibility: Mostrar datos de un animal en formato card.
///
/// Presentation Layer - Molecules (UI Design System)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Tarjeta de ganado bovino
///
/// Componente según especificación en:
/// docs/design/ui-design-system.md (Líneas 482-596)
class CattleCard extends StatelessWidget {
  /// Nombre del animal
  final String name;

  /// Número de caravana/arete
  final String earTag;

  /// Raza del animal (una de las 7)
  final String breed;

  /// URL o path de la foto del animal
  final String? photoUrl;

  /// Último peso registrado en kg
  final double? lastWeight;

  /// Callback al tocar la card
  final VoidCallback? onTap;

  /// Color opcional para el borde de la raza
  final Color? breedColor;

  const CattleCard({
    required this.name,
    required this.earTag,
    required this.breed,
    this.photoUrl,
    this.lastWeight,
    this.onTap,
    this.breedColor,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.cardPadding),
          child: Row(
            children: [
              // Foto del animal (circular)
              _buildAvatar(),
              const SizedBox(width: AppSpacing.md),

              // Información del animal
              Expanded(child: _buildInfo(context)),

              // Último peso (si existe)
              if (lastWeight != null) _buildWeight(context),
            ],
          ),
        ),
      ),
    );
  }

  /// Avatar circular del animal
  Widget _buildAvatar() {
    return Hero(
      tag: 'cattle_$earTag',
      child: CircleAvatar(
        radius: 32,
        backgroundImage: photoUrl != null && photoUrl!.isNotEmpty
            ? (photoUrl!.startsWith('http')
                      ? NetworkImage(photoUrl!)
                      : FileImage(photoUrl! as dynamic))
                  as ImageProvider
            : null,
        backgroundColor: AppColors.primaryLight.withValues(alpha: 0.3),
        child: photoUrl == null || photoUrl!.isEmpty
            ? const Icon(Icons.pets, size: 32, color: AppColors.primary)
            : null,
      ),
    );
  }

  /// Información del animal
  Widget _buildInfo(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Nombre del animal
        Text(
          name,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
            color: AppColors.grey900,
          ),
          overflow: TextOverflow.ellipsis,
          maxLines: 1,
        ),
        const SizedBox(height: AppSpacing.xs),

        // Caravana
        Text(
          'Caravana: $earTag',
          style: Theme.of(
            context,
          ).textTheme.bodySmall?.copyWith(color: AppColors.grey600),
        ),
        const SizedBox(height: AppSpacing.xs),

        // Raza con ícono
        Row(
          children: [
            Icon(
              Icons.category,
              size: AppSpacing.iconSizeSmall,
              color: breedColor ?? AppColors.secondary,
            ),
            const SizedBox(width: 4),
            Flexible(
              child: Text(
                breed,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: AppColors.grey700,
                  fontWeight: FontWeight.w500,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
      ],
    );
  }

  /// Widget del último peso
  Widget _buildWeight(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.sm,
        vertical: AppSpacing.xs,
      ),
      decoration: BoxDecoration(
        gradient: AppColors.primaryGradient,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Ícono de peso
          const Icon(
            Icons.monitor_weight,
            color: Colors.white,
            size: AppSpacing.iconSize,
          ),
          const SizedBox(height: 4),

          // Valor del peso
          Text(
            '${lastWeight!.toStringAsFixed(1)} kg',
            style: Theme.of(context).textTheme.titleSmall?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
