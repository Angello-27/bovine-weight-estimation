/// Capture Page - Template
///
/// US-001: Captura Continua de Fotogramas
///
/// Pantalla refactorizada con Atomic Design + SOLID.
/// Single Responsibility: Orquestar componentes de captura.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';
import 'widgets/capture_action_button.dart';
import 'widgets/capture_content.dart';
import 'widgets/capture_status_card.dart';

/// Pantalla de captura de fotogramas
///
/// Usa composición de componentes siguiendo Atomic Design:
/// - Organisms: CaptureStatusCard, CaptureContent
/// - Molecules: CaptureActionButton
class CapturePage extends StatelessWidget {
  const CapturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Captura de Fotogramas')),
      body: Consumer<CaptureProvider>(
        builder: (context, provider, child) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Estado actual
                  CaptureStatusCard(provider: provider),

                  const SizedBox(height: AppSpacing.lg),

                  // Contenido principal (scrollable)
                  Expanded(child: CaptureContent(provider: provider)),

                  const SizedBox(height: AppSpacing.md),

                  // Botón de acción
                  CaptureActionButton(provider: provider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
