/// Main App - Sistema de Estimación de Peso Bovino
/// 
/// Hacienda Gamelera - Bruno Brito Macedo
/// Clean Architecture + Provider + Material Design 3
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/ui/theme/app_colors.dart';
import 'data/datasources/camera_datasource.dart';
import 'data/datasources/frame_local_datasource.dart';
import 'data/repositories/frame_repository_impl.dart';
import 'domain/usecases/capture_frames_usecase.dart';
import 'presentation/pages/capture/capture_page.dart';
import 'presentation/providers/capture_provider.dart';

void main() {
  runApp(const MyApp());
}

/// App principal
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Inicializar dependencias (Dependency Injection manual)
    // TODO: En producción, usar GetIt o similar para DI
    final cameraDataSource = CameraDataSourceImpl();
    final localDataSource = FrameLocalDataSourceImpl();
    final frameRepository = FrameRepositoryImpl(
      cameraDataSource: cameraDataSource,
      localDataSource: localDataSource,
    );
    final captureFramesUseCase = CaptureFramesUseCase(frameRepository);

    return MultiProvider(
      providers: [
        // Provider para captura de fotogramas (US-001)
        ChangeNotifierProvider(
          create: (_) => CaptureProvider(
            captureFramesUseCase: captureFramesUseCase,
          ),
        ),
        // TODO: Agregar más providers según avancemos (US-002, US-003, etc.)
      ],
      child: MaterialApp(
        title: 'Bovine Weight Estimation',
        debugShowCheckedModeBanner: false,
        
        // Tema Material Design 3
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: AppColors.primary,
            primary: AppColors.primary,
            secondary: AppColors.secondary,
            error: AppColors.error,
            surface: AppColors.surface,
            background: AppColors.background,
          ),
          
          // AppBar Theme
          appBarTheme: const AppBarTheme(
            backgroundColor: AppColors.primary,
            foregroundColor: AppColors.onPrimary,
            elevation: 2,
            centerTitle: true,
          ),
          
          // Card Theme
          cardTheme: CardTheme(
            elevation: 4,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          
          // Elevated Button Theme
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primary,
              foregroundColor: AppColors.onPrimary,
              minimumSize: const Size.fromHeight(48),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ),
        ),
        
        // Home page
        home: const HomePage(),
      ),
    );
  }
}

/// Página de inicio (placeholder)
/// TODO: Implementar HomePage completa con navegación
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Hacienda Gamelera'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo o imagen
            const Icon(
              Icons.pets,
              size: 100,
              color: AppColors.primary,
            ),
            
            const SizedBox(height: 24),
            
            const Text(
              'Sistema de Estimación\nde Peso Bovino',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            
            const SizedBox(height: 8),
            
            const Text(
              'Hacienda Gamelera',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
              ),
            ),
            
            const SizedBox(height: 48),
            
            // Botón para ir a Captura (US-001)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32),
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const CapturePage(),
                    ),
                  );
                },
                icon: const Icon(Icons.camera_alt),
                label: const Text('Capturar Fotogramas (US-001)'),
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 56),
                ),
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Placeholder para otras funcionalidades
            const Padding(
              padding: EdgeInsets.all(16.0),
              child: Text(
                'Más funcionalidades próximamente:\n'
                '• Selección de mejor fotograma (US-002)\n'
                '• Estimación de peso con IA (US-003)\n'
                '• Análisis histórico (US-004)\n'
                '• Sincronización (US-005)\n'
                '• Búsqueda avanzada (US-006)',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
