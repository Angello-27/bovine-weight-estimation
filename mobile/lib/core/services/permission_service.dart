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
  Future<bool> hasAllRequiredPermissions() async {
    final camera = await Permission.camera.isGranted;
    final storage = await _hasStoragePermission();

    return camera && storage;
  }

  /// Verifica si los permisos opcionales están otorgados
  Future<bool> hasOptionalPermissions() async {
    final location = await Permission.location.isGranted;
    return location;
  }

  /// Solicita todos los permisos esenciales
  ///
  /// Retorna true si todos fueron otorgados, false en caso contrario
  Future<bool> requestRequiredPermissions() async {
    // Solicitar cámara (crítico para US-001)
    final cameraStatus = await Permission.camera.request();

    // Solicitar almacenamiento (crítico para SQLite y fotogramas)
    final storageStatus = await _requestStoragePermission();

    return cameraStatus.isGranted && storageStatus.isGranted;
  }

  /// Solicita permisos opcionales (GPS)
  Future<bool> requestOptionalPermissions() async {
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

  /// Verifica y solicita permiso de almacenamiento según versión de Android
  ///
  /// Android 13+ (API 33): usa READ_MEDIA_IMAGES
  /// Android 10-12 (API 29-32): usa READ_EXTERNAL_STORAGE
  /// Android <10 (API <29): usa WRITE_EXTERNAL_STORAGE
  Future<PermissionStatus> _requestStoragePermission() async {
    // En Android 13+, necesitamos READ_MEDIA_IMAGES
    if (await Permission.photos.isGranted) {
      return PermissionStatus.granted;
    }

    // Intentar con photos (Android 13+)
    var status = await Permission.photos.request();
    if (status.isGranted) return status;

    // Fallback para versiones antiguas de Android
    status = await Permission.storage.request();
    return status;
  }

  /// Verifica permiso de almacenamiento
  Future<bool> _hasStoragePermission() async {
    // Android 13+
    if (await Permission.photos.isGranted) return true;

    // Android <13
    if (await Permission.storage.isGranted) return true;

    return false;
  }

  /// Solicita todos los permisos en secuencia con mensajes claros
  ///
  /// Retorna mapa con estado de cada permiso
  Future<Map<String, PermissionStatus>>
  requestAllPermissionsWithDetails() async {
    final results = <String, PermissionStatus>{};

    // 1. Cámara (crítico)
    results['camera'] = await Permission.camera.request();

    // 2. Almacenamiento (crítico)
    results['storage'] = await _requestStoragePermission();

    // 3. Ubicación (opcional)
    results['location'] = await Permission.location.request();

    return results;
  }

  /// Verifica si se necesita mostrar rationale para un permiso
  ///
  /// Útil para mostrar diálogo explicativo antes de solicitar permiso
  Future<bool> shouldShowRequestRationale(Permission permission) async {
    final status = await permission.status;
    return status.isDenied && !status.isPermanentlyDenied;
  }
}
