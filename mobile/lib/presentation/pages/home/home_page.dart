/// Home Page - Template
///
/// Dashboard principal con estadísticas y accesos rápidos.
/// Single Responsibility: Orquestar componentes de la pantalla home.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_spacing.dart';
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
            // Header con gradiente y sincronización
            const SliverToBoxAdapter(child: HomeHeader()),

            // Contenido principal con padding
            SliverPadding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  const SizedBox(height: AppSpacing.md),

                  // Título de sección
                  _buildSectionTitle(context, 'Accesos Rápidos'),

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
    return Text(
      title,
      style: Theme.of(
        context,
      ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
    );
  }
}
