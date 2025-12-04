/// Theme Toggle Button - Atom
///
/// Botón para cambiar entre tema claro y oscuro.
/// Atomic Design: Atom
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../domain/entities/app_settings.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/settings_provider.dart';

/// Botón para cambiar el tema
class ThemeToggleButton extends StatelessWidget {
  const ThemeToggleButton({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Consumer<SettingsProvider>(
      builder: (context, settingsProvider, _) {
        final themeMode = settingsProvider.settings.themeMode;
        final isDark =
            themeMode == AppThemeMode.dark ||
            (themeMode == AppThemeMode.system &&
                MediaQuery.of(context).platformBrightness == Brightness.dark);

        return IconButton(
          icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
          tooltip: isDark ? l10n.themeModeLight : l10n.themeModeDark,
          onPressed: () {
            // Cambiar entre claro y oscuro (ignorar sistema)
            final newMode = isDark ? AppThemeMode.light : AppThemeMode.dark;
            settingsProvider.updateThemeMode(newMode);
          },
        );
      },
    );
  }
}
