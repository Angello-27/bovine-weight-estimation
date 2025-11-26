/// App Colors - Material Design 3
///
/// Paleta de colores de marca - Hacienda Gamelera
/// Tema: Verde Naturaleza + Dorado Accent
/// Colores principales: #255946 (Primary), #EFB443 (Accent)
///
/// Core Theme - Design System
library;

import 'package:flutter/material.dart';

/// Colores de la aplicación
class AppColors {
  // ============================================================
  // COLORES PRIMARIOS (Verde Marca - #255946)
  // ============================================================
  static const Color primary = Color(0xFF255946); // Verde marca principal
  static const Color primaryLight = Color(0xFF49A760); // Verde claro (#49A760)
  static const Color primaryDark = Color(0xFF1F4E3D); // Verde oscuro (#1F4E3D)

  // ============================================================
  // COLORES SECUNDARIOS (Derivados del primario)
  // ============================================================
  static const Color secondary = Color(
    0xFF49A760,
  ); // Verde claro como secundario
  static const Color secondaryLight = Color(0xFF6BC47A); // Verde más claro
  static const Color secondaryDark = Color(0xFF1F4E3D); // Verde más oscuro

  // ============================================================
  // COLORES DE ACENTO (Dorado Marca - #EFB443)
  // ============================================================
  static const Color accent = Color(0xFFEFB443); // Dorado marca principal
  static const Color accentLight = Color(0xFFF5C869); // Dorado claro
  static const Color accentDark = Color(0xFFD99E2E); // Dorado oscuro

  // ============================================================
  // COLORES DE SUPERFICIE (Tema Claro)
  // ============================================================
  static const Color surface = Color(0xFFFAFAFA); // Blanco roto
  static const Color background = Color(0xFFFFFFFF); // Blanco
  static const Color surfaceVariant = Color(0xFFE8F5E9); // Verde muy claro

  // ============================================================
  // COLORES DE SUPERFICIE (Tema Oscuro)
  // ============================================================
  static const Color surfaceDark = Color(0xFF121212); // Casi negro
  static const Color backgroundDark = Color(0xFF1E1E1E); // Gris muy oscuro
  static const Color surfaceVariantDark = Color(0xFF1F4E3D); // Verde oscuro

  // ============================================================
  // COLORES DE TEXTO (Tema Claro)
  // ============================================================
  static const Color onPrimary = Color(0xFFFFFFFF); // Blanco sobre verde
  static const Color onSecondary = Color(
    0xFFFFFFFF,
  ); // Blanco sobre verde claro
  static const Color onAccent = Color(0xFF1F4E3D); // Verde oscuro sobre dorado
  static const Color onSurface = Color(0xFF212121); // Negro suave
  static const Color onBackground = Color(0xFF212121); // Negro suave
  static const Color textSecondary = Color(0xFF757575); // Gris texto secundario
  static const Color textTertiary = Color(0xFF9E9E9E); // Gris texto terciario

  // ============================================================
  // COLORES DE TEXTO (Tema Oscuro)
  // ============================================================
  static const Color onSurfaceDark = Color(0xFFE0E0E0); // Gris claro
  static const Color onBackgroundDark = Color(0xFFE0E0E0); // Gris claro
  static const Color textSecondaryDark = Color(0xFFB0B0B0); // Gris medio
  static const Color textTertiaryDark = Color(0xFF808080); // Gris oscuro

  // ============================================================
  // COLORES SEMÁNTICOS
  // ============================================================
  static const Color success = Color(0xFF49A760); // Verde claro de marca
  static const Color error = Color(0xFFEF4444); // Rojo brillante
  static const Color warning = Color(0xFFEFB443); // Dorado accent
  static const Color info = Color(0xFF255946); // Verde primario

  // Fondos Semánticos (Tema Claro)
  static const Color successLight = Color(0xFFE8F5E9); // Verde muy claro
  static const Color errorLight = Color(0xFFFEE2E2); // Rojo rosa claro
  static const Color warningLight = Color(0xFFFFF8E1); // Dorado crema claro
  static const Color infoLight = Color(
    0xFFE8F5E9,
  ); // Verde claro (mismo que success)

  // Fondos Semánticos (Tema Oscuro)
  static const Color successDark = Color(0xFF1F4E3D); // Verde oscuro
  static const Color errorDark = Color(0xFF7A1F1F); // Rojo oscuro
  static const Color warningDark = Color(0xFF8B6914); // Dorado oscuro
  static const Color infoDark = Color(0xFF0F2E1F); // Verde muy oscuro

  // ============================================================
  // GRADIENTES (Solo para fondos de tema)
  // ============================================================
  // Gradiente primario (para fondos de tema claro)
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF255946), Color(0xFF1F4E3D)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradiente primario (para fondos de tema oscuro)
  static const LinearGradient primaryGradientDark = LinearGradient(
    colors: [Color(0xFF1F4E3D), Color(0xFF0F2E1F)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradiente accent (para fondos especiales)
  static const LinearGradient accentGradient = LinearGradient(
    colors: [Color(0xFFEFB443), Color(0xFFD99E2E)],
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
  static const Color online = Color(
    0xFF49A760,
  ); // Verde claro de marca (online)
  static const Color syncing = Color(
    0xFF255946,
  ); // Verde primario (sincronizando)
}
