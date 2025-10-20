/// Atom: SyncStatusIndicator
///
/// Indicador visual de estado de sincronización.
/// Single Responsibility: Mostrar estado offline/sincronizando/sincronizado.
///
/// Atomic Design - Presentation Layer
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';

/// Indicador de estado de sincronización
class SyncStatusIndicator extends StatelessWidget {
  /// Estado: 'offline', 'syncing', 'synced', 'error', 'idle'
  final String status;

  /// Texto descriptivo
  final String label;

  /// Tamaño del indicador
  final double size;

  /// Mostrar animación si está sincronizando
  final bool animated;

  const SyncStatusIndicator({
    super.key,
    required this.status,
    required this.label,
    this.size = 12.0,
    this.animated = true,
  });

  @override
  Widget build(BuildContext context) {
    final color = _getColorForStatus(status);
    final icon = _getIconForStatus(status);

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (status == 'syncing' && animated)
          SizedBox(
            width: size,
            height: size,
            child: CircularProgressIndicator(
              strokeWidth: 2.0,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          )
        else
          Container(
            width: size,
            height: size,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: color.withValues(alpha: 0.4),
                  blurRadius: 4.0,
                  spreadRadius: 1.0,
                ),
              ],
            ),
            child: Center(
              child: Icon(icon, size: size * 0.6, color: Colors.white),
            ),
          ),
        const SizedBox(width: 8.0),
        Text(
          label,
          style: TextStyle(
            fontSize: 13.0,
            fontWeight: FontWeight.w500,
            color: color,
          ),
        ),
      ],
    );
  }

  Color _getColorForStatus(String status) {
    switch (status) {
      case 'offline':
        return Colors.red.shade600;
      case 'syncing':
        return Colors.amber.shade600;
      case 'synced':
        return AppColors.primary; // Verde esmeralda
      case 'error':
        return Colors.orange.shade700;
      case 'idle':
      default:
        return Colors.grey.shade500;
    }
  }

  IconData _getIconForStatus(String status) {
    switch (status) {
      case 'offline':
        return Icons.cloud_off_rounded;
      case 'syncing':
        return Icons.sync_rounded;
      case 'synced':
        return Icons.cloud_done_rounded;
      case 'error':
        return Icons.error_outline_rounded;
      case 'idle':
      default:
        return Icons.cloud_queue_rounded;
    }
  }
}
