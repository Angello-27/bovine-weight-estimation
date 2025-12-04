import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_es.dart';
import 'app_localizations_pt.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
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
    Locale('es'),
    Locale('pt'),
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

  /// Opción de idioma: Portugués
  ///
  /// In es, this message translates to:
  /// **'Português'**
  String get languagePortuguese;

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

  /// Mensaje mientras se estima el peso con IA
  ///
  /// In es, this message translates to:
  /// **'Estimando peso con IA...'**
  String get estimatingWeightWithAI;

  /// Título de la sección de datos obligatorios
  ///
  /// In es, this message translates to:
  /// **'Datos Obligatorios'**
  String get requiredData;

  /// Título de la sección de datos opcionales
  ///
  /// In es, this message translates to:
  /// **'Datos Opcionales'**
  String get optionalData;

  /// Label del campo número de caravana
  ///
  /// In es, this message translates to:
  /// **'Número de Caravana *'**
  String get earTagNumber;

  /// Hint del campo número de caravana
  ///
  /// In es, this message translates to:
  /// **'Ej: A-001'**
  String get earTagExample;

  /// Mensaje de validación: caravana obligatoria
  ///
  /// In es, this message translates to:
  /// **'La caravana es obligatoria'**
  String get earTagRequired;

  /// Mensaje de validación: formato inválido de caravana
  ///
  /// In es, this message translates to:
  /// **'Solo alfanuméricos y guiones'**
  String get earTagInvalid;

  /// Label del campo fecha de nacimiento
  ///
  /// In es, this message translates to:
  /// **'Fecha de Nacimiento *'**
  String get birthDate;

  /// Hint del campo fecha de nacimiento
  ///
  /// In es, this message translates to:
  /// **'Selecciona fecha'**
  String get selectDate;

  /// Mensaje de validación: fecha de nacimiento obligatoria
  ///
  /// In es, this message translates to:
  /// **'La fecha de nacimiento es obligatoria'**
  String get birthDateRequired;

  /// Título del selector de fecha
  ///
  /// In es, this message translates to:
  /// **'Selecciona fecha de nacimiento'**
  String get selectBirthDate;

  /// Texto del botón aceptar
  ///
  /// In es, this message translates to:
  /// **'Aceptar'**
  String get accept;

  /// Label del campo nombre
  ///
  /// In es, this message translates to:
  /// **'Nombre'**
  String get name;

  /// Hint del campo nombre
  ///
  /// In es, this message translates to:
  /// **'Ej: Brownie'**
  String get nameExample;

  /// Label del campo color
  ///
  /// In es, this message translates to:
  /// **'Color'**
  String get color;

  /// Hint del campo color
  ///
  /// In es, this message translates to:
  /// **'Ej: Pardo, Negro'**
  String get colorExample;

  /// Label del campo peso al nacer
  ///
  /// In es, this message translates to:
  /// **'Peso al Nacer (kg)'**
  String get birthWeight;

  /// Hint del campo peso al nacer
  ///
  /// In es, this message translates to:
  /// **'Ej: 35'**
  String get birthWeightExample;

  /// Mensaje de validación: peso inválido
  ///
  /// In es, this message translates to:
  /// **'Peso debe estar entre 10-100 kg'**
  String get birthWeightInvalid;

  /// Label del campo observaciones
  ///
  /// In es, this message translates to:
  /// **'Observaciones'**
  String get observations;

  /// Hint del campo observaciones
  ///
  /// In es, this message translates to:
  /// **'Notas adicionales'**
  String get observationsHint;

  /// Título de la categoría automática
  ///
  /// In es, this message translates to:
  /// **'Categoría Automática'**
  String get automaticCategory;

  /// Título del header de registro
  ///
  /// In es, this message translates to:
  /// **'Nuevo Animal'**
  String get newAnimal;

  /// Descripción del header de registro
  ///
  /// In es, this message translates to:
  /// **'Completa los datos del animal'**
  String get completeAnimalData;

  /// Título cuando se completa la estimación
  ///
  /// In es, this message translates to:
  /// **'¡Estimación Completada!'**
  String get estimationCompleted;

  /// Label del peso estimado
  ///
  /// In es, this message translates to:
  /// **'Peso Estimado'**
  String get estimatedWeight;

  /// Label de confianza con porcentaje
  ///
  /// In es, this message translates to:
  /// **'Confianza: {percentage}%'**
  String confidence(String percentage);

  /// Label de raza
  ///
  /// In es, this message translates to:
  /// **'Raza'**
  String get breed;

  /// Label de método
  ///
  /// In es, this message translates to:
  /// **'Método'**
  String get method;

  /// Label de tiempo de procesamiento
  ///
  /// In es, this message translates to:
  /// **'Tiempo procesamiento'**
  String get processingTime;

  /// Label de modelo
  ///
  /// In es, this message translates to:
  /// **'Modelo'**
  String get model;

  /// Título del preview del fotograma
  ///
  /// In es, this message translates to:
  /// **'Fotograma seleccionado'**
  String get selectedFrame;

  /// Label del dropdown de raza
  ///
  /// In es, this message translates to:
  /// **'Raza *'**
  String get breedRequired;

  /// Hint del dropdown de raza
  ///
  /// In es, this message translates to:
  /// **'Selecciona la raza'**
  String get selectBreed;

  /// Mensaje de validación: raza obligatoria
  ///
  /// In es, this message translates to:
  /// **'La raza es obligatoria'**
  String get breedRequiredValidation;

  /// Label del dropdown de género
  ///
  /// In es, this message translates to:
  /// **'Género *'**
  String get genderRequired;

  /// Hint del dropdown de género
  ///
  /// In es, this message translates to:
  /// **'Selecciona el género'**
  String get selectGender;

  /// Mensaje de validación: género obligatorio
  ///
  /// In es, this message translates to:
  /// **'El género es obligatorio'**
  String get genderRequiredValidation;

  /// Label de estadística: animales
  ///
  /// In es, this message translates to:
  /// **'Animales'**
  String get animals;

  /// Label de estadística: peso promedio
  ///
  /// In es, this message translates to:
  /// **'Peso Prom.'**
  String get averageWeight;

  /// Label de estadística: razas
  ///
  /// In es, this message translates to:
  /// **'Razas'**
  String get breeds;

  /// Título de sección de información
  ///
  /// In es, this message translates to:
  /// **'Información'**
  String get information;

  /// Label de conectividad
  ///
  /// In es, this message translates to:
  /// **'Conectividad'**
  String get connectivity;

  /// Estado: online
  ///
  /// In es, this message translates to:
  /// **'Online'**
  String get online;

  /// Estado: offline
  ///
  /// In es, this message translates to:
  /// **'Offline'**
  String get offline;

  /// Label de items pendientes
  ///
  /// In es, this message translates to:
  /// **'Items pendientes'**
  String get pendingItems;

  /// Label de sincronización automática
  ///
  /// In es, this message translates to:
  /// **'Sincronización automática'**
  String get automaticSync;

  /// Estado: activa
  ///
  /// In es, this message translates to:
  /// **'Activa'**
  String get active;

  /// Descripción de sincronización automática
  ///
  /// In es, this message translates to:
  /// **'La sincronización se ejecuta automáticamente cada 60 segundos cuando hay conexión y items pendientes.'**
  String get syncAutoDescription;

  /// Título del card de estado de sincronización
  ///
  /// In es, this message translates to:
  /// **'Estado de Sincronización'**
  String get syncStatusTitle;

  /// Label: sincronizados
  ///
  /// In es, this message translates to:
  /// **'Sincronizados'**
  String get synced;

  /// Label: pendientes
  ///
  /// In es, this message translates to:
  /// **'Pendientes'**
  String get pending;

  /// Label: errores
  ///
  /// In es, this message translates to:
  /// **'Errores'**
  String get errors;

  /// Label: conflictos
  ///
  /// In es, this message translates to:
  /// **'Conflictos'**
  String get conflicts;

  /// Texto del botón de sincronización manual
  ///
  /// In es, this message translates to:
  /// **'Sincronizar ahora'**
  String get syncNow;

  /// Estado: sincronizando
  ///
  /// In es, this message translates to:
  /// **'Sincronizando...'**
  String get syncing;

  /// Estado: sin conexión
  ///
  /// In es, this message translates to:
  /// **'Sin conexión'**
  String get noConnection;

  /// Estado: sincronizado
  ///
  /// In es, this message translates to:
  /// **'Sincronizado'**
  String get syncedStatus;

  /// Estado: error al sincronizar
  ///
  /// In es, this message translates to:
  /// **'Error al sincronizar'**
  String get syncError;

  /// Estado: todo sincronizado
  ///
  /// In es, this message translates to:
  /// **'Todo sincronizado'**
  String get allSynced;

  /// Mensaje: items esperando sincronización
  ///
  /// In es, this message translates to:
  /// **'{count} items esperando sincronización'**
  String itemsWaitingSync(int count);

  /// Estado: no hay cambios pendientes
  ///
  /// In es, this message translates to:
  /// **'No hay cambios pendientes'**
  String get noPendingChanges;

  /// Estado: cantidad pendiente
  ///
  /// In es, this message translates to:
  /// **'{count} pendientes'**
  String pendingCount(int count);

  /// Tiempo transcurrido: hace unos segundos
  ///
  /// In es, this message translates to:
  /// **'Hace unos segundos'**
  String get agoSeconds;

  /// Tiempo transcurrido: hace X minutos
  ///
  /// In es, this message translates to:
  /// **'Hace {minutes}m'**
  String agoMinutes(int minutes);

  /// Tiempo transcurrido: hace X horas
  ///
  /// In es, this message translates to:
  /// **'Hace {hours}h'**
  String agoHours(int hours);

  /// Tiempo transcurrido: hace X días
  ///
  /// In es, this message translates to:
  /// **'Hace {days}d'**
  String agoDays(int days);

  /// Mensaje de sincronización exitosa
  ///
  /// In es, this message translates to:
  /// **'{count} items sincronizados exitosamente'**
  String syncResultSuccess(int count);

  /// Mensaje de sincronización parcial con errores
  ///
  /// In es, this message translates to:
  /// **'{synced} de {total} sincronizados. {failed} errores.'**
  String syncResultPartial(int synced, int total, int failed);

  /// Mensaje de sincronización con conflictos
  ///
  /// In es, this message translates to:
  /// **'{conflicts} conflictos detectados. {synced} sincronizados.'**
  String syncResultConflicts(int conflicts, int synced);

  /// Mensaje cuando no hay items para sincronizar
  ///
  /// In es, this message translates to:
  /// **'No hay items pendientes de sincronización'**
  String get syncResultEmpty;

  /// Mensaje cuando no hay cambios
  ///
  /// In es, this message translates to:
  /// **'Sin cambios'**
  String get syncResultNoChanges;

  /// Resumen de items sincronizados
  ///
  /// In es, this message translates to:
  /// **'{count} sincronizados'**
  String syncResultSynced(int count);

  /// Resumen de sincronización parcial
  ///
  /// In es, this message translates to:
  /// **'{synced} de {total} sincronizados'**
  String syncResultPartialSummary(int synced, int total);

  /// Mensaje de error en sincronización
  ///
  /// In es, this message translates to:
  /// **'Error: {failed} fallidos'**
  String syncResultError(int failed);

  /// Botón de login
  ///
  /// In es, this message translates to:
  /// **'Iniciar Sesión'**
  String get login;

  /// Título de la página de login
  ///
  /// In es, this message translates to:
  /// **'Iniciar Sesión'**
  String get loginTitle;

  /// Subtítulo de la página de login
  ///
  /// In es, this message translates to:
  /// **'Ingresa tus credenciales para continuar'**
  String get loginSubtitle;

  /// Etiqueta del campo de usuario
  ///
  /// In es, this message translates to:
  /// **'Usuario'**
  String get username;

  /// Hint del campo de usuario
  ///
  /// In es, this message translates to:
  /// **'Ingresa tu nombre de usuario'**
  String get usernameHint;

  /// Mensaje de validación: usuario requerido
  ///
  /// In es, this message translates to:
  /// **'El usuario es requerido'**
  String get usernameRequired;

  /// Etiqueta del campo de contraseña
  ///
  /// In es, this message translates to:
  /// **'Contraseña'**
  String get password;

  /// Hint del campo de contraseña
  ///
  /// In es, this message translates to:
  /// **'Ingresa tu contraseña'**
  String get passwordHint;

  /// Mensaje de validación: contraseña requerida
  ///
  /// In es, this message translates to:
  /// **'La contraseña es requerida'**
  String get passwordRequired;

  /// Mensaje mientras se inicia sesión
  ///
  /// In es, this message translates to:
  /// **'Iniciando sesión...'**
  String get loggingIn;

  /// Título de error de autenticación
  ///
  /// In es, this message translates to:
  /// **'Error de autenticación'**
  String get authenticationError;

  /// Mensaje de error: credenciales inválidas
  ///
  /// In es, this message translates to:
  /// **'Credenciales inválidas. Verifica tu usuario y contraseña.'**
  String get invalidCredentials;

  /// Mensaje de error: sin conexión
  ///
  /// In es, this message translates to:
  /// **'Sin conexión a internet. Verifica tu conexión.'**
  String get noInternetConnection;

  /// Mensaje de error del servidor
  ///
  /// In es, this message translates to:
  /// **'Error del servidor'**
  String get serverError;

  /// Mensaje genérico de error de login
  ///
  /// In es, this message translates to:
  /// **'Error al iniciar sesión'**
  String get loginError;

  /// Descripción de la aplicación
  ///
  /// In es, this message translates to:
  /// **'Hacienda Gamelera'**
  String get appDescription;
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
      <String>['es', 'pt'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'es':
      return AppLocalizationsEs();
    case 'pt':
      return AppLocalizationsPt();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
