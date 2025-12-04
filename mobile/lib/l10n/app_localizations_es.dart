// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Spanish Castilian (`es`).
class AppLocalizationsEs extends AppLocalizations {
  AppLocalizationsEs([String locale = 'es']) : super(locale);

  @override
  String get appName => 'Agrocom';

  @override
  String get settings => 'Configuración';

  @override
  String get appearance => 'Apariencia';

  @override
  String get theme => 'Tema';

  @override
  String get textSize => 'Tamaño de texto';

  @override
  String get capture => 'Captura';

  @override
  String get autoFlash => 'Flash automático';

  @override
  String get autoFlashSubtitle => 'Activar flash durante la captura';

  @override
  String get captureFps => 'FPS de Captura';

  @override
  String get fps => 'FPS';

  @override
  String get selectCaptureFps => 'Seleccionar FPS de Captura';

  @override
  String get unitsAndFormat => 'Unidades y formato';

  @override
  String get weightUnit => 'Unidad de peso';

  @override
  String get dateFormat => 'Formato de fecha';

  @override
  String get language => 'Idioma';

  @override
  String get interfaceLanguage => 'Idioma de la interfaz';

  @override
  String get themeModeSystem => 'Seguir sistema';

  @override
  String get themeModeLight => 'Claro';

  @override
  String get themeModeDark => 'Oscuro';

  @override
  String get textSizeSmall => 'Pequeño';

  @override
  String get textSizeNormal => 'Normal';

  @override
  String get textSizeLarge => 'Grande';

  @override
  String get textSizeExtraLarge => 'Extra grande';

  @override
  String get weightUnitKilograms => 'Kilogramos (kg)';

  @override
  String get weightUnitPounds => 'Libras (lb)';

  @override
  String get dateFormatDayMonthYear => 'DD/MM/YYYY';

  @override
  String get dateFormatMonthDayYear => 'MM/DD/YYYY';

  @override
  String get dateFormatYearMonthDay => 'YYYY-MM-DD';

  @override
  String get languageSpanish => 'Español';

  @override
  String get languagePortuguese => 'Português';

  @override
  String get selectTheme => 'Seleccionar tema';

  @override
  String get selectTextSize => 'Tamaño de texto';

  @override
  String get selectWeightUnit => 'Unidad de peso';

  @override
  String get selectDateFormat => 'Formato de fecha';

  @override
  String get selectLanguage => 'Idioma';

  @override
  String get quickAccess => 'Accesos Rápidos';

  @override
  String get captureAction => 'Capturar';

  @override
  String get captureSubtitle => 'Fotogramas';

  @override
  String get estimateAction => 'Estimar';

  @override
  String get estimateSubtitle => 'Peso IA';

  @override
  String get registerAction => 'Registrar';

  @override
  String get registerSubtitle => 'Animal';

  @override
  String get historyAction => 'Historial';

  @override
  String get historySubtitle => 'Pesajes';

  @override
  String get retry => 'Reintentar';

  @override
  String get captureFrames => 'Captura de Fotogramas';

  @override
  String get configurePermissions => 'Configurar Permisos';

  @override
  String get cameraPermissionDenied =>
      'Permiso de cámara denegado. Por favor, habilítalo en configuración.';

  @override
  String get weightEstimation => 'Estimación de Peso';

  @override
  String get cancel => 'Cancelar';

  @override
  String generatingPdf(String cattleName) {
    return 'Generando PDF de $cattleName...';
  }

  @override
  String get error => 'Error';

  @override
  String unexpectedError(String error) {
    return 'Error inesperado: $error';
  }

  @override
  String generatingCsv(String cattleName) {
    return 'Generando CSV de $cattleName...';
  }

  @override
  String get pdfSharedSuccessfully => 'PDF compartido exitosamente';

  @override
  String errorSharingPdf(String error) {
    return 'Error al compartir PDF: $error';
  }

  @override
  String errorPrintingPdf(String error) {
    return 'Error al imprimir PDF: $error';
  }

  @override
  String errorShowingPdf(String error) {
    return 'Error al mostrar PDF: $error';
  }

  @override
  String csvSavedAt(String path) {
    return 'CSV guardado en: $path';
  }

  @override
  String errorSharingCsv(String error) {
    return 'Error al compartir CSV: $error';
  }

  @override
  String get noSyncHistory => 'No hay historial de sincronización';

  @override
  String historyTitle(String cattleName) {
    return 'Historial - $cattleName';
  }

  @override
  String get export => 'Exportar';

  @override
  String get loadingHistory => 'Cargando historial...';

  @override
  String get errorLoadingHistory => 'Error al cargar historial';

  @override
  String get unknownError => 'Error desconocido';

  @override
  String get noWeighingsRegistered => 'Sin pesajes registrados';

  @override
  String performFirstEstimation(String cattleName) {
    return 'Realiza la primera estimación de peso\npara ver el historial de $cattleName';
  }

  @override
  String get detailedHistory => 'Historial Detallado';

  @override
  String get syncStatus => 'Estado de Sincronización';

  @override
  String get registerAnimal => 'Registrar Animal';

  @override
  String get period => 'Período';

  @override
  String get estimateAgain => 'Estimar Otra Vez';

  @override
  String get estimateWeight => 'Estimar Peso';

  @override
  String get analyzingAnimalFeatures => 'Analizando características del animal';

  @override
  String get cameraPermissionRequired =>
      'Se necesita permiso de cámara para mostrar el preview.';

  @override
  String get exportAsCsv => 'Exportar como CSV';

  @override
  String get forExcelAnalysis => 'Para análisis en Excel';

  @override
  String get exportAsPdf => 'Exportar como PDF';

  @override
  String get forPrinting => 'Para impresión y compartir';

  @override
  String get estimatingWeightWithAI => 'Estimando peso con IA...';

  @override
  String get requiredData => 'Datos Obligatorios';

  @override
  String get optionalData => 'Datos Opcionales';

  @override
  String get earTagNumber => 'Número de Caravana *';

  @override
  String get earTagExample => 'Ej: A-001';

  @override
  String get earTagRequired => 'La caravana es obligatoria';

  @override
  String get earTagInvalid => 'Solo alfanuméricos y guiones';

  @override
  String get birthDate => 'Fecha de Nacimiento *';

  @override
  String get selectDate => 'Selecciona fecha';

  @override
  String get birthDateRequired => 'La fecha de nacimiento es obligatoria';

  @override
  String get selectBirthDate => 'Selecciona fecha de nacimiento';

  @override
  String get accept => 'Aceptar';

  @override
  String get name => 'Nombre';

  @override
  String get nameExample => 'Ej: Brownie';

  @override
  String get color => 'Color';

  @override
  String get colorExample => 'Ej: Pardo, Negro';

  @override
  String get birthWeight => 'Peso al Nacer (kg)';

  @override
  String get birthWeightExample => 'Ej: 35';

  @override
  String get birthWeightInvalid => 'Peso debe estar entre 10-100 kg';

  @override
  String get observations => 'Observaciones';

  @override
  String get observationsHint => 'Notas adicionales';

  @override
  String get automaticCategory => 'Categoría Automática';

  @override
  String get newAnimal => 'Nuevo Animal';

  @override
  String get completeAnimalData => 'Completa los datos del animal';

  @override
  String get estimationCompleted => '¡Estimación Completada!';

  @override
  String get estimatedWeight => 'Peso Estimado';

  @override
  String confidence(String percentage) {
    return 'Confianza: $percentage%';
  }

  @override
  String get breed => 'Raza';

  @override
  String get method => 'Método';

  @override
  String get processingTime => 'Tiempo procesamiento';

  @override
  String get model => 'Modelo';

  @override
  String get selectedFrame => 'Fotograma seleccionado';

  @override
  String get breedRequired => 'Raza *';

  @override
  String get selectBreed => 'Selecciona la raza';

  @override
  String get breedRequiredValidation => 'La raza es obligatoria';

  @override
  String get genderRequired => 'Género *';

  @override
  String get selectGender => 'Selecciona el género';

  @override
  String get genderRequiredValidation => 'El género es obligatorio';

  @override
  String get animals => 'Animales';

  @override
  String get averageWeight => 'Peso Prom.';

  @override
  String get breeds => 'Razas';

  @override
  String get information => 'Información';

  @override
  String get connectivity => 'Conectividad';

  @override
  String get online => 'Online';

  @override
  String get offline => 'Offline';

  @override
  String get pendingItems => 'Items pendientes';

  @override
  String get automaticSync => 'Sincronización automática';

  @override
  String get active => 'Activa';

  @override
  String get syncAutoDescription =>
      'La sincronización se ejecuta automáticamente cada 60 segundos cuando hay conexión y items pendientes.';

  @override
  String get syncStatusTitle => 'Estado de Sincronización';

  @override
  String get synced => 'Sincronizados';

  @override
  String get pending => 'Pendientes';

  @override
  String get errors => 'Errores';

  @override
  String get conflicts => 'Conflictos';

  @override
  String get syncNow => 'Sincronizar ahora';

  @override
  String get syncing => 'Sincronizando...';

  @override
  String get noConnection => 'Sin conexión';

  @override
  String get syncedStatus => 'Sincronizado';

  @override
  String get syncError => 'Error al sincronizar';

  @override
  String get allSynced => 'Todo sincronizado';

  @override
  String itemsWaitingSync(int count) {
    return '$count items esperando sincronización';
  }

  @override
  String get noPendingChanges => 'No hay cambios pendientes';

  @override
  String pendingCount(int count) {
    return '$count pendientes';
  }

  @override
  String get agoSeconds => 'Hace unos segundos';

  @override
  String agoMinutes(int minutes) {
    return 'Hace ${minutes}m';
  }

  @override
  String agoHours(int hours) {
    return 'Hace ${hours}h';
  }

  @override
  String agoDays(int days) {
    return 'Hace ${days}d';
  }

  @override
  String syncResultSuccess(int count) {
    return '$count items sincronizados exitosamente';
  }

  @override
  String syncResultPartial(int synced, int total, int failed) {
    return '$synced de $total sincronizados. $failed errores.';
  }

  @override
  String syncResultConflicts(int conflicts, int synced) {
    return '$conflicts conflictos detectados. $synced sincronizados.';
  }

  @override
  String get syncResultEmpty => 'No hay items pendientes de sincronización';

  @override
  String get syncResultNoChanges => 'Sin cambios';

  @override
  String syncResultSynced(int count) {
    return '$count sincronizados';
  }

  @override
  String syncResultPartialSummary(int synced, int total) {
    return '$synced de $total sincronizados';
  }

  @override
  String syncResultError(int failed) {
    return 'Error: $failed fallidos';
  }

  @override
  String get login => 'Iniciar Sesión';

  @override
  String get loginTitle => 'Iniciar Sesión';

  @override
  String get loginSubtitle => 'Ingresa tus credenciales para continuar';

  @override
  String get username => 'Usuario';

  @override
  String get usernameHint => 'Ingresa tu nombre de usuario';

  @override
  String get usernameRequired => 'El usuario es requerido';

  @override
  String get password => 'Contraseña';

  @override
  String get passwordHint => 'Ingresa tu contraseña';

  @override
  String get passwordRequired => 'La contraseña es requerida';

  @override
  String get loggingIn => 'Iniciando sesión...';

  @override
  String get authenticationError => 'Error de autenticación';

  @override
  String get invalidCredentials =>
      'Credenciales inválidas. Verifica tu usuario y contraseña.';

  @override
  String get noInternetConnection =>
      'Sin conexión a internet. Verifica tu conexión.';

  @override
  String get serverError => 'Error del servidor';

  @override
  String get loginError => 'Error al iniciar sesión';

  @override
  String get appDescription => 'Hacienda Gamelera';

  @override
  String get bestFrameCaptured => 'Mejor Frame Capturado';

  @override
  String get globalScore => 'Score Global';

  @override
  String get sharpness => 'Nitidez';

  @override
  String get illumination => 'Iluminación';

  @override
  String get contrast => 'Contraste';

  @override
  String get silhouette => 'Silueta';

  @override
  String get totalFrames => 'Total Frames';

  @override
  String get optimalFrames => 'Frames Óptimos';

  @override
  String get confirmAndContinue => 'Confirmar y Continuar';

  @override
  String get deleteFrame => 'Eliminar Frame';

  @override
  String get deleteFrameConfirmation =>
      '¿Eliminar este frame? Se buscará otro mejor frame automáticamente.';
}
