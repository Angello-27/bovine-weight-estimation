/// Page: HomePage
///
/// Dashboard moderno con estadísticas y accesos rápidos.
/// Single Responsibility: Mostrar resumen del sistema y navegación principal.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/config/app_config.dart';
import '../../../core/routes/app_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/sync_provider.dart';
import '../../widgets/molecules/action_tile.dart';
import 'widgets/home_stat_card.dart';

/// Pantalla de inicio con dashboard moderno
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Header con gradiente (moderno)
            SliverToBoxAdapter(
              child: Container(
                decoration: const BoxDecoration(
                  gradient: AppColors.primaryGradient,
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(AppSpacing.borderRadiusXLarge),
                    bottomRight: Radius.circular(AppSpacing.borderRadiusXLarge),
                  ),
                ),
                padding: const EdgeInsets.all(AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Título con logo + indicador de sincronización
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.sm),
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(
                              AppSpacing.borderRadiusMedium,
                            ),
                          ),
                          child: const Icon(
                            Icons.pets,
                            color: Colors.white,
                            size: AppSpacing.iconSizeLarge,
                          ),
                        ),
                        const SizedBox(width: AppSpacing.md),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Agrocom',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: AppSpacing.fontSizeLarge,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                AppConfig.haciendaName,
                                style: TextStyle(
                                  color: Colors.white.withValues(alpha: 0.9),
                                  fontSize: AppSpacing.fontSizeMedium,
                                ),
                              ),
                            ],
                          ),
                        ),
                        // Indicador de sincronización (US-005)
                        Consumer<SyncProvider>(
                          builder: (context, syncProvider, _) {
                            return GestureDetector(
                              onTap: () =>
                                  Navigator.pushNamed(context, AppRoutes.sync),
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: AppSpacing.sm,
                                  vertical: AppSpacing.xs,
                                ),
                                decoration: BoxDecoration(
                                  color: Colors.white.withValues(alpha: 0.2),
                                  borderRadius: BorderRadius.circular(
                                    AppSpacing.borderRadiusLarge,
                                  ),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(
                                      syncProvider.isSyncing
                                          ? Icons.sync_rounded
                                          : syncProvider.isOffline
                                          ? Icons.cloud_off_rounded
                                          : Icons.cloud_done_rounded,
                                      color: Colors.white,
                                      size: 16,
                                    ),
                                    if (syncProvider.hasPendingItems) ...[
                                      const SizedBox(width: 4),
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 6,
                                          vertical: 2,
                                        ),
                                        decoration: BoxDecoration(
                                          color: Colors.amber.shade600,
                                          borderRadius: BorderRadius.circular(
                                            10,
                                          ),
                                        ),
                                        child: Text(
                                          '${syncProvider.pendingCount}',
                                          style: const TextStyle(
                                            color: Colors.white,
                                            fontSize: 10,
                                            fontWeight: FontWeight.w600,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      ],
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Estadísticas rápidas (mock data)
                    const Row(
                      children: [
                        Expanded(
                          child: HomeStatCard(
                            icon: Icons.pets,
                            value: '500',
                            label: 'Animales',
                          ),
                        ),
                        SizedBox(width: AppSpacing.sm),
                        Expanded(
                          child: HomeStatCard(
                            icon: Icons.monitor_weight,
                            value: '450 kg',
                            label: 'Peso Prom.',
                          ),
                        ),
                        SizedBox(width: AppSpacing.sm),
                        Expanded(
                          child: HomeStatCard(
                            icon: Icons.category,
                            value: '7',
                            label: 'Razas',
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            // Contenido principal
            SliverPadding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  const SizedBox(height: AppSpacing.sm),

                  // Título sección
                  Text(
                    'Accesos Rápidos',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: AppSpacing.md),

                  // Grid de acciones (moderno)
                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 2,
                    mainAxisSpacing: AppSpacing.md,
                    crossAxisSpacing: AppSpacing.md,
                    childAspectRatio: 1.2,
                    children: [
                      ActionTile(
                        icon: Icons.camera_alt,
                        title: 'Capturar',
                        subtitle: 'Fotogramas',
                        gradient: AppColors.primaryGradient,
                        onTap: () => AppRouter.push(context, AppRoutes.capture),
                      ),
                      ActionTile(
                        icon: Icons.monitor_weight,
                        title: 'Estimar',
                        subtitle: 'Peso IA',
                        gradient: AppColors.secondaryGradient,
                        onTap: () => AppRouter.push(
                          context,
                          AppRoutes.weightEstimation,
                          arguments: {
                            'framePath': '/mock/frame.jpg',
                            'cattleId': null,
                          },
                        ),
                      ),
                      ActionTile(
                        icon: Icons.add_circle,
                        title: 'Registrar',
                        subtitle: 'Animal',
                        gradient: AppColors.accentGradient,
                        onTap: () => AppRouter.push(
                          context,
                          AppRoutes.cattleRegistration,
                        ),
                      ),
                      const ActionTile(
                        icon: Icons.more_horiz,
                        title: 'Próximamente',
                        subtitle: 'Más funciones',
                        gradient: LinearGradient(
                          colors: [AppColors.grey300, AppColors.grey400],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: AppSpacing.xl),

                  // Info footer
                  Center(
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
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: AppSpacing.md,
                            vertical: AppSpacing.sm,
                          ),
                          decoration: BoxDecoration(
                            color: AppColors.infoLight,
                            borderRadius: BorderRadius.circular(
                              AppSpacing.borderRadiusLarge,
                            ),
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
                        ),
                      ],
                    ),
                  ),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
