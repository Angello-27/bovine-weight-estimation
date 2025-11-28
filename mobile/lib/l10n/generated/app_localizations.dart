import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_es.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'generated/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('es'),
  ];

  /// Nombre de la aplicación
  ///
  /// In es, this message translates to:
  /// **'Agrocom'**
  String get appName;

  /// Título de la página de configuración
  ///
  /// In es, this message translates to:
  /// **'Configuración'**
  String get settings;

  /// Título de la sección de apariencia
  ///
  /// In es, this message translates to:
  /// **'Apariencia'**
  String get appearance;

  /// Etiqueta para el selector de tema
  ///
  /// In es, this message translates to:
  /// **'Tema'**
  String get theme;

  /// Etiqueta para el selector de tamaño de texto
  ///
  /// In es, this message translates to:
  /// **'Tamaño de texto'**
  String get textSize;

  /// Título de la sección de captura
  ///
  /// In es, this message translates to:
  /// **'Captura'**
  String get capture;

  /// Etiqueta para el switch de flash automático
  ///
  /// In es, this message translates to:
  /// **'Flash automático'**
  String get autoFlash;

  /// Subtítulo para el switch de flash automático
  ///
  /// In es, this message translates to:
  /// **'Activar flash durante la captura'**
  String get autoFlashSubtitle;

  /// Título de la sección de unidades y formato
  ///
  /// In es, this message translates to:
  /// **'Unidades y formato'**
  String get unitsAndFormat;

  /// Etiqueta para el selector de unidad de peso
  ///
  /// In es, this message translates to:
  /// **'Unidad de peso'**
  String get weightUnit;

  /// Etiqueta para el selector de formato de fecha
  ///
  /// In es, this message translates to:
  /// **'Formato de fecha'**
  String get dateFormat;

  /// Título de la sección de idioma
  ///
  /// In es, this message translates to:
  /// **'Idioma'**
  String get language;

  /// Etiqueta para el selector de idioma
  ///
  /// In es, this message translates to:
  /// **'Idioma de la interfaz'**
  String get interfaceLanguage;

  /// Opción de tema: seguir sistema
  ///
  /// In es, this message translates to:
  /// **'Seguir sistema'**
  String get themeModeSystem;

  /// Opción de tema: claro
  ///
  /// In es, this message translates to:
  /// **'Claro'**
  String get themeModeLight;

  /// Opción de tema: oscuro
  ///
  /// In es, this message translates to:
  /// **'Oscuro'**
  String get themeModeDark;

  /// Opción de tamaño de texto: pequeño
  ///
  /// In es, this message translates to:
  /// **'Pequeño'**
  String get textSizeSmall;

  /// Opción de tamaño de texto: normal
  ///
  /// In es, this message translates to:
  /// **'Normal'**
  String get textSizeNormal;

  /// Opción de tamaño de texto: grande
  ///
  /// In es, this message translates to:
  /// **'Grande'**
  String get textSizeLarge;

  /// Opción de tamaño de texto: extra grande
  ///
  /// In es, this message translates to:
  /// **'Extra grande'**
  String get textSizeExtraLarge;

  /// Opción de unidad de peso: kilogramos
  ///
  /// In es, this message translates to:
  /// **'Kilogramos (kg)'**
  String get weightUnitKilograms;

  /// Opción de unidad de peso: libras
  ///
  /// In es, this message translates to:
  /// **'Libras (lb)'**
  String get weightUnitPounds;

  /// Formato de fecha: día/mes/año
  ///
  /// In es, this message translates to:
  /// **'DD/MM/YYYY'**
  String get dateFormatDayMonthYear;

  /// Formato de fecha: mes/día/año
  ///
  /// In es, this message translates to:
  /// **'MM/DD/YYYY'**
  String get dateFormatMonthDayYear;

  /// Formato de fecha: año-mes-día
  ///
  /// In es, this message translates to:
  /// **'YYYY-MM-DD'**
  String get dateFormatYearMonthDay;

  /// Opción de idioma: español
  ///
  /// In es, this message translates to:
  /// **'Español'**
  String get languageSpanish;

  /// Opción de idioma: inglés
  ///
  /// In es, this message translates to:
  /// **'English'**
  String get languageEnglish;

  /// Título del diálogo de selección de tema
  ///
  /// In es, this message translates to:
  /// **'Seleccionar tema'**
  String get selectTheme;

  /// Título del diálogo de selección de tamaño de texto
  ///
  /// In es, this message translates to:
  /// **'Tamaño de texto'**
  String get selectTextSize;

  /// Título del diálogo de selección de unidad de peso
  ///
  /// In es, this message translates to:
  /// **'Unidad de peso'**
  String get selectWeightUnit;

  /// Título del diálogo de selección de formato de fecha
  ///
  /// In es, this message translates to:
  /// **'Formato de fecha'**
  String get selectDateFormat;

  /// Título del diálogo de selección de idioma
  ///
  /// In es, this message translates to:
  /// **'Idioma'**
  String get selectLanguage;

  /// Título de la sección de accesos rápidos
  ///
  /// In es, this message translates to:
  /// **'Accesos Rápidos'**
  String get quickAccess;

  /// Título de la acción de captura
  ///
  /// In es, this message translates to:
  /// **'Capturar'**
  String get captureAction;

  /// Subtítulo de la acción de captura
  ///
  /// In es, this message translates to:
  /// **'Fotogramas'**
  String get captureSubtitle;

  /// Título de la acción de estimación
  ///
  /// In es, this message translates to:
  /// **'Estimar'**
  String get estimateAction;

  /// Subtítulo de la acción de estimación
  ///
  /// In es, this message translates to:
  /// **'Peso IA'**
  String get estimateSubtitle;

  /// Título de la acción de registro
  ///
  /// In es, this message translates to:
  /// **'Registrar'**
  String get registerAction;

  /// Subtítulo de la acción de registro
  ///
  /// In es, this message translates to:
  /// **'Animal'**
  String get registerSubtitle;

  /// Título de la acción de historial
  ///
  /// In es, this message translates to:
  /// **'Historial'**
  String get historyAction;

  /// Subtítulo de la acción de historial
  ///
  /// In es, this message translates to:
  /// **'Pesajes'**
  String get historySubtitle;

  /// Texto del botón de reintentar
  ///
  /// In es, this message translates to:
  /// **'Reintentar'**
  String get retry;

  /// Título de la página de captura
  ///
  /// In es, this message translates to:
  /// **'Captura de Fotogramas'**
  String get captureFrames;

  /// Texto del botón para configurar permisos
  ///
  /// In es, this message translates to:
  /// **'Configurar Permisos'**
  String get configurePermissions;

  /// Mensaje cuando el permiso de cámara está denegado
  ///
  /// In es, this message translates to:
  /// **'Permiso de cámara denegado. Por favor, habilítalo en configuración.'**
  String get cameraPermissionDenied;

  /// Título de la página de estimación de peso
  ///
  /// In es, this message translates to:
  /// **'Estimación de Peso'**
  String get weightEstimation;

  /// Texto del botón de cancelar
  ///
  /// In es, this message translates to:
  /// **'Cancelar'**
  String get cancel;

  /// Mensaje al generar PDF
  ///
  /// In es, this message translates to:
  /// **'Generando PDF de {cattleName}...'**
  String generatingPdf(String cattleName);

  /// Título genérico de error
  ///
  /// In es, this message translates to:
  /// **'Error'**
  String get error;

  /// Mensaje de error inesperado
  ///
  /// In es, this message translates to:
  /// **'Error inesperado: {error}'**
  String unexpectedError(String error);

  /// Mensaje al generar CSV
  ///
  /// In es, this message translates to:
  /// **'Generando CSV de {cattleName}...'**
  String generatingCsv(String cattleName);

  /// Mensaje cuando el PDF se compartió exitosamente
  ///
  /// In es, this message translates to:
  /// **'PDF compartido exitosamente'**
  String get pdfSharedSuccessfully;

  /// Mensaje de error al compartir PDF
  ///
  /// In es, this message translates to:
  /// **'Error al compartir PDF: {error}'**
  String errorSharingPdf(String error);

  /// Mensaje de error al imprimir PDF
  ///
  /// In es, this message translates to:
  /// **'Error al imprimir PDF: {error}'**
  String errorPrintingPdf(String error);

  /// Mensaje de error al mostrar PDF
  ///
  /// In es, this message translates to:
  /// **'Error al mostrar PDF: {error}'**
  String errorShowingPdf(String error);

  /// Mensaje cuando el CSV se guardó exitosamente
  ///
  /// In es, this message translates to:
  /// **'CSV guardado en: {path}'**
  String csvSavedAt(String path);

  /// Mensaje de error al compartir CSV
  ///
  /// In es, this message translates to:
  /// **'Error al compartir CSV: {error}'**
  String errorSharingCsv(String error);

  /// Mensaje cuando no hay historial de sincronización
  ///
  /// In es, this message translates to:
  /// **'No hay historial de sincronización'**
  String get noSyncHistory;

  /// Título de la página de historial
  ///
  /// In es, this message translates to:
  /// **'Historial - {cattleName}'**
  String historyTitle(String cattleName);

  /// Texto del botón de exportar
  ///
  /// In es, this message translates to:
  /// **'Exportar'**
  String get export;

  /// Mensaje mientras se carga el historial
  ///
  /// In es, this message translates to:
  /// **'Cargando historial...'**
  String get loadingHistory;

  /// Título de error al cargar historial
  ///
  /// In es, this message translates to:
  /// **'Error al cargar historial'**
  String get errorLoadingHistory;

  /// Mensaje de error desconocido
  ///
  /// In es, this message translates to:
  /// **'Error desconocido'**
  String get unknownError;

  /// Título cuando no hay pesajes
  ///
  /// In es, this message translates to:
  /// **'Sin pesajes registrados'**
  String get noWeighingsRegistered;

  /// Mensaje cuando no hay pesajes
  ///
  /// In es, this message translates to:
  /// **'Realiza la primera estimación de peso\npara ver el historial de {cattleName}'**
  String performFirstEstimation(String cattleName);

  /// Título de la sección de historial detallado
  ///
  /// In es, this message translates to:
  /// **'Historial Detallado'**
  String get detailedHistory;

  /// Título de la página de estado de sincronización
  ///
  /// In es, this message translates to:
  /// **'Estado de Sincronización'**
  String get syncStatus;

  /// Título de la página de registro de animal
  ///
  /// In es, this message translates to:
  /// **'Registrar Animal'**
  String get registerAnimal;

  /// Título de la sección de período
  ///
  /// In es, this message translates to:
  /// **'Período'**
  String get period;

  /// Texto del botón para estimar de nuevo
  ///
  /// In es, this message translates to:
  /// **'Estimar Otra Vez'**
  String get estimateAgain;

  /// Texto del botón para estimar peso
  ///
  /// In es, this message translates to:
  /// **'Estimar Peso'**
  String get estimateWeight;

  /// Mensaje mientras se analiza el animal
  ///
  /// In es, this message translates to:
  /// **'Analizando características del animal'**
  String get analyzingAnimalFeatures;

  /// Mensaje cuando se necesita permiso de cámara
  ///
  /// In es, this message translates to:
  /// **'Se necesita permiso de cámara para mostrar el preview.'**
  String get cameraPermissionRequired;

  /// Texto de la opción para exportar como CSV
  ///
  /// In es, this message translates to:
  /// **'Exportar como CSV'**
  String get exportAsCsv;

  /// Subtítulo de la opción de exportar CSV
  ///
  /// In es, this message translates to:
  /// **'Para análisis en Excel'**
  String get forExcelAnalysis;

  /// Texto de la opción para exportar como PDF
  ///
  /// In es, this message translates to:
  /// **'Exportar como PDF'**
  String get exportAsPdf;

  /// Subtítulo de la opción de exportar PDF
  ///
  /// In es, this message translates to:
  /// **'Para impresión y compartir'**
  String get forPrinting;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'es'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'es':
      return AppLocalizationsEs();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
