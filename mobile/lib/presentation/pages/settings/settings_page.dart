/// Settings Page
///
/// Página de configuración de preferencias del usuario.
/// Single Responsibility: Orquestar componentes de settings.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_spacing.dart';
import '../../../domain/entities/app_settings.dart';
import '../../../l10n/app_localizations.dart';
import '../../providers/settings_provider.dart';
import '../../widgets/molecules/app_bar_gradient.dart';
import 'widgets/settings_list_tile.dart';
import 'widgets/settings_section.dart';
import 'widgets/settings_switch_tile.dart';

/// Página de configuración
class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<SettingsProvider>(
      builder: (context, provider, _) {
        return Scaffold(
          appBar: AppBarGradient(title: AppLocalizations.of(context)!.settings),
          body:
              provider.isLoading &&
                  provider.settings == AppSettings.defaultSettings
              ? const Center(child: CircularProgressIndicator())
              : _buildSettingsContent(context, provider),
        );
      },
    );
  }

  /// Construye el contenido de settings factorizado
  Widget _buildSettingsContent(
    BuildContext context,
    SettingsProvider provider,
  ) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Sección: Apariencia
          _buildAppearanceSection(context, provider),

          const SizedBox(height: AppSpacing.lg),

          // Sección: Captura
          _buildCaptureSection(context, provider),

          const SizedBox(height: AppSpacing.lg),

          // Sección: Unidades y formato
          _buildUnitsSection(context, provider),

          const SizedBox(height: AppSpacing.lg),

          // Sección: Idioma
          _buildLanguageSection(context, provider),

          const SizedBox(height: AppSpacing.xl),
        ],
      ),
    );
  }

  /// Sección de apariencia
  Widget _buildAppearanceSection(
    BuildContext context,
    SettingsProvider provider,
  ) {
    final l10n = AppLocalizations.of(context)!;
    return SettingsSection(
      title: l10n.appearance,
      icon: Icons.palette_rounded,
      children: [
        SettingsListTile(
          title: l10n.theme,
          subtitle: _getThemeModeLabel(context, provider.settings.themeMode),
          icon: Icons.brightness_6_rounded,
          onTap: () => _showThemeModeDialog(context, provider),
        ),
        SettingsListTile(
          title: l10n.textSize,
          subtitle: _getTextSizeLabel(context, provider.settings.textSize),
          icon: Icons.text_fields_rounded,
          onTap: () => _showTextSizeDialog(context, provider),
        ),
      ],
    );
  }

  /// Sección de captura
  Widget _buildCaptureSection(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    return SettingsSection(
      title: l10n.capture,
      icon: Icons.camera_alt_rounded,
      children: [
        SettingsSwitchTile(
          title: l10n.autoFlash,
          subtitle: l10n.autoFlashSubtitle,
          icon: Icons.flash_on_rounded,
          value: provider.settings.flashEnabled,
          onChanged: (value) => provider.updateFlashEnabled(value),
        ),
      ],
    );
  }

  /// Sección de unidades y formato
  Widget _buildUnitsSection(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    return SettingsSection(
      title: l10n.unitsAndFormat,
      icon: Icons.tune_rounded,
      children: [
        SettingsListTile(
          title: l10n.weightUnit,
          subtitle: _getWeightUnitLabel(context, provider.settings.weightUnit),
          icon: Icons.scale_rounded,
          onTap: () => _showWeightUnitDialog(context, provider),
        ),
        SettingsListTile(
          title: l10n.dateFormat,
          subtitle: _getDateFormatLabel(context, provider.settings.dateFormat),
          icon: Icons.calendar_today_rounded,
          onTap: () => _showDateFormatDialog(context, provider),
        ),
      ],
    );
  }

  /// Sección de idioma
  Widget _buildLanguageSection(
    BuildContext context,
    SettingsProvider provider,
  ) {
    final l10n = AppLocalizations.of(context)!;
    return SettingsSection(
      title: l10n.language,
      icon: Icons.language_rounded,
      children: [
        SettingsListTile(
          title: l10n.interfaceLanguage,
          subtitle: _getLanguageLabel(context, provider.settings.language),
          icon: Icons.translate_rounded,
          onTap: () => _showLanguageDialog(context, provider),
        ),
      ],
    );
  }

  String _getThemeModeLabel(BuildContext context, AppThemeMode mode) {
    final l10n = AppLocalizations.of(context)!;
    switch (mode) {
      case AppThemeMode.system:
        return l10n.themeModeSystem;
      case AppThemeMode.light:
        return l10n.themeModeLight;
      case AppThemeMode.dark:
        return l10n.themeModeDark;
    }
  }

  String _getTextSizeLabel(BuildContext context, TextSize size) {
    final l10n = AppLocalizations.of(context)!;
    switch (size) {
      case TextSize.small:
        return l10n.textSizeSmall;
      case TextSize.normal:
        return l10n.textSizeNormal;
      case TextSize.large:
        return l10n.textSizeLarge;
      case TextSize.extraLarge:
        return l10n.textSizeExtraLarge;
    }
  }

  String _getWeightUnitLabel(BuildContext context, WeightUnit unit) {
    final l10n = AppLocalizations.of(context)!;
    switch (unit) {
      case WeightUnit.kilograms:
        return l10n.weightUnitKilograms;
      case WeightUnit.pounds:
        return l10n.weightUnitPounds;
    }
  }

  String _getDateFormatLabel(BuildContext context, DateFormat format) {
    final l10n = AppLocalizations.of(context)!;
    switch (format) {
      case DateFormat.dayMonthYear:
        return l10n.dateFormatDayMonthYear;
      case DateFormat.monthDayYear:
        return l10n.dateFormatMonthDayYear;
      case DateFormat.yearMonthDay:
        return l10n.dateFormatYearMonthDay;
    }
  }

  String _getLanguageLabel(BuildContext context, AppLanguage language) {
    final l10n = AppLocalizations.of(context)!;
    switch (language) {
      case AppLanguage.spanish:
        return l10n.languageSpanish;
      case AppLanguage.portuguese:
        return l10n.languagePortuguese;
    }
  }

  void _showThemeModeDialog(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(l10n.selectTheme),
        content: RadioGroup<AppThemeMode>(
          groupValue: provider.settings.themeMode,
          onChanged: (value) {
            if (value != null) {
              provider.updateThemeMode(value);
              Navigator.pop(context);
            }
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: AppThemeMode.values.map((mode) {
              return RadioListTile<AppThemeMode>(
                title: Text(_getThemeModeLabel(context, mode)),
                value: mode,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  /// Obtiene el factor de escala para un TextSize
  double _getTextScaleFactor(TextSize textSize) {
    switch (textSize) {
      case TextSize.small:
        return 0.85;
      case TextSize.normal:
        return 1.0;
      case TextSize.large:
        return 1.15;
      case TextSize.extraLarge:
        return 1.3;
    }
  }

  /// Obtiene el tamaño de fuente escalado para mostrar en el diálogo
  /// Usa bodyMedium como base (14.0) y aplica el factor de escala
  double _getPreviewFontSize(TextSize textSize) {
    const double baseSize = 14.0; // bodyMedium base
    return baseSize * _getTextScaleFactor(textSize);
  }

  void _showTextSizeDialog(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text(l10n.selectTextSize),
        content: ConstrainedBox(
          constraints: const BoxConstraints(maxHeight: 300),
          child: SingleChildScrollView(
            child: RadioGroup<TextSize>(
              groupValue: provider.settings.textSize,
              onChanged: (value) async {
                if (value != null) {
                  // Actualizar primero (esto notificará y reconstruirá)
                  await provider.updateTextSize(value);
                  // Cerrar diálogo después de actualizar
                  if (dialogContext.mounted) {
                    Navigator.pop(dialogContext);
                  }
                }
              },
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: TextSize.values.map((size) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4.0),
                    child: RadioListTile<TextSize>(
                      title: Text(
                        _getTextSizeLabel(context, size),
                        // Aplicar tamaño de fuente específico para cada opción
                        style: TextStyle(fontSize: _getPreviewFontSize(size)),
                      ),
                      value: size,
                      dense: true,
                      contentPadding: EdgeInsets.zero,
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _showWeightUnitDialog(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(l10n.selectWeightUnit),
        content: RadioGroup<WeightUnit>(
          groupValue: provider.settings.weightUnit,
          onChanged: (value) {
            if (value != null) {
              provider.updateWeightUnit(value);
              Navigator.pop(context);
            }
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: WeightUnit.values.map((unit) {
              return RadioListTile<WeightUnit>(
                title: Text(_getWeightUnitLabel(context, unit)),
                value: unit,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  void _showDateFormatDialog(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(l10n.selectDateFormat),
        content: RadioGroup<DateFormat>(
          groupValue: provider.settings.dateFormat,
          onChanged: (value) {
            if (value != null) {
              provider.updateDateFormat(value);
              Navigator.pop(context);
            }
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: DateFormat.values.map((format) {
              return RadioListTile<DateFormat>(
                title: Text(_getDateFormatLabel(context, format)),
                value: format,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  void _showLanguageDialog(BuildContext context, SettingsProvider provider) {
    final l10n = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(l10n.selectLanguage),
        content: RadioGroup<AppLanguage>(
          groupValue: provider.settings.language,
          onChanged: (value) {
            if (value != null) {
              provider.updateLanguage(value);
              Navigator.pop(context);
            }
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: AppLanguage.values.map((language) {
              return RadioListTile<AppLanguage>(
                title: Text(_getLanguageLabel(context, language)),
                value: language,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}
