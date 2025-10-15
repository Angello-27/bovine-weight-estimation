/// Service: PermissionService
///
/// Servicio para gestionar permisos de la aplicación.
/// Single Responsibility: Solicitar y verificar permisos del sistema.
///
/// Core Services Layer
library;

import 'package:permission_handler/permission_handler.dart';

/// Servicio de gestión de permisos
class PermissionService {
  /// Verifica si todos los permisos esenciales están otorgados
  ///
  /// NOTA: Solo cámara es crítica. Almacenamiento interno NO requiere permisos.
  Future<bool> hasAllRequiredPermissions() async {
    final camera = await Permission.camera.isGranted;
    return camera;
  }

  /// Verifica si los permisos opcionales están otorgados
  Future<bool> hasOptionalPermissions() async {
    final location = await Permission.location.isGranted;
    return location;
  }

  /// Solicita permiso de cámara (único permiso esencial)
  ///
  /// NOTA: No se solicita almacenamiento porque:
  /// - getTemporaryDirectory() no requiere permisos
  /// - SQLite en app-private storage no requiere permisos
  /// - No se guardan fotos en galería del usuario
  Future<bool> requestCameraPermission() async {
    final cameraStatus = await Permission.camera.request();
    return cameraStatus.isGranted;
  }

  /// Solicita permiso de ubicación (opcional para geolocalización)
  Future<bool> requestLocationPermission() async {
    final locationStatus = await Permission.location.request();
    return locationStatus.isGranted;
  }

  /// Solicita un permiso específico
  Future<PermissionStatus> requestPermission(Permission permission) async {
    return await permission.request();
  }

  /// Verifica si un permiso específico está otorgado
  Future<bool> isPermissionGranted(Permission permission) async {
    return await permission.isGranted;
  }

  /// Verifica si un permiso fue denegado permanentemente
  Future<bool> isPermissionPermanentlyDenied(Permission permission) async {
    return await permission.isPermanentlyDenied;
  }

  /// Abre la configuración de la app para que el usuario otorgue permisos
  Future<bool> openAppSettings() async {
    return await openAppSettings();
  }

  /// Verifica estado de permiso de cámara
  Future<PermissionStatus> getCameraPermissionStatus() async {
    return await Permission.camera.status;
  }

  /// Verifica estado de permiso de ubicación
  Future<PermissionStatus> getLocationPermissionStatus() async {
    return await Permission.location.status;
  }

  /// Verifica si se necesita mostrar rationale para un permiso
  ///
  /// Útil para mostrar diálogo explicativo antes de solicitar permiso
  Future<bool> shouldShowRequestRationale(Permission permission) async {
    final status = await permission.status;
    return status.isDenied && !status.isPermanentlyDenied;
  }
}
