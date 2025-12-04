/// Auth Guard - Organism
///
/// Widget que determina la ruta inicial basado en el estado de autenticación.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../providers/auth_provider.dart';
import '../../pages/auth/login_page.dart';
import '../../pages/home/home_page.dart';

/// Widget que determina qué página mostrar basado en la autenticación
class AuthGuard extends StatefulWidget {
  const AuthGuard({super.key});

  @override
  State<AuthGuard> createState() => _AuthGuardState();
}

class _AuthGuardState extends State<AuthGuard> {
  bool _isInitializing = true;

  @override
  void initState() {
    super.initState();
    _initializeAuth();
  }

  /// Inicializa la autenticación verificando sesión existente
  Future<void> _initializeAuth() async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    // Inicializar en modo silencioso para evitar notifyListeners durante el build
    await authProvider.initialize(silent: true);

    if (mounted) {
      setState(() {
        _isInitializing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isInitializing) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Consumer<AuthProvider>(
      builder: (context, authProvider, _) {
        // Si no está autenticado, mostrar login
        if (!authProvider.isAuthenticated) {
          return const LoginPage();
        }

        // Si está autenticado, mostrar home
        return const HomePage();
      },
    );
  }
}
