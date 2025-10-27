/// App Colors - Material Design 3
///
/// Paleta de colores moderna para Agrocom (Taller de Grado UAGRM)
/// Tema: Agro-Tech Premium (Verde Vibrante + Azul Tecnológico)
/// Inspirado en: AgriWebb, HerdWatch, CattleMax
///
/// Core Theme - Design System
library;

import 'package:flutter/material.dart';

/// Colores de la aplicación
class AppColors {
  // Colores Primarios (Verde Esmeralda - Naturaleza + Innovación)
  static const Color primary = Color(0xFF10B981); // Verde esmeralda vibrante
  static const Color primaryLight = Color(0xFF34D399); // Verde menta claro
  static const Color primaryDark = Color(0xFF059669); // Verde bosque

  // Colores Secundarios (Azul Tech - Innovación + Precisión)
  static const Color secondary = Color(0xFF3B82F6); // Azul brillante
  static const Color secondaryLight = Color(0xFF60A5FA); // Azul cielo
  static const Color secondaryDark = Color(0xFF2563EB); // Azul profundo

  // Acento (Ámbar - Alertas y llamadas a la acción)
  static const Color accent = Color(0xFFF59E0B); // Ámbar cálido
  static const Color accentLight = Color(0xFFFBBF24); // Ámbar claro
  static const Color accentDark = Color(0xFFD97706); // Ámbar oscuro

  // Colores de Superficie (Neutrales)
  static const Color surface = Color(0xFFFAFAFA); // Blanco roto
  static const Color background = Color(0xFFFFFFFF); // Blanco
  static const Color surfaceVariant = Color(0xFFE0E0E0); // Gris claro

  // Colores de Texto
  static const Color onPrimary = Color(0xFFFFFFFF); // Blanco
  static const Color onSecondary = Color(0xFFFFFFFF); // Blanco
  static const Color onSurface = Color(0xFF212121); // Negro suave
  static const Color onBackground = Color(0xFF212121); // Negro suave
  static const Color textSecondary = Color(0xFF757575); // Gris texto secundario
  static const Color textTertiary = Color(0xFF9E9E9E); // Gris texto terciario

  // Colores Semánticos (más vibrantes)
  static const Color success = Color(0xFF10B981); // Verde esmeralda
  static const Color error = Color(0xFFEF4444); // Rojo brillante
  static const Color warning = Color(0xFFF59E0B); // Ámbar
  static const Color info = Color(0xFF3B82F6); // Azul brillante

  // Fondos Semánticos (sutiles)
  static const Color successLight = Color(0xFFD1FAE5); // Verde menta muy claro
  static const Color errorLight = Color(0xFFFEE2E2); // Rojo rosa claro
  static const Color warningLight = Color(0xFFFEF3C7); // Ámbar crema
  static const Color infoLight = Color(0xFFDBEAFE); // Azul cielo claro

  // Gradientes predefinidos
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF10B981), Color(0xFF059669)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient secondaryGradient = LinearGradient(
    colors: [Color(0xFF3B82F6), Color(0xFF2563EB)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient accentGradient = LinearGradient(
    colors: [Color(0xFFF59E0B), Color(0xFFD97706)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient infoGradient = LinearGradient(
    colors: [Color(0xFF3B82F6), Color(0xFF2563EB)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Colores Neutros para UI
  static const Color grey50 = Color(0xFFFAFAFA);
  static const Color grey100 = Color(0xFFF5F5F5);
  static const Color grey200 = Color(0xFFEEEEEE);
  static const Color grey300 = Color(0xFFE0E0E0);
  static const Color grey400 = Color(0xFFBDBDBD);
  static const Color grey500 = Color(0xFF9E9E9E);
  static const Color grey600 = Color(0xFF757575);
  static const Color grey700 = Color(0xFF616161);
  static const Color grey800 = Color(0xFF424242);
  static const Color grey900 = Color(0xFF212121);

  // Colores de Estado (Offline/Online)
  static const Color offline = Color(0xFF9E9E9E); // Gris (offline)
  static const Color online = Color(0xFF4CAF50); // Verde (online)
  static const Color syncing = Color(0xFF2196F3); // Azul (sincronizando)
}
