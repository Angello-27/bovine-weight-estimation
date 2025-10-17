/// Atom: AnimatedScaleButton
///
/// Widget que anima una escala al presionar (efecto de rebote).
/// Single Responsibility: Agregar animación de escala a cualquier widget.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';

/// Botón con animación de escala al presionar
class AnimatedScaleButton extends StatefulWidget {
  /// Widget hijo a animar
  final Widget child;

  /// Callback al tocar
  final VoidCallback? onTap;

  /// Escala cuando está presionado (default: 0.95)
  final double scaleOnPressed;

  /// Duración de la animación
  final Duration duration;

  const AnimatedScaleButton({
    required this.child,
    this.onTap,
    this.scaleOnPressed = 0.95,
    this.duration = const Duration(milliseconds: 100),
    super.key,
  });

  @override
  State<AnimatedScaleButton> createState() => _AnimatedScaleButtonState();
}

class _AnimatedScaleButtonState extends State<AnimatedScaleButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: widget.duration);

    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: widget.scaleOnPressed,
    ).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails details) {
    _controller.forward();
  }

  void _onTapUp(TapUpDetails details) {
    _controller.reverse();
  }

  void _onTapCancel() {
    _controller.reverse();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: widget.onTap != null ? _onTapDown : null,
      onTapUp: widget.onTap != null ? _onTapUp : null,
      onTapCancel: widget.onTap != null ? _onTapCancel : null,
      onTap: widget.onTap,
      child: ScaleTransition(scale: _scaleAnimation, child: widget.child),
    );
  }
}
