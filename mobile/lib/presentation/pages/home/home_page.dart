/// Home Page - Template
///
/// Dashboard principal con estadísticas y accesos rápidos.
/// Single Responsibility: Orquestar componentes de la pantalla home.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../l10n/app_localizations.dart';
import 'widgets/home_footer.dart';
import 'widgets/home_header.dart';
import 'widgets/home_quick_actions.dart';

/// Pantalla de inicio con dashboard moderno
///
/// Usa composición de componentes siguiendo Atomic Design:
/// - Organisms: HomeHeader, HomeStats, HomeQuickActions
/// - Molecules: HomeFooter
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            // Header con sincronización
            const SliverToBoxAdapter(child: HomeHeader()),

            // Contenido principal con padding
            SliverPadding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  const SizedBox(height: AppSpacing.md),

                  // Título de sección
                  _buildSectionTitle(
                    context,
                    AppLocalizations.of(context)!.quickAccess,
                  ),

                  const SizedBox(height: AppSpacing.md),

                  // Grid de acciones rápidas
                  const HomeQuickActions(),

                  const SizedBox(height: AppSpacing.xl),

                  // Footer con información
                  const HomeFooter(),
                ]),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Construye el título de una sección
  Widget _buildSectionTitle(BuildContext context, String title) {
    return Row(
      children: [
        Container(
          width: 4,
          height: 24,
          decoration: BoxDecoration(
            color: AppColors.primary,
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        Text(
          title,
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            fontWeight: FontWeight.bold,
            color: Theme.of(context).colorScheme.onSurface,
          ),
        ),
      ],
    );
  }
}
