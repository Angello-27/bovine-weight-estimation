# UI Design System - Sistema de Estimación de Peso Bovino

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Framework**: Flutter 3.x + Material Design 3  
**Metodología**: Atomic Design  

---

## 🎨 Principios de Diseño

### 1. **Contexto de Uso**
- **Usuario primario**: Ganaderos rurales (Bruno y su equipo)
- **Entorno**: Campo abierto, luz solar variable, uso con guantes
- **Dispositivos**: Smartphones Android/iOS gama media
- **Conectividad**: Offline-first (funcionalidad sin internet)

### 2. **Principios UX**
1. **Simplicidad**: Interfaz intuitiva, mínima curva de aprendizaje
2. **Feedback visual claro**: Estados visibles (cargando, éxito, error)
3. **Gestos grandes**: Botones táctiles >48dp (uso con guantes)
4. **Alto contraste**: Legibilidad bajo luz solar directa
5. **Offline-first**: Indicadores claros de estado de conexión

---

## 🏗️ Atomic Design - Jerarquía de Componentes

### Nivel 1: **Atoms (Átomos)** 
*Componentes básicos indivisibles*

```
lib/core/ui/atoms/
├── buttons/
│   ├── primary_button.dart           # Botón principal (acción primaria)
│   ├── secondary_button.dart         # Botón secundario
│   ├── icon_button.dart              # Botón solo icono
│   └── floating_action_button.dart   # FAB Material Design
│
├── text/
│   ├── heading_text.dart             # Títulos (H1, H2, H3)
│   ├── body_text.dart                # Texto de cuerpo
│   ├── caption_text.dart             # Texto pequeño/secundario
│   └── label_text.dart               # Etiquetas de formulario
│
├── inputs/
│   ├── text_field.dart               # Input de texto
│   ├── number_field.dart             # Input numérico
│   ├── dropdown.dart                 # Selector dropdown
│   ├── checkbox.dart                 # Checkbox
│   └── radio_button.dart             # Radio button
│
├── icons/
│   ├── cattle_icon.dart              # Icono de bovino
│   ├── weight_icon.dart              # Icono de peso
│   ├── camera_icon.dart              # Icono de cámara
│   └── sync_icon.dart                # Icono de sincronización
│
├── images/
│   ├── avatar_image.dart             # Imagen circular (foto animal)
│   ├── thumbnail_image.dart          # Miniatura
│   └── placeholder_image.dart        # Placeholder sin imagen
│
└── indicators/
    ├── loading_spinner.dart          # Spinner de carga
    ├── progress_bar.dart             # Barra de progreso
    ├── badge.dart                    # Badge de notificación
    └── chip.dart                     # Chip Material Design
```

---

### Nivel 2: **Molecules (Moléculas)**
*Combinación de átomos con funcionalidad específica*

```
lib/core/ui/molecules/
├── form_fields/
│   ├── labeled_text_field.dart       # Label + TextField + Error
│   ├── breed_selector.dart           # Label + Dropdown (7 razas)
│   ├── age_category_selector.dart    # Label + Dropdown (4 categorías)
│   └── date_picker_field.dart        # Label + DatePicker
│
├── cards/
│   ├── cattle_card.dart              # Card de animal (foto + nombre + raza)
│   ├── weight_record_card.dart       # Card de registro de peso
│   └── info_card.dart                # Card informativa genérica
│
├── list_items/
│   ├── cattle_list_tile.dart         # Item de lista de ganado
│   ├── weight_history_tile.dart      # Item de historial de peso
│   └── sync_status_tile.dart         # Item de estado de sync
│
├── dialogs/
│   ├── confirmation_dialog.dart      # Diálogo de confirmación
│   ├── error_dialog.dart             # Diálogo de error
│   └── loading_dialog.dart           # Diálogo de carga
│
└── feedback/
    ├── success_snackbar.dart         # Snackbar de éxito
    ├── error_snackbar.dart           # Snackbar de error
    ├── info_banner.dart              # Banner informativo
    └── empty_state.dart              # Estado vacío (sin datos)
```

---

### Nivel 3: **Organisms (Organismos)**
*Componentes complejos con lógica de negocio*

```
lib/core/ui/organisms/
├── navigation/
│   ├── app_bar_custom.dart           # AppBar con logo y acciones
│   ├── bottom_navigation_bar.dart    # Navegación inferior (4 tabs)
│   └── drawer_menu.dart              # Menú lateral (navegación)
│
├── forms/
│   ├── cattle_registration_form.dart # Formulario de registro de ganado
│   ├── weight_estimation_form.dart   # Formulario de estimación
│   └── search_filter_panel.dart      # Panel de búsqueda con filtros
│
├── lists/
│   ├── cattle_list.dart              # Lista de ganado (scroll infinito)
│   ├── weight_history_list.dart      # Lista de historial de peso
│   └── search_results_list.dart      # Lista de resultados de búsqueda
│
├── capture/
│   ├── camera_preview_widget.dart    # Vista previa de cámara en vivo
│   ├── frame_quality_overlay.dart    # Overlay de calidad de fotograma
│   └── capture_controls.dart         # Controles de captura (botones)
│
└── analysis/
    ├── weight_trend_chart.dart       # Gráfico de tendencia de peso
    ├── statistics_panel.dart         # Panel de estadísticas (GDP, etc.)
    └── anomaly_alert_card.dart       # Alerta de anomalía detectada
```

---

### Nivel 4: **Templates (Plantillas)**
*Layouts completos sin datos específicos*

```
lib/core/ui/templates/
├── scaffold_template.dart            # Scaffold con AppBar + BottomNav
├── list_template.dart                # Template de lista con búsqueda
├── detail_template.dart              # Template de detalle (foto + info)
└── form_template.dart                # Template de formulario completo
```

---

### Nivel 5: **Pages (Páginas)**
*Pantallas completas con datos y lógica*

```
lib/features/[feature]/presentation/pages/
├── home_page.dart                    # Pantalla principal
├── capture_page.dart                 # Pantalla de captura
├── cattle_list_page.dart             # Lista de ganado
├── cattle_detail_page.dart           # Detalle de animal
├── weight_estimation_page.dart       # Estimación de peso
├── analysis_page.dart                # Análisis histórico
└── settings_page.dart                # Configuración
```

---

## 🎨 Paleta de Colores (Material Design 3)

### **Tema: Ganadería Rural Boliviana**

```dart
// lib/core/ui/theme/app_colors.dart

import 'package:flutter/material.dart';

class AppColors {
  // Colores Primarios (Verde Campo/Agricultura)
  static const Color primary = Color(0xFF2E7D32);        // Verde oscuro
  static const Color primaryLight = Color(0xFF60AD5E);   // Verde claro
  static const Color primaryDark = Color(0xFF005005);    // Verde muy oscuro
  
  // Colores Secundarios (Terracota/Tierra)
  static const Color secondary = Color(0xFFD84315);      // Terracota
  static const Color secondaryLight = Color(0xFFFF7543); // Terracota claro
  static const Color secondaryDark = Color(0xFF9F0000);  // Terracota oscuro
  
  // Colores de Superficie (Neutrales)
  static const Color surface = Color(0xFFFAFAFA);        // Blanco roto
  static const Color background = Color(0xFFFFFFFF);     // Blanco
  static const Color surfaceVariant = Color(0xFFE0E0E0); // Gris claro
  
  // Colores de Texto
  static const Color onPrimary = Color(0xFFFFFFFF);      // Blanco
  static const Color onSecondary = Color(0xFFFFFFFF);    // Blanco
  static const Color onSurface = Color(0xFF212121);      // Negro suave
  static const Color onBackground = Color(0xFF212121);   // Negro suave
  
  // Colores Semánticos
  static const Color success = Color(0xFF4CAF50);        // Verde éxito
  static const Color error = Color(0xFFD32F2F);          // Rojo error
  static const Color warning = Color(0xFFFFA726);        // Naranja warning
  static const Color info = Color(0xFF1976D2);           // Azul info
  
  // Colores de Estado (Offline/Online)
  static const Color offline = Color(0xFF9E9E9E);        // Gris (offline)
  static const Color online = Color(0xFF4CAF50);         // Verde (online)
  static const Color syncing = Color(0xFF2196F3);        // Azul (sincronizando)
  
  // Colores de Raza (Opcional para diferenciar visualmente)
  static const Map<String, Color> breedColors = {
    'brahman': Color(0xFFBCAAA4),      // Beige claro (Brahman)
    'nelore': Color(0xFF8D6E63),       // Marrón claro (Nelore)
    'angus': Color(0xFF424242),        // Negro (Angus)
    'cebuinas': Color(0xFFA1887F),     // Marrón rosado (Cebuinas)
    'criollo': Color(0xFF795548),      // Marrón (Criollo)
    'pardo_suizo': Color(0xFF6D4C41),  // Marrón oscuro (Pardo Suizo)
    'jersey': Color(0xFFD7CCC8),       // Beige (Jersey)
  };
}
```

---

## 📝 Tipografía (Material Design 3)

```dart
// lib/core/ui/theme/app_typography.dart

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTypography {
  // Fuente principal: Roboto (Material Design estándar)
  // Fuente secundaria: Open Sans (mejor legibilidad en exteriores)
  
  static final TextTheme textTheme = TextTheme(
    // Display (Títulos muy grandes)
    displayLarge: GoogleFonts.roboto(
      fontSize: 57,
      fontWeight: FontWeight.bold,
      letterSpacing: -0.25,
    ),
    displayMedium: GoogleFonts.roboto(
      fontSize: 45,
      fontWeight: FontWeight.bold,
    ),
    displaySmall: GoogleFonts.roboto(
      fontSize: 36,
      fontWeight: FontWeight.bold,
    ),
    
    // Headline (Títulos de sección)
    headlineLarge: GoogleFonts.roboto(
      fontSize: 32,
      fontWeight: FontWeight.w600,
    ),
    headlineMedium: GoogleFonts.roboto(
      fontSize: 28,
      fontWeight: FontWeight.w600,
    ),
    headlineSmall: GoogleFonts.roboto(
      fontSize: 24,
      fontWeight: FontWeight.w600,
    ),
    
    // Title (Títulos de componentes)
    titleLarge: GoogleFonts.openSans(
      fontSize: 22,
      fontWeight: FontWeight.w600,
      letterSpacing: 0,
    ),
    titleMedium: GoogleFonts.openSans(
      fontSize: 16,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.15,
    ),
    titleSmall: GoogleFonts.openSans(
      fontSize: 14,
      fontWeight: FontWeight.w600,
      letterSpacing: 0.1,
    ),
    
    // Body (Texto de cuerpo)
    bodyLarge: GoogleFonts.openSans(
      fontSize: 16,
      fontWeight: FontWeight.normal,
      letterSpacing: 0.5,
    ),
    bodyMedium: GoogleFonts.openSans(
      fontSize: 14,
      fontWeight: FontWeight.normal,
      letterSpacing: 0.25,
    ),
    bodySmall: GoogleFonts.openSans(
      fontSize: 12,
      fontWeight: FontWeight.normal,
      letterSpacing: 0.4,
    ),
    
    // Label (Etiquetas de botones, chips)
    labelLarge: GoogleFonts.roboto(
      fontSize: 14,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.1,
    ),
    labelMedium: GoogleFonts.roboto(
      fontSize: 12,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.5,
    ),
    labelSmall: GoogleFonts.roboto(
      fontSize: 11,
      fontWeight: FontWeight.w500,
      letterSpacing: 0.5,
    ),
  );
}
```

---

## 📐 Spacing y Layout

```dart
// lib/core/ui/theme/app_spacing.dart

class AppSpacing {
  // Espaciado base (múltiplos de 4dp)
  static const double xs = 4.0;     // Extra small
  static const double sm = 8.0;     // Small
  static const double md = 16.0;    // Medium (estándar)
  static const double lg = 24.0;    // Large
  static const double xl = 32.0;    // Extra large
  static const double xxl = 48.0;   // Extra extra large
  
  // Padding de componentes
  static const double buttonPadding = 16.0;
  static const double cardPadding = 16.0;
  static const double screenPadding = 16.0;
  
  // Bordes redondeados
  static const double borderRadiusSmall = 4.0;
  static const double borderRadiusMedium = 8.0;
  static const double borderRadiusLarge = 16.0;
  static const double borderRadiusCircle = 999.0;
  
  // Tamaños de componentes
  static const double minButtonHeight = 48.0;  // Táctil con guantes
  static const double minTapTarget = 48.0;     // Material Design mínimo
  static const double iconSize = 24.0;
  static const double iconSizeLarge = 32.0;
  static const double avatarSize = 56.0;
  
  // Elevación (sombras)
  static const double elevationLow = 2.0;
  static const double elevationMedium = 4.0;
  static const double elevationHigh = 8.0;
}
```

---

## 🎯 Iconografía Material Design

### **Iconos Principales del Sistema**

```dart
// lib/core/ui/theme/app_icons.dart

import 'package:flutter/material.dart';

class AppIcons {
  // Navegación principal
  static const IconData home = Icons.home;
  static const IconData search = Icons.search;
  static const IconData list = Icons.list;
  static const IconData settings = Icons.settings;
  
  // Ganado
  static const IconData cattle = Icons.pets;              // Icono de animal
  static const IconData addCattle = Icons.add_circle;
  static const IconData editCattle = Icons.edit;
  static const IconData deleteCattle = Icons.delete;
  
  // Captura y Peso
  static const IconData camera = Icons.camera_alt;
  static const IconData cameraOutlined = Icons.camera_alt_outlined;
  static const IconData weight = Icons.monitor_weight;     // Icono de peso
  static const IconData estimate = Icons.calculate;
  
  // Razas (representación visual)
  static const IconData breed = Icons.category;
  static const IconData ageCategory = Icons.cake;          // Edad
  
  // Análisis
  static const IconData analytics = Icons.analytics;
  static const IconData chart = Icons.show_chart;
  static const IconData trend = Icons.trending_up;
  static const IconData anomaly = Icons.warning;
  
  // Sincronización
  static const IconData sync = Icons.sync;
  static const IconData syncOff = Icons.sync_disabled;
  static const IconData syncProblem = Icons.sync_problem;
  static const IconData cloudDone = Icons.cloud_done;
  static const IconData cloudOff = Icons.cloud_off;
  
  // Estados
  static const IconData success = Icons.check_circle;
  static const IconData error = Icons.error;
  static const IconData warning = Icons.warning_amber;
  static const IconData info = Icons.info;
  
  // Acciones
  static const IconData save = Icons.save;
  static const IconData cancel = Icons.cancel;
  static const IconData delete = Icons.delete;
  static const IconData edit = Icons.edit;
  static const IconData add = Icons.add;
  static const IconData close = Icons.close;
  
  // Reportes y Exportación
  static const IconData report = Icons.description;
  static const IconData export = Icons.file_download;
  static const IconData print = Icons.print;
  static const IconData share = Icons.share;
  
  // Entidades Regulatorias
  static const IconData senasag = Icons.verified;          // SENASAG
  static const IconData regensa = Icons.assignment;         // REGENSA
  static const IconData asocebu = Icons.emoji_events;       // ASOCEBU (competencias)
  
  // Filtros y Ordenamiento
  static const IconData filter = Icons.filter_list;
  static const IconData sort = Icons.sort;
  static const IconData dateRange = Icons.date_range;
  
  // Navegación
  static const IconData back = Icons.arrow_back;
  static const IconData forward = Icons.arrow_forward;
  static const IconData menu = Icons.menu;
  static const IconData more = Icons.more_vert;
}
```

---

## 📱 Componentes Específicos del Sistema

### 1. **Cattle Card (Tarjeta de Ganado)**

```dart
// lib/core/ui/molecules/cards/cattle_card.dart

import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_spacing.dart';

class CattleCard extends StatelessWidget {
  final String name;
  final String earTag;
  final String breed;
  final String? photoUrl;
  final double? lastWeight;
  final VoidCallback? onTap;
  
  const CattleCard({
    Key? key,
    required this.name,
    required this.earTag,
    required this.breed,
    this.photoUrl,
    this.lastWeight,
    this.onTap,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.cardPadding),
          child: Row(
            children: [
              // Foto del animal (circular)
              CircleAvatar(
                radius: 32,
                backgroundImage: photoUrl != null 
                    ? NetworkImage(photoUrl!) 
                    : null,
                child: photoUrl == null 
                    ? Icon(Icons.pets, size: 32) 
                    : null,
              ),
              const SizedBox(width: AppSpacing.md),
              
              // Información del animal
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      name,
                      style: Theme.of(context).textTheme.titleMedium,
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Text(
                      'Caravana: $earTag',
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Row(
                      children: [
                        Icon(
                          Icons.category,
                          size: 16,
                          color: AppColors.breedColors[breed.toLowerCase()],
                        ),
                        const SizedBox(width: 4),
                        Text(
                          breed,
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              
              // Último peso
              if (lastWeight != null)
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Icon(
                      Icons.monitor_weight,
                      color: AppColors.primary,
                      size: 24,
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${lastWeight!.toStringAsFixed(1)} kg',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: AppColors.primary,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## 🎯 Patrones de Navegación

### **Bottom Navigation Bar (4 Tabs)**

```dart
// Tabs principales del sistema
1. Home (Inicio)          - Icons.home
2. Capture (Capturar)     - Icons.camera_alt
3. List (Ganado)          - Icons.list
4. Analysis (Análisis)    - Icons.analytics
```

### **Flujo de Captura (US-001, US-002, US-003)**

```
1. Home Page
   ↓ [FAB Camera]
2. Capture Page (Camera Preview)
   ↓ [Capturar Botón]
3. Capturing (10-15 FPS, 3-5 seg)
   ↓ [Selección automática]
4. Frame Preview (Confirmación)
   ↓ [Estimar Peso]
5. Weight Estimation (Inferencia TFLite)
   ↓
6. Weight Result Page (Peso + Confianza)
   ↓ [Guardar]
7. Success → Back to Home
```

---

## ✅ Checklist de Implementación

Para cada componente UI que creemos, validar:

- [ ] **Atomic Design**: ¿En qué nivel está? (Atom/Molecule/Organism)
- [ ] **Material Design 3**: ¿Sigue guidelines de Material?
- [ ] **Accesibilidad**: ¿Tamaño mínimo táctil 48dp?
- [ ] **Alto contraste**: ¿Legible bajo luz solar?
- [ ] **Responsivo**: ¿Funciona en diferentes tamaños de pantalla?
- [ ] **Estados**: ¿Maneja loading/success/error?
- [ ] **Feedback visual**: ¿El usuario sabe qué está pasando?
- [ ] **Offline-first**: ¿Muestra estado de conexión?
- [ ] **Testeable**: ¿Tiene Key para widget testing?
- [ ] **Documentado**: ¿Tiene docstring explicando uso?

---

## 📚 Referencias

- [Material Design 3](https://m3.material.io/)
- [Flutter Material Components](https://docs.flutter.dev/ui/widgets/material)
- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/)
- [Google Fonts](https://fonts.google.com/)
- [Material Icons](https://fonts.google.com/icons)

---

**Última actualización**: 28 Oct 2024  
**Versión**: 1.0.0  
**Autor**: Equipo de Desarrollo - Hacienda Gamelera

