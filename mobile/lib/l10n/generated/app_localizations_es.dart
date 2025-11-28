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
  String get languageEnglish => 'English';

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
}
