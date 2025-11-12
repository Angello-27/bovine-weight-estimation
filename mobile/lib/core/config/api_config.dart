/// API Configuration
///
/// Configuración centralizada de la API backend.
/// Single Responsibility: Gestionar URLs y endpoints de la API.
///
/// Core Config Layer
library;

/// Configuración de la API backend
class ApiConfig {
  // ========================================
  // CONFIGURACIÓN POR AMBIENTE
  // ========================================

  /// URL base del backend
  ///
  /// **IMPORTANTE**: Cambiar según el entorno:
  /// - **Emulador Android**: `http://192.168.0.12:8000` (emulador usa 192.168.0.12 para localhost de la máquina)
  /// - **Dispositivo físico Android/iOS**: `http://TU_IP_LOCAL:8000` (ej: `http://192.168.1.100:8000`)
  /// - **Producción**: `https://api.tudominio.com`
  ///
  /// **Cómo obtener tu IP local:**
  /// - Mac/Linux: `ifconfig | grep "inet " | grep -v 127.0.0.1`
  /// - Windows: `ipconfig` (buscar "IPv4 Address")
  /// - Android: Configuración → Wi‑Fi → (red activa) → Ver detalles
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://192.168.0.12:8000', // Default para emulador Android
  );

  /// Prefijo de la API (v1, v2, etc.)
  static const String apiPrefix = '/api/v1';

  /// URL completa de la API
  static String get apiUrl => '$baseUrl$apiPrefix';

  // ========================================
  // ENDPOINTS
  // ========================================

  /// Endpoint de sincronización de ganado
  static String get syncCattleEndpoint => '$apiPrefix/sync/cattle';

  /// Endpoint de sincronización de estimaciones de peso
  static String get syncWeightEstimationsEndpoint =>
      '$apiPrefix/sync/weight-estimations';

  /// Endpoint de health check
  static String get healthEndpoint => '/health';

  /// Endpoint de predicción ML
  static String get mlPredictEndpoint => '$apiPrefix/ml/predict';

  // ========================================
  // CONFIGURACIÓN DE REQUESTS
  // ========================================

  /// Timeout de conexión (30 segundos)
  static const Duration connectTimeout = Duration(seconds: 30);

  /// Timeout de recepción (30 segundos)
  static const Duration receiveTimeout = Duration(seconds: 30);

  /// Timeout corto para health check (3 segundos)
  static const Duration healthCheckTimeout = Duration(seconds: 3);

  // ========================================
  // HEADERS
  // ========================================

  /// Headers por defecto para requests
  static const Map<String, String> defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  // ========================================
  // VALIDACIÓN
  // ========================================

  /// Valida que la URL base sea válida
  static bool isValidBaseUrl(String url) {
    try {
      final uri = Uri.parse(url);
      return uri.hasScheme && (uri.scheme == 'http' || uri.scheme == 'https');
    } catch (e) {
      return false;
    }
  }

  /// Obtiene la URL base según el ambiente
  ///
  /// Detecta automáticamente si está en emulador o dispositivo físico
  static String getBaseUrlForEnvironment() {
    // En producción, esto vendría de variables de entorno o archivo de configuración
    const envUrl = String.fromEnvironment('API_BASE_URL');
    if (envUrl.isNotEmpty) {
      return envUrl;
    }

    // Default: emulador Android
    return baseUrl;
  }
}
