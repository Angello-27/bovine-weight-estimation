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
    return Consumer<SettingsProvider>(
      builder: (context, provider, _) {
        return Scaffold(
          appBar: AppBar(
            title: Text(
              'Configuración',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            flexibleSpace: Container(
              decoration: const BoxDecoration(color: AppColors.primary),
            ),
          ),
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
    return SettingsSection(
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
    );
  }

  /// Sección de captura
  Widget _buildCaptureSection(BuildContext context, SettingsProvider provider) {
    return SettingsSection(
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
    );
  }

  /// Sección de unidades y formato
  Widget _buildUnitsSection(BuildContext context, SettingsProvider provider) {
    return SettingsSection(
      title: 'Unidades y formato',
      icon: Icons.tune_rounded,
      children: [
        SettingsListTile(
          title: 'Unidad de peso',
          subtitle: _getWeightUnitLabel(provider.settings.weightUnit),
          icon: Icons.scale_rounded,
          onTap: () => _showWeightUnitDialog(context, provider),
        ),
        SettingsListTile(
          title: 'Formato de fecha',
          subtitle: _getDateFormatLabel(provider.settings.dateFormat),
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
    return SettingsSection(
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
                title: Text(_getThemeModeLabel(mode)),
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
    showDialog(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Tamaño de texto'),
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
                        _getTextSizeLabel(size),
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
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Unidad de peso'),
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
                title: Text(_getWeightUnitLabel(unit)),
                value: unit,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  void _showDateFormatDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Formato de fecha'),
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
                title: Text(_getDateFormatLabel(format)),
                value: format,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  void _showLanguageDialog(BuildContext context, SettingsProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Idioma'),
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
                title: Text(_getLanguageLabel(language)),
                value: language,
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}
