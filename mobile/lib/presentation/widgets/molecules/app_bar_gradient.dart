/// Molecule: AppBarGradient
///
/// AppBar reutilizable con gradiente primario y texto blanco.
/// Single Responsibility: Proporcionar AppBar consistente en todas las páginas.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';

/// AppBar con gradiente primario y texto blanco
///
/// Este componente proporciona un AppBar consistente para todas las páginas
/// (excepto home) con:
/// - Gradiente primario de fondo
/// - Texto blanco
/// - Soporte para acciones opcionales (IconButtons)
class AppBarGradient extends StatelessWidget implements PreferredSizeWidget {
  /// Título del AppBar
  final String title;

  /// Acciones opcionales (IconButtons) a mostrar en el AppBar
  final List<Widget>? actions;

  /// Widget de título personalizado (opcional, si se proporciona, ignora title)
  final Widget? titleWidget;

  /// Callback para el botón de retroceso (opcional)
  final VoidCallback? onBackPressed;

  const AppBarGradient({
    super.key,
    required this.title,
    this.actions,
    this.titleWidget,
    this.onBackPressed,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: titleWidget ?? Text(title),
      flexibleSpace: Container(
        decoration: const BoxDecoration(gradient: AppColors.primaryGradient),
      ),
      foregroundColor: Colors.white, // Texto blanco
      iconTheme: const IconThemeData(color: Colors.white), // Iconos blancos
      actionsIconTheme: const IconThemeData(
        color: Colors.white,
      ), // Iconos de acciones blancos
      actions: actions,
      leading: onBackPressed != null
          ? IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: onBackPressed,
              color: Colors.white,
            )
          : null,
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
