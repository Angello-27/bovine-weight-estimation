/// Page: HomePage
/// 
/// Pantalla de inicio de la aplicación.
/// Single Responsibility: Mostrar opciones principales de navegación.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';

import '../../../core/config/app_config.dart';
import '../../../core/routes/app_router.dart';
import '../../../core/ui/theme/app_colors.dart';
import '../../../core/ui/theme/app_spacing.dart';

/// Pantalla de inicio
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppConfig.haciendaName),
      ),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.screenPadding),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo/Icono
                const Icon(
                  Icons.pets,
                  size: 100,
                  color: AppColors.primary,
                ),

                const SizedBox(height: AppSpacing.lg),

                // Título
                const Text(
                  'Sistema de Estimación\nde Peso Bovino',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                const SizedBox(height: AppSpacing.sm),

                // Subtítulo
                Text(
                  AppConfig.haciendaName,
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.grey[600],
                  ),
                ),

                const SizedBox(height: AppSpacing.xxl),

                // Botón US-001
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      AppRouter.push(context, AppRoutes.capture);
                    },
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('Capturar Fotogramas (US-001)'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 56),
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.md),

                // Botón US-002 (Demo directo)
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: () {
                      AppRouter.push(
                        context,
                        AppRoutes.weightEstimation,
                        arguments: {
                          'framePath': '/mock/frame.jpg',
                          'cattleId': null,
                        },
                      );
                    },
                    icon: const Icon(Icons.monitor_weight),
                    label: const Text('Estimar Peso con IA (US-002)'),
                    style: OutlinedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 56),
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.md),

                // Placeholder para funcionalidades futuras
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.cardPadding),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Próximamente:',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                        const SizedBox(height: AppSpacing.sm),
                        _buildFeatureTile(
                          Icons.check_circle_outline,
                          'Selección de mejor fotograma (US-002)',
                        ),
                        _buildFeatureTile(
                          Icons.monitor_weight,
                          'Estimación de peso con IA (US-003)',
                        ),
                        _buildFeatureTile(
                          Icons.analytics,
                          'Análisis histórico (US-004)',
                        ),
                        _buildFeatureTile(
                          Icons.sync,
                          'Sincronización (US-005)',
                        ),
                        _buildFeatureTile(
                          Icons.search,
                          'Búsqueda avanzada (US-006)',
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Información del cliente
                Text(
                  '${AppConfig.ownerName}\n${AppConfig.location}',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[500],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Widget de feature tile
  Widget _buildFeatureTile(IconData icon, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
      child: Row(
        children: [
          Icon(
            icon,
            size: 20,
            color: Colors.grey[600],
          ),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[700],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

