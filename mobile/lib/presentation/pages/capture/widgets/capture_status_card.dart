/// Capture Status Card - Organism
///
/// Muestra el estado actual de la captura con información detallada.
/// Atomic Design: Organism (componente complejo con estado del provider)
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../providers/capture_provider.dart';
import '../../../widgets/molecules/cards/status_card.dart';

/// Card de estado de captura
class CaptureStatusCard extends StatelessWidget {
  /// Provider de capture
  final CaptureProvider provider;

  const CaptureStatusCard({required this.provider, super.key});

  @override
  Widget build(BuildContext context) {
    return StatusCard(
      icon: provider.state.icon,
      iconColor: provider.state.color,
      title: provider.state.title,
      description: provider.state.description,
    );
  }
}
