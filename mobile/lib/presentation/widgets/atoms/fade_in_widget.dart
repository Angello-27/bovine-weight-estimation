/// Atom: FadeInWidget
///
/// Widget con animación de fade-in al aparecer.
/// Single Responsibility: Animar la entrada de un widget con fade-in.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';

/// Widget con fade-in automático al aparecer
class FadeInWidget extends StatefulWidget {
  /// Widget hijo a animar
  final Widget child;

  /// Duración de la animación
  final Duration duration;

  /// Delay antes de comenzar
  final Duration delay;

  /// Offset en Y al inicio (para slide + fade)
  final double offsetY;

  const FadeInWidget({
    required this.child,
    this.duration = const Duration(milliseconds: 500),
    this.delay = Duration.zero,
    this.offsetY = 20.0,
    super.key,
  });

  @override
  State<FadeInWidget> createState() => _FadeInWidgetState();
}

class _FadeInWidgetState extends State<FadeInWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: widget.duration);

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));

    _slideAnimation = Tween<Offset>(
      begin: Offset(0, widget.offsetY),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeOut));

    // Iniciar animación después del delay
    Future.delayed(widget.delay, () {
      if (mounted) {
        _controller.forward();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: Transform.translate(
        offset: _slideAnimation.value,
        child: widget.child,
      ),
    );
  }
}
