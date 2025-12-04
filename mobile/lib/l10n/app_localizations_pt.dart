// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Portuguese (`pt`).
class AppLocalizationsPt extends AppLocalizations {
  AppLocalizationsPt([String locale = 'pt']) : super(locale);

  @override
  String get appName => 'Agrocom';

  @override
  String get settings => 'Configurações';

  @override
  String get appearance => 'Aparência';

  @override
  String get theme => 'Tema';

  @override
  String get textSize => 'Tamanho do texto';

  @override
  String get capture => 'Captura';

  @override
  String get autoFlash => 'Flash automático';

  @override
  String get autoFlashSubtitle => 'Ativar flash durante a captura';

  @override
  String get unitsAndFormat => 'Unidades e formato';

  @override
  String get weightUnit => 'Unidade de peso';

  @override
  String get dateFormat => 'Formato de data';

  @override
  String get language => 'Idioma';

  @override
  String get interfaceLanguage => 'Idioma da interface';

  @override
  String get themeModeSystem => 'Seguir sistema';

  @override
  String get themeModeLight => 'Claro';

  @override
  String get themeModeDark => 'Escuro';

  @override
  String get textSizeSmall => 'Pequeno';

  @override
  String get textSizeNormal => 'Normal';

  @override
  String get textSizeLarge => 'Grande';

  @override
  String get textSizeExtraLarge => 'Extra grande';

  @override
  String get weightUnitKilograms => 'Quilogramas (kg)';

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
  String get selectTheme => 'Selecionar tema';

  @override
  String get selectTextSize => 'Tamanho do texto';

  @override
  String get selectWeightUnit => 'Selecionar unidade de peso';

  @override
  String get selectDateFormat => 'Selecionar formato de data';

  @override
  String get selectLanguage => 'Idioma';

  @override
  String get quickAccess => 'Acesso rápido';

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
  String get historyAction => 'Histórico';

  @override
  String get historySubtitle => 'Pesagens';

  @override
  String get retry => 'Tentar novamente';

  @override
  String get captureFrames => 'Captura de fotogramas';

  @override
  String get configurePermissions => 'Configurar permissões';

  @override
  String get cameraPermissionDenied =>
      'Permissão da câmera negada. Por favor, habilite nas configurações.';

  @override
  String get weightEstimation => 'Estimativa de peso';

  @override
  String get cancel => 'Cancelar';

  @override
  String generatingPdf(String cattleName) {
    return 'Gerando PDF para $cattleName...';
  }

  @override
  String get error => 'Erro';

  @override
  String unexpectedError(String error) {
    return 'Erro inesperado: $error';
  }

  @override
  String generatingCsv(String cattleName) {
    return 'Gerando CSV para $cattleName...';
  }

  @override
  String get pdfSharedSuccessfully => 'PDF compartilhado com sucesso';

  @override
  String errorSharingPdf(String error) {
    return 'Erro ao compartilhar PDF: $error';
  }

  @override
  String errorPrintingPdf(String error) {
    return 'Erro ao imprimir PDF: $error';
  }

  @override
  String errorShowingPdf(String error) {
    return 'Erro ao mostrar PDF: $error';
  }

  @override
  String csvSavedAt(String path) {
    return 'CSV salvo em: $path';
  }

  @override
  String errorSharingCsv(String error) {
    return 'Erro ao compartilhar CSV: $error';
  }

  @override
  String get noSyncHistory => 'Sem histórico de sincronização';

  @override
  String historyTitle(String cattleName) {
    return 'Histórico - $cattleName';
  }

  @override
  String get export => 'Exportar';

  @override
  String get loadingHistory => 'Carregando histórico...';

  @override
  String get errorLoadingHistory => 'Erro ao carregar histórico';

  @override
  String get unknownError => 'Erro desconhecido';

  @override
  String get noWeighingsRegistered => 'Nenhuma pesagem registrada';

  @override
  String performFirstEstimation(String cattleName) {
    return 'Realize a primeira estimativa de peso\npara ver o histórico de $cattleName';
  }

  @override
  String get detailedHistory => 'Histórico detalhado';

  @override
  String get syncStatus => 'Status de sincronização';

  @override
  String get registerAnimal => 'Registrar animal';

  @override
  String get period => 'Período';

  @override
  String get estimateAgain => 'Estimar novamente';

  @override
  String get estimateWeight => 'Estimar peso';

  @override
  String get analyzingAnimalFeatures => 'Analisando características do animal';

  @override
  String get cameraPermissionRequired =>
      'Permissão da câmera é necessária para mostrar a pré-visualização.';

  @override
  String get exportAsCsv => 'Exportar como CSV';

  @override
  String get forExcelAnalysis => 'Para análise no Excel';

  @override
  String get exportAsPdf => 'Exportar como PDF';

  @override
  String get forPrinting => 'Para impressão e compartilhamento';

  @override
  String get estimatingWeightWithAI => 'Estimando peso com IA...';

  @override
  String get requiredData => 'Dados obrigatórios';

  @override
  String get optionalData => 'Dados opcionais';

  @override
  String get earTagNumber => 'Número da brinco *';

  @override
  String get earTagExample => 'Ex: A-001';

  @override
  String get earTagRequired => 'O número da brinco é obrigatório';

  @override
  String get earTagInvalid => 'Apenas alfanumérico e hífens';

  @override
  String get birthDate => 'Data de nascimento *';

  @override
  String get selectDate => 'Selecionar data';

  @override
  String get birthDateRequired => 'A data de nascimento é obrigatória';

  @override
  String get selectBirthDate => 'Selecionar data de nascimento';

  @override
  String get accept => 'Aceitar';

  @override
  String get name => 'Nome';

  @override
  String get nameExample => 'Ex: Brownie';

  @override
  String get color => 'Cor';

  @override
  String get colorExample => 'Ex: Marrom, Preto';

  @override
  String get birthWeight => 'Peso ao nascer (kg)';

  @override
  String get birthWeightExample => 'Ex: 35';

  @override
  String get birthWeightInvalid => 'O peso deve estar entre 10-100 kg';

  @override
  String get observations => 'Observações';

  @override
  String get observationsHint => 'Notas adicionais';

  @override
  String get automaticCategory => 'Categoria automática';

  @override
  String get newAnimal => 'Novo animal';

  @override
  String get completeAnimalData => 'Complete os dados do animal';

  @override
  String get estimationCompleted => 'Estimativa concluída!';

  @override
  String get estimatedWeight => 'Peso estimado';

  @override
  String confidence(String percentage) {
    return 'Confiança: $percentage%';
  }

  @override
  String get breed => 'Raça';

  @override
  String get method => 'Método';

  @override
  String get processingTime => 'Tempo de processamento';

  @override
  String get model => 'Modelo';

  @override
  String get selectedFrame => 'Fotograma selecionado';

  @override
  String get breedRequired => 'Raça *';

  @override
  String get selectBreed => 'Selecionar raça';

  @override
  String get breedRequiredValidation => 'A raça é obrigatória';

  @override
  String get genderRequired => 'Gênero *';

  @override
  String get selectGender => 'Selecionar gênero';

  @override
  String get genderRequiredValidation => 'O gênero é obrigatório';

  @override
  String get animals => 'Animais';

  @override
  String get averageWeight => 'Peso médio';

  @override
  String get breeds => 'Raças';

  @override
  String get information => 'Informação';

  @override
  String get connectivity => 'Conectividade';

  @override
  String get online => 'Online';

  @override
  String get offline => 'Offline';

  @override
  String get pendingItems => 'Itens pendentes';

  @override
  String get automaticSync => 'Sincronização automática';

  @override
  String get active => 'Ativo';

  @override
  String get syncAutoDescription =>
      'A sincronização é executada automaticamente a cada 60 segundos quando há conexão e itens pendentes.';

  @override
  String get syncStatusTitle => 'Status de sincronização';

  @override
  String get synced => 'Sincronizado';

  @override
  String get pending => 'Pendente';

  @override
  String get errors => 'Erros';

  @override
  String get conflicts => 'Conflitos';

  @override
  String get syncNow => 'Sincronizar agora';

  @override
  String get syncing => 'Sincronizando...';

  @override
  String get noConnection => 'Sem conexão';

  @override
  String get syncedStatus => 'Sincronizado';

  @override
  String get syncError => 'Erro de sincronização';

  @override
  String get allSynced => 'Tudo sincronizado';

  @override
  String itemsWaitingSync(int count) {
    return '$count itens aguardando sincronização';
  }

  @override
  String get noPendingChanges => 'Sem alterações pendentes';

  @override
  String pendingCount(int count) {
    return '$count pendentes';
  }

  @override
  String get agoSeconds => 'Há alguns segundos';

  @override
  String agoMinutes(int minutes) {
    return '${minutes}m atrás';
  }

  @override
  String agoHours(int hours) {
    return '${hours}h atrás';
  }

  @override
  String agoDays(int days) {
    return '${days}d atrás';
  }

  @override
  String syncResultSuccess(int count) {
    return '$count itens sincronizados com sucesso';
  }

  @override
  String syncResultPartial(int synced, int total, int failed) {
    return '$synced de $total sincronizados. $failed erros.';
  }

  @override
  String syncResultConflicts(int conflicts, int synced) {
    return '$conflicts conflitos detectados. $synced sincronizados.';
  }

  @override
  String get syncResultEmpty => 'Sem itens pendentes para sincronizar';

  @override
  String get syncResultNoChanges => 'Sem alterações';

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
    return 'Erro: $failed falharam';
  }

  @override
  String get login => 'Entrar';

  @override
  String get loginTitle => 'Entrar';

  @override
  String get loginSubtitle => 'Digite suas credenciais para continuar';

  @override
  String get username => 'Usuário';

  @override
  String get usernameHint => 'Digite seu nome de usuário';

  @override
  String get usernameRequired => 'O usuário é obrigatório';

  @override
  String get password => 'Senha';

  @override
  String get passwordHint => 'Digite sua senha';

  @override
  String get passwordRequired => 'A senha é obrigatória';

  @override
  String get loggingIn => 'Entrando...';

  @override
  String get authenticationError => 'Erro de autenticação';

  @override
  String get invalidCredentials =>
      'Credenciais inválidas. Verifique seu usuário e senha.';

  @override
  String get noInternetConnection =>
      'Sem conexão à internet. Verifique sua conexão.';

  @override
  String get serverError => 'Erro do servidor';

  @override
  String get loginError => 'Erro ao fazer login';

  @override
  String get appDescription => 'Fazenda Gamelera';
}
