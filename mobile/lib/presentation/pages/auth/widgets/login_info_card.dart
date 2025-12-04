/// Login Info Card - Molecule
///
/// Card informativa en la página de login.
/// Atomic Design: Molecule
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../l10n/app_localizations.dart';
import '../../../widgets/molecules/cards/info_card.dart';

/// Card informativa del login
class LoginInfoCard extends StatelessWidget {
  const LoginInfoCard({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return InfoCard(
      title: l10n.appName,
      description: l10n.appDescription,
      icon: Icons.info_outline,
      // Usar colores del tema para adaptarse a tema claro/oscuro
      color: colorScheme.primary,
      backgroundColor: colorScheme.primaryContainer.withValues(alpha: 0.3),
    );
  }
}
