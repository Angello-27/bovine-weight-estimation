/// Camera Framing Guides - Atom
///
/// Indicadores visuales de encuadre para ayudar a posicionar el ganado.
/// Muestra guías de composición sobre la cámara.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

/// Guías de encuadre para la cámara
class CameraFramingGuides extends StatelessWidget {
  const CameraFramingGuides({super.key});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return CustomPaint(painter: FramingGuidesPainter(), size: size);
  }
}

/// Painter para dibujar las guías de encuadre
class FramingGuidesPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.primary.withOpacity(0.6)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    // Regla de tercios: líneas verticales
    final verticalThird1 = size.width / 3;
    final verticalThird2 = size.width * 2 / 3;

    canvas.drawLine(
      Offset(verticalThird1, 0),
      Offset(verticalThird1, size.height),
      paint,
    );
    canvas.drawLine(
      Offset(verticalThird2, 0),
      Offset(verticalThird2, size.height),
      paint,
    );

    // Regla de tercios: líneas horizontales
    final horizontalThird1 = size.height / 3;
    final horizontalThird2 = size.height * 2 / 3;

    canvas.drawLine(
      Offset(0, horizontalThird1),
      Offset(size.width, horizontalThird1),
      paint,
    );
    canvas.drawLine(
      Offset(0, horizontalThird2),
      Offset(size.width, horizontalThird2),
      paint,
    );

    // Área central recomendada (rectángulo)
    final centerRect = Rect.fromCenter(
      center: Offset(size.width / 2, size.height / 2),
      width: size.width * 0.7,
      height: size.height * 0.6,
    );

    final centerPaint = Paint()
      ..color = AppColors.success.withOpacity(0.3)
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke;

    canvas.drawRect(centerRect, centerPaint);

    // Indicadores de esquinas (para alineación)
    final cornerPaint = Paint()
      ..color = AppColors.accent.withOpacity(0.8)
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke;

    final cornerSize = 30.0;

    // Esquina superior izquierda
    _drawCorner(canvas, Offset(20, 20), cornerSize, cornerPaint);
    // Esquina superior derecha
    _drawCorner(canvas, Offset(size.width - 20, 20), cornerSize, cornerPaint);
    // Esquina inferior izquierda
    _drawCorner(canvas, Offset(20, size.height - 20), cornerSize, cornerPaint);
    // Esquina inferior derecha
    _drawCorner(
      canvas,
      Offset(size.width - 20, size.height - 20),
      cornerSize,
      cornerPaint,
    );
  }

  /// Dibuja un indicador de esquina
  void _drawCorner(Canvas canvas, Offset center, double size, Paint paint) {
    final halfSize = size / 2;

    // Línea horizontal superior
    canvas.drawLine(
      Offset(center.dx - halfSize, center.dy),
      Offset(center.dx, center.dy),
      paint,
    );

    // Línea vertical izquierda
    canvas.drawLine(
      Offset(center.dx, center.dy - halfSize),
      Offset(center.dx, center.dy),
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
