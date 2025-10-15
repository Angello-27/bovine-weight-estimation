/// App Configuration
/// 
/// Configuración global de la aplicación.
/// Single Responsibility: Gestionar constantes y configuración.
///
/// Core Config Layer
library;

/// Configuración de la aplicación
class AppConfig {
  // Información de la aplicación
  static const String appName = 'Bovine Weight Estimation';
  static const String appVersion = '1.0.0';
  
  // Información del cliente
  static const String haciendaName = 'Hacienda Gamelera';
  static const String ownerName = 'Bruno Brito Macedo';
  static const String location = 'San Ignacio de Velasco, Santa Cruz, Bolivia';
  
  // Configuración de captura (US-001)
  static const int defaultTargetFps = 12; // 10-15 FPS
  static const int minFps = 10;
  static const int maxFps = 15;
  
  static const int defaultCaptureDuration = 4; // 3-5 segundos
  static const int minCaptureDuration = 3;
  static const int maxCaptureDuration = 5;
  
  // Configuración de calidad de fotogramas
  static const double minSharpness = 0.7;
  static const double minBrightness = 0.4;
  static const double maxBrightness = 0.8;
  static const double minContrast = 0.5;
  static const double minSilhouetteVisibility = 0.8;
  static const double minAngleScore = 0.6;
  
  // Ponderación de score global
  static const double silhouetteWeight = 0.40; // 40%
  static const double sharpnessWeight = 0.30; // 30%
  static const double brightnessWeight = 0.20; // 20%
  static const double angleWeight = 0.10; // 10%
  
  // Base de datos
  static const String databaseName = 'bovine_weight.db';
  static const int databaseVersion = 1;
  
  // Debug
  static const bool isDebugMode = true;
  static const bool showDebugBanner = false;
}

