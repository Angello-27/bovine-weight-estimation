/// Page: WeightHistoryPage
///
/// US-004: Historial de Pesajes con Gráficos de Evolución
///
/// Pantalla para visualizar historial completo de peso de un animal.
/// Single Responsibility: Coordinar visualización de historial.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/weight_history_provider.dart';
import '../../widgets/molecules/empty_state_card.dart';
import '../../widgets/molecules/error_state_card.dart';
import '../../widgets/molecules/loading_state_card.dart';
import 'widgets/export_options_bottom_sheet.dart';
import 'widgets/period_filter_chips.dart';
import 'widgets/weight_history_chart.dart';
import 'widgets/weight_history_list.dart';
import 'widgets/weight_history_stats_panel.dart';

/// Pantalla de historial de pesajes
class WeightHistoryPage extends StatefulWidget {
  /// ID del animal
  final String cattleId;

  /// Nombre del animal (para título)
  final String cattleName;

  const WeightHistoryPage({
    required this.cattleId,
    required this.cattleName,
    super.key,
  });

  @override
  State<WeightHistoryPage> createState() => _WeightHistoryPageState();
}

class _WeightHistoryPageState extends State<WeightHistoryPage> {
  @override
  void initState() {
    super.initState();
    // Cargar historial al iniciar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<WeightHistoryProvider>().loadHistory(widget.cattleId);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.grey50,
      appBar: AppBar(
        title: Text('Historial - ${widget.cattleName}'),
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: AppColors.secondaryGradient,
          ),
        ),
        actions: [
          // Botón de exportación
          IconButton(
            icon: const Icon(Icons.file_download),
            onPressed: () {
              showModalBottomSheet(
                context: context,
                shape: const RoundedRectangleBorder(
                  borderRadius: BorderRadius.vertical(
                    top: Radius.circular(AppSpacing.borderRadiusLarge),
                  ),
                ),
                builder: (context) => ExportOptionsBottomSheet(
                  cattleId: widget.cattleId,
                  cattleName: widget.cattleName,
                ),
              );
            },
            tooltip: 'Exportar',
          ),
        ],
      ),
      body: Consumer<WeightHistoryProvider>(
        builder: (context, provider, child) {
          // Loading state
          if (provider.isLoading) {
            return const LoadingStateCard(
              message: 'Cargando historial...',
              color: AppColors.secondary,
            );
          }

          // Error state
          if (provider.hasError) {
            return ErrorStateCard(
              title: 'Error al cargar historial',
              message: provider.errorMessage ?? 'Error desconocido',
              onRetry: () => provider.loadHistory(widget.cattleId),
            );
          }

          // Empty state
          if (!provider.hasHistory) {
            return EmptyStateCard(
              icon: Icons.history,
              title: 'Sin pesajes registrados',
              message:
                  'Realiza la primera estimación de peso\npara ver el historial de ${widget.cattleName}',
            );
          }

          // Content
          return SafeArea(
            child: CustomScrollView(
              slivers: [
                // Panel de estadísticas
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.screenPadding),
                    child: WeightHistoryStatsPanel(history: provider.history!),
                  ),
                ),

                // Filtros de período
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.screenPadding,
                    ),
                    child: PeriodFilterChips(
                      selectedPeriod: provider.selectedPeriod,
                      onPeriodChanged: (period) {
                        provider.setPeriod(period);
                        provider.loadHistory(widget.cattleId);
                      },
                    ),
                  ),
                ),

                const SliverToBoxAdapter(
                  child: SizedBox(height: AppSpacing.md),
                ),

                // Gráfico de evolución
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.screenPadding,
                    ),
                    child: WeightHistoryChart(history: provider.history!),
                  ),
                ),

                const SliverToBoxAdapter(
                  child: SizedBox(height: AppSpacing.lg),
                ),

                // Lista de pesajes
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.screenPadding,
                    ),
                    child: Text(
                      'Historial Detallado',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),

                const SliverToBoxAdapter(
                  child: SizedBox(height: AppSpacing.sm),
                ),

                // Lista de pesajes
                SliverPadding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.screenPadding,
                  ),
                  sliver: WeightHistoryList(
                    weighings: provider.history!.weighings,
                  ),
                ),

                const SliverToBoxAdapter(
                  child: SizedBox(height: AppSpacing.xl),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
