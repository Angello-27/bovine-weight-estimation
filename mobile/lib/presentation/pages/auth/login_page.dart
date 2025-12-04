/// Login Page
///
/// Página de inicio de sesión.
/// Permite autenticar usuarios con username y password.
///
/// Presentation Layer - Pages
library;

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/errors/failures.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/atoms/buttons/primary_button.dart';
import '../../widgets/molecules/error_state_card.dart';
import '../../widgets/molecules/loading_state_card.dart';
import 'widgets/login_form.dart';
import 'widgets/login_header.dart';
import 'widgets/login_info_card.dart';
import 'widgets/theme_toggle_button.dart';

/// Página de login
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  Timer? _errorAutoClearTimer;

  @override
  void dispose() {
    _errorAutoClearTimer?.cancel();
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin(AuthProvider provider) async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    final success = await provider.login(
      username: _usernameController.text.trim(),
      password: _passwordController.text,
    );

    if (success && mounted) {
      // Navegar a home después de login exitoso
      Navigator.of(context).pushReplacementNamed('/');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            Consumer<AuthProvider>(
              builder: (context, provider, _) {
                final l10n = AppLocalizations.of(context)!;

                // Configurar auto-limpieza de error después de 5 segundos
                if (provider.error != null) {
                  _errorAutoClearTimer?.cancel();
                  _errorAutoClearTimer = Timer(const Duration(seconds: 5), () {
                    if (mounted && provider.error != null) {
                      provider.clearError();
                    }
                  });
                } else {
                  _errorAutoClearTimer?.cancel();
                }

                if (provider.isLoading) {
                  return LoadingStateCard(message: l10n.loggingIn);
                }

                return SingleChildScrollView(
                  padding: const EdgeInsets.all(AppSpacing.screenPadding),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const SizedBox(height: AppSpacing.xxl),

                      // Header con logo y título
                      const LoginHeader(),

                      const SizedBox(height: AppSpacing.xxl),

                      // Formulario de login
                      LoginForm(
                        usernameController: _usernameController,
                        passwordController: _passwordController,
                        formKey: _formKey,
                        onLogin: () => _handleLogin(provider),
                      ),

                      const SizedBox(height: AppSpacing.xl),

                      // Botón de login
                      PrimaryButton(
                        text: l10n.login,
                        onPressed: () => _handleLogin(provider),
                      ),

                      // Error message (debajo del botón)
                      if (provider.error != null) ...[
                        const SizedBox(height: AppSpacing.md),
                        ErrorStateCard(
                          title: l10n.authenticationError,
                          message: _getErrorMessage(provider.error!, l10n),
                        ),
                      ],

                      const SizedBox(height: AppSpacing.lg),

                      // Card informativa
                      const LoginInfoCard(),
                    ],
                  ),
                );
              },
            ),
            // Botón de cambio de tema en la esquina superior derecha
            Positioned(
              top: AppSpacing.md,
              right: AppSpacing.md,
              child: const ThemeToggleButton(),
            ),
          ],
        ),
      ),
    );
  }

  String _getErrorMessage(Failure failure, AppLocalizations l10n) {
    if (failure is AuthFailure) {
      return l10n.invalidCredentials;
    } else if (failure is NetworkFailure) {
      return l10n.noInternetConnection;
    } else if (failure is ServerFailure) {
      return '${l10n.serverError}: ${failure.message}';
    }
    return '${l10n.loginError}: ${failure.message}';
  }
}
