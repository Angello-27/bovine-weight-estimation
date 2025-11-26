/// Settings Page
///
/// Página de configuración de preferencias del usuario.
/// Single Responsibility: Orquestar componentes de settings.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../domain/entities/app_settings.dart';
import '../../providers/settings_provider.dart';
import 'widgets/settings_list_tile.dart';
import 'widgets/settings_section.dart';
import 'widgets/settings_switch_tile.dart';

/// Página de configuración
class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Configuración'),
        flexibleSpace: Container(
          decoration: const BoxDecoration(color: AppColors.primary),
        ),
      ),
      body: Consumer<SettingsProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading &&
              provider.settings == AppSettings.defaultSettings) {
            return const Center(child: CircularProgressIndicator());
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.screenPadding),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Sección: Apariencia
                SettingsSection(
                  title: 'Apariencia',
                  icon: Icons.palette_rounded,
                  children: [
                    SettingsListTile(
                      title: 'Tema',
                      subtitle: _getThemeModeLabel(provider.settings.themeMode),
                      icon: Icons.brightness_6_rounded,
                      onTap: () => _showThemeModeDialog(context, provider),
                    ),
                    SettingsListTile(
                      title: 'Tamaño de texto',
                      subtitle: _getTextSizeLabel(provider.settings.textSize),
                      icon: Icons.text_fields_rounded,
                      onTap: () => _showTextSizeDialog(context, provider),
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.lg),

                // Sección: Captura
                SettingsSection(
                  title: 'Captura',
                  icon: Icons.camera_alt_rounded,
                  children: [
                    SettingsSwitchTile(
                      title: 'Flash automático',
                      subtitle: 'Activar flash durante la captura',
                      icon: Icons.flash_on_rounded,
                      value: provider.settings.flashEnabled,
                      onChanged: (value) => provider.updateFlashEnabled(value),
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.lg),

                // Sección: Unidades y formato
                SettingsSection(
                  title: 'Unidades y formato',
                  icon: Icons.tune_rounded,
                  children: [
                    SettingsListTile(
                      title: 'Unidad de peso',
                      subtitle: _getWeightUnitLabel(
                        provider.settings.weightUnit,
                      ),
                      icon: Icons.scale_rounded,
                      onTap: () => _showWeightUnitDialog(context, provider),
                    ),
                    SettingsListTile(
                      title: 'Formato de fecha',
                      subtitle: _getDateFormatLabel(
                        provider.settings.dateFormat,
                      ),
                      icon: Icons.calendar_today_rounded,
                      onTap: () => _showDateFormatDialog(context, provider),
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.lg),

                // Sección: Idioma
                SettingsSection(
                  title: 'Idioma',
                  icon: Icons.language_rounded,
                  children: [
                    SettingsListTile(
                      title: 'Idioma de la interfaz',
                      subtitle: _getLanguageLabel(provider.settings.language),
                      icon: Icons.translate_rounded,
                      onTap: () => _showLanguageDialog(context, provider),
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          );
        },
      ),
    );
  }

  String _getThemeModeLabel(AppThemeMode mode) {
    switch (mode) {
      case AppThemeMode.system:
        return 'Seguir sistema';
      case AppThemeMode.light:
        return 'Claro';
      case AppThemeMode.dark:
        return 'Oscuro';
    }
  }

  String _getTextSizeLabel(TextSize size) {
    switch (size) {
      case TextSize.small:
        return 'Pequeño';
      case TextSize.normal:
        return 'Normal';
      case TextSize.large:
        return 'Grande';
      case TextSize.extraLarge:
        return 'Extra grande';
    }
  }

  String _getWeightUnitLabel(WeightUnit unit) {
    switch (unit) {
      case WeightUnit.kilograms:
        return 'Kilogramos (kg)';
      case WeightUnit.pounds:
        return 'Libras (lb)';
    }
  }

  String _getDateFormatLabel(DateFormat format) {
    switch (format) {
      case DateFormat.dayMonthYear:
        return 'DD/MM/YYYY';
      case DateFormat.monthDayYear:
        return 'MM/DD/YYYY';
      case DateFormat.yearMonthDay:
        return 'YYYY-MM-DD';
    }
  }

  String _getLanguageLabel(AppLanguage language) {
    switch (language) {
      case AppLanguage.spanish:
        return 'Español';
      case AppLanguage.english:
        return 'English';
    }
  }

  void _showThemeModeDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Seleccionar tema'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: AppThemeMode.values.map((mode) {
            return RadioListTile<AppThemeMode>(
              title: Text(_getThemeModeLabel(mode)),
              value: mode,
              groupValue: provider.settings.themeMode,
              onChanged: (value) {
                if (value != null) {
                  provider.updateThemeMode(value);
                  Navigator.pop(context);
                }
              },
            );
          }).toList(),
        ),
      ),
    );
  }

  void _showTextSizeDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Tamaño de texto'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: TextSize.values.map((size) {
            return RadioListTile<TextSize>(
              title: Text(_getTextSizeLabel(size)),
              value: size,
              groupValue: provider.settings.textSize,
              onChanged: (value) {
                if (value != null) {
                  provider.updateTextSize(value);
                  Navigator.pop(context);
                }
              },
            );
          }).toList(),
        ),
      ),
    );
  }

  void _showWeightUnitDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Unidad de peso'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: WeightUnit.values.map((unit) {
            return RadioListTile<WeightUnit>(
              title: Text(_getWeightUnitLabel(unit)),
              value: unit,
              groupValue: provider.settings.weightUnit,
              onChanged: (value) {
                if (value != null) {
                  provider.updateWeightUnit(value);
                  Navigator.pop(context);
                }
              },
            );
          }).toList(),
        ),
      ),
    );
  }

  void _showDateFormatDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Formato de fecha'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: DateFormat.values.map((format) {
            return RadioListTile<DateFormat>(
              title: Text(_getDateFormatLabel(format)),
              value: format,
              groupValue: provider.settings.dateFormat,
              onChanged: (value) {
                if (value != null) {
                  provider.updateDateFormat(value);
                  Navigator.pop(context);
                }
              },
            );
          }).toList(),
        ),
      ),
    );
  }

  void _showLanguageDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Idioma'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: AppLanguage.values.map((language) {
            return RadioListTile<AppLanguage>(
              title: Text(_getLanguageLabel(language)),
              value: language,
              groupValue: provider.settings.language,
              onChanged: (value) {
                if (value != null) {
                  provider.updateLanguage(value);
                  Navigator.pop(context);
                }
              },
            );
          }).toList(),
        ),
      ),
    );
  }
}
