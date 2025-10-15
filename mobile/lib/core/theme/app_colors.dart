/// App Colors - Material Design 3
///
/// Paleta de colores temática para Hacienda Gamelera.
/// Tema: Ganadería Rural Boliviana (Verde Campo + Terracota)
///
/// Core UI - Design System
library;

import 'package:flutter/material.dart';

/// Colores de la aplicación
class AppColors {
  // Colores Primarios (Verde Campo/Agricultura)
  static const Color primary = Color(0xFF2E7D32); // Verde oscuro
  static const Color primaryLight = Color(0xFF60AD5E); // Verde claro
  static const Color primaryDark = Color(0xFF005005); // Verde muy oscuro

  // Colores Secundarios (Terracota/Tierra)
  static const Color secondary = Color(0xFFD84315); // Terracota
  static const Color secondaryLight = Color(0xFFFF7543); // Terracota claro
  static const Color secondaryDark = Color(0xFF9F0000); // Terracota oscuro

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

  // Colores Semánticos
  static const Color success = Color(0xFF4CAF50); // Verde éxito
  static const Color error = Color(0xFFD32F2F); // Rojo error
  static const Color warning = Color(0xFFFFA726); // Naranja warning
  static const Color info = Color(0xFF1976D2); // Azul info

  // Fondos Semánticos
  static const Color successLight = Color(0xFFE8F5E9); // Fondo verde claro
  static const Color errorLight = Color(0xFFFFEBEE); // Fondo rojo claro
  static const Color warningLight = Color(0xFFFFF3E0); // Fondo naranja claro
  static const Color infoLight = Color(0xFFE3F2FD); // Fondo azul claro

  // Colores Neutros para UI
  static const Color grey50 = Color(0xFFFAFAFA);
  static const Color grey100 = Color(0xFFF5F5F5);
  static const Color grey200 = Color(0xFFEEEEEE);
  static const Color grey300 = Color(0xFFE0E0E0);
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
