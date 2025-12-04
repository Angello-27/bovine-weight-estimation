/// Login Form - Organism
///
/// Formulario de login con campos de usuario y contraseña.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';

/// Formulario de login
class LoginForm extends StatefulWidget {
  final TextEditingController usernameController;
  final TextEditingController passwordController;
  final GlobalKey<FormState> formKey;
  final VoidCallback onLogin;

  const LoginForm({
    super.key,
    required this.usernameController,
    required this.passwordController,
    required this.formKey,
    required this.onLogin,
  });

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  bool _obscurePassword = true;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Form(
      key: widget.formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Campo de usuario
          TextFormField(
            controller: widget.usernameController,
            decoration: InputDecoration(
              labelText: l10n.username,
              hintText: l10n.usernameHint,
            ),
            keyboardType: TextInputType.text,
            textInputAction: TextInputAction.next,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return l10n.usernameRequired;
              }
              return null;
            },
          ),

          const SizedBox(height: AppSpacing.md),

          // Campo de contraseña
          TextFormField(
            controller: widget.passwordController,
            decoration: InputDecoration(
              labelText: l10n.password,
              hintText: l10n.passwordHint,
              suffixIcon: IconButton(
                icon: Icon(
                  _obscurePassword ? Icons.visibility : Icons.visibility_off,
                ),
                onPressed: () {
                  setState(() {
                    _obscurePassword = !_obscurePassword;
                  });
                },
              ),
            ),
            keyboardType: TextInputType.visiblePassword,
            obscureText: _obscurePassword,
            textInputAction: TextInputAction.done,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return l10n.passwordRequired;
              }
              return null;
            },
            onFieldSubmitted: (_) => widget.onLogin(),
          ),
        ],
      ),
    );
  }
}
