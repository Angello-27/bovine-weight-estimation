// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appName => 'Agrocom';

  @override
  String get settings => 'Settings';

  @override
  String get appearance => 'Appearance';

  @override
  String get theme => 'Theme';

  @override
  String get textSize => 'Text Size';

  @override
  String get capture => 'Capture';

  @override
  String get autoFlash => 'Auto Flash';

  @override
  String get autoFlashSubtitle => 'Enable flash during capture';

  @override
  String get unitsAndFormat => 'Units and Format';

  @override
  String get weightUnit => 'Weight Unit';

  @override
  String get dateFormat => 'Date Format';

  @override
  String get language => 'Language';

  @override
  String get interfaceLanguage => 'Interface Language';

  @override
  String get themeModeSystem => 'Follow System';

  @override
  String get themeModeLight => 'Light';

  @override
  String get themeModeDark => 'Dark';

  @override
  String get textSizeSmall => 'Small';

  @override
  String get textSizeNormal => 'Normal';

  @override
  String get textSizeLarge => 'Large';

  @override
  String get textSizeExtraLarge => 'Extra Large';

  @override
  String get weightUnitKilograms => 'Kilograms (kg)';

  @override
  String get weightUnitPounds => 'Pounds (lb)';

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
  String get selectTheme => 'Select Theme';

  @override
  String get selectTextSize => 'Text Size';

  @override
  String get selectWeightUnit => 'Select Weight Unit';

  @override
  String get selectDateFormat => 'Select Date Format';

  @override
  String get selectLanguage => 'Language';

  @override
  String get quickAccess => 'Quick Access';

  @override
  String get captureAction => 'Capture';

  @override
  String get captureSubtitle => 'Frames';

  @override
  String get estimateAction => 'Estimate';

  @override
  String get estimateSubtitle => 'AI Weight';

  @override
  String get registerAction => 'Register';

  @override
  String get registerSubtitle => 'Animal';

  @override
  String get historyAction => 'History';

  @override
  String get historySubtitle => 'Weighings';

  @override
  String get retry => 'Retry';

  @override
  String get captureFrames => 'Frame Capture';

  @override
  String get configurePermissions => 'Configure Permissions';

  @override
  String get cameraPermissionDenied =>
      'Camera permission denied. Please enable it in settings.';

  @override
  String get weightEstimation => 'Weight Estimation';

  @override
  String get cancel => 'Cancel';

  @override
  String generatingPdf(String cattleName) {
    return 'Generating PDF for $cattleName...';
  }

  @override
  String get error => 'Error';

  @override
  String unexpectedError(String error) {
    return 'Unexpected error: $error';
  }

  @override
  String generatingCsv(String cattleName) {
    return 'Generating CSV for $cattleName...';
  }

  @override
  String get pdfSharedSuccessfully => 'PDF shared successfully';

  @override
  String errorSharingPdf(String error) {
    return 'Error sharing PDF: $error';
  }

  @override
  String errorPrintingPdf(String error) {
    return 'Error printing PDF: $error';
  }

  @override
  String errorShowingPdf(String error) {
    return 'Error showing PDF: $error';
  }

  @override
  String csvSavedAt(String path) {
    return 'CSV saved at: $path';
  }

  @override
  String errorSharingCsv(String error) {
    return 'Error sharing CSV: $error';
  }

  @override
  String get noSyncHistory => 'No sync history';

  @override
  String historyTitle(String cattleName) {
    return 'History - $cattleName';
  }

  @override
  String get export => 'Export';

  @override
  String get loadingHistory => 'Loading history...';

  @override
  String get errorLoadingHistory => 'Error loading history';

  @override
  String get unknownError => 'Unknown error';

  @override
  String get noWeighingsRegistered => 'No weighings registered';

  @override
  String performFirstEstimation(String cattleName) {
    return 'Perform the first weight estimation\nto see the history of $cattleName';
  }

  @override
  String get detailedHistory => 'Detailed History';

  @override
  String get syncStatus => 'Sync Status';

  @override
  String get registerAnimal => 'Register Animal';

  @override
  String get period => 'Period';

  @override
  String get estimateAgain => 'Estimate Again';

  @override
  String get estimateWeight => 'Estimate Weight';

  @override
  String get analyzingAnimalFeatures => 'Analyzing animal features';

  @override
  String get cameraPermissionRequired =>
      'Camera permission is required to show the preview.';

  @override
  String get exportAsCsv => 'Export as CSV';

  @override
  String get forExcelAnalysis => 'For Excel analysis';

  @override
  String get exportAsPdf => 'Export as PDF';

  @override
  String get forPrinting => 'For printing and sharing';

  @override
  String get estimatingWeightWithAI => 'Estimating weight with AI...';

  @override
  String get requiredData => 'Required Data';

  @override
  String get optionalData => 'Optional Data';

  @override
  String get earTagNumber => 'Ear Tag Number *';

  @override
  String get earTagExample => 'E.g: A-001';

  @override
  String get earTagRequired => 'Ear tag is required';

  @override
  String get earTagInvalid => 'Only alphanumeric and hyphens';

  @override
  String get birthDate => 'Birth Date *';

  @override
  String get selectDate => 'Select date';

  @override
  String get birthDateRequired => 'Birth date is required';

  @override
  String get selectBirthDate => 'Select birth date';

  @override
  String get accept => 'Accept';

  @override
  String get name => 'Name';

  @override
  String get nameExample => 'E.g: Brownie';

  @override
  String get color => 'Color';

  @override
  String get colorExample => 'E.g: Brown, Black';

  @override
  String get birthWeight => 'Birth Weight (kg)';

  @override
  String get birthWeightExample => 'E.g: 35';

  @override
  String get birthWeightInvalid => 'Weight must be between 10-100 kg';

  @override
  String get observations => 'Observations';

  @override
  String get observationsHint => 'Additional notes';

  @override
  String get automaticCategory => 'Automatic Category';

  @override
  String get newAnimal => 'New Animal';

  @override
  String get completeAnimalData => 'Complete the animal data';

  @override
  String get estimationCompleted => 'Estimation Completed!';

  @override
  String get estimatedWeight => 'Estimated Weight';

  @override
  String confidence(String percentage) {
    return 'Confidence: $percentage%';
  }

  @override
  String get breed => 'Breed';

  @override
  String get method => 'Method';

  @override
  String get processingTime => 'Processing Time';

  @override
  String get model => 'Model';

  @override
  String get selectedFrame => 'Selected Frame';

  @override
  String get breedRequired => 'Breed *';

  @override
  String get selectBreed => 'Select breed';

  @override
  String get breedRequiredValidation => 'Breed is required';

  @override
  String get genderRequired => 'Gender *';

  @override
  String get selectGender => 'Select gender';

  @override
  String get genderRequiredValidation => 'Gender is required';

  @override
  String get animals => 'Animals';

  @override
  String get averageWeight => 'Avg. Weight';

  @override
  String get breeds => 'Breeds';

  @override
  String get information => 'Information';

  @override
  String get connectivity => 'Connectivity';

  @override
  String get online => 'Online';

  @override
  String get offline => 'Offline';

  @override
  String get pendingItems => 'Pending items';

  @override
  String get automaticSync => 'Automatic sync';

  @override
  String get active => 'Active';

  @override
  String get syncAutoDescription =>
      'Sync runs automatically every 60 seconds when there is connection and pending items.';

  @override
  String get syncStatusTitle => 'Sync Status';

  @override
  String get synced => 'Synced';

  @override
  String get pending => 'Pending';

  @override
  String get errors => 'Errors';

  @override
  String get conflicts => 'Conflicts';

  @override
  String get syncNow => 'Sync now';

  @override
  String get syncing => 'Syncing...';

  @override
  String get noConnection => 'No connection';

  @override
  String get syncedStatus => 'Synced';

  @override
  String get syncError => 'Sync error';

  @override
  String get allSynced => 'All synced';

  @override
  String itemsWaitingSync(int count) {
    return '$count items waiting to sync';
  }

  @override
  String get noPendingChanges => 'No pending changes';

  @override
  String pendingCount(int count) {
    return '$count pending';
  }

  @override
  String get agoSeconds => 'A few seconds ago';

  @override
  String agoMinutes(int minutes) {
    return '${minutes}m ago';
  }

  @override
  String agoHours(int hours) {
    return '${hours}h ago';
  }

  @override
  String agoDays(int days) {
    return '${days}d ago';
  }

  @override
  String syncResultSuccess(int count) {
    return '$count items synced successfully';
  }

  @override
  String syncResultPartial(int synced, int total, int failed) {
    return '$synced of $total synced. $failed errors.';
  }

  @override
  String syncResultConflicts(int conflicts, int synced) {
    return '$conflicts conflicts detected. $synced synced.';
  }

  @override
  String get syncResultEmpty => 'No pending items to sync';

  @override
  String get syncResultNoChanges => 'No changes';

  @override
  String syncResultSynced(int count) {
    return '$count synced';
  }

  @override
  String syncResultPartialSummary(int synced, int total) {
    return '$synced of $total synced';
  }

  @override
  String syncResultError(int failed) {
    return 'Error: $failed failed';
  }
}
