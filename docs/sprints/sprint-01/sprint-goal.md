# Sprint 1 - Sprint Goal

## Información del Sprint

**Duración**: 2 semanas  
**Fecha inicio**: 30 septiembre 2024  
**Fecha fin**: 13 octubre 2024  
**Scrum Master**: Rodrigo Escobar Morón  
**Product Owner**: Miguel Angel Escobar Lazcano  
**Cliente**: Bruno Brito Macedo (Hacienda Gamelera)

## Contexto del Proyecto

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Escala**: 500 cabezas de ganado bovino  
**Razas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey

**Problema actual**: Método tradicional requiere 2-3 días para 20 animales con error 5-20 kg  
**Objetivo**: Sistema IA con precisión >95% y tiempo <2 horas para 20 animales

## Sprint Goal

**"Validar que la captura continua de fotogramas y estimación de peso por IA funciona en condiciones reales de campo con Bruno Brito Macedo en Hacienda Gamelera, logrando precisión >95% con al menos 3 razas principales."**

## Objetivos Específicos

### 1. Validar Captura Continua

- **Objetivo**: Confirmar que la captura de 10-15 FPS durante 3-5 segundos es práctica en campo
- **Criterio de éxito**: Bruno puede capturar fotogramas de bovinos sin dificultad
- **Validación**: Demo en Hacienda Gamelera con condiciones reales

### 2. Validar Precisión ML

- **Objetivo**: Confirmar que la estimación de peso por IA es más precisa que fórmula Schaeffer
- **Criterio de éxito**: Precisión >95% con al menos 3 razas principales
- **Validación**: Comparación directa con método actual de Bruno

### 3. Validar Usabilidad

- **Objetivo**: Confirmar que la interfaz es intuitiva para personal rural
- **Criterio de éxito**: Bruno puede usar la app sin entrenamiento formal
- **Validación**: Usuario puede completar flujo completo sin ayuda

## User Stories del Sprint

### US-001: Captura Continua de Fotogramas

**Story Points**: 8  
**Prioridad**: Crítica

### US-002: Estimación de Peso por Raza

**Story Points**: 13  
**Prioridad**: Crítica

### US-003: Registro Automático de Animales

**Story Points**: 5  
**Prioridad**: Alta

**Total Story Points**: 26

## Criterios de Éxito del Sprint

### Técnicos

- [ ] App móvil funciona en dispositivos de Bruno
- [ ] Captura continua implementada y estable
- [ ] Modelo ML procesa al menos 3 razas (Brahman, Nelore, Angus)
- [ ] Precisión >95% en condiciones controladas
- [ ] Tiempo de procesamiento <3 segundos

### Criterios de Negocio

- [ ] Bruno puede usar la app sin entrenamiento
- [ ] Captura funciona en condiciones de campo reales
- [ ] Precisión es superior a fórmula Schaeffer
- [ ] Tiempo de pesaje se reduce significativamente
- [ ] Bruno está satisfecho con la solución

### Validación

- [ ] Demo exitosa en Hacienda Gamelera
- [ ] Feedback positivo de Bruno Brito Macedo
- [ ] Métricas de precisión validadas
- [ ] Casos de uso reales probados
- [ ] Próximos pasos claros definidos

## Riesgos Identificados

### Alto Impacto

1. **Precisión ML insuficiente**: Modelo no alcanza >95% precisión
   - **Mitigación**: Tener modelo de respaldo y ajustes rápidos
2. **Usabilidad en campo**: Interfaz no es práctica para condiciones rurales
   - **Mitigación**: Testing temprano con Bruno y ajustes iterativos
3. **Rendimiento en dispositivos**: App no funciona bien en smartphones de Bruno
   - **Mitigación**: Testing en dispositivos reales desde inicio

### Medio Impacto

1. **Conectividad limitada**: Problemas con funcionamiento offline
   - **Mitigación**: Enfoque offline-first desde diseño
2. **Condiciones climáticas**: App no funciona bien en clima tropical
   - **Mitigación**: Testing en condiciones reales de campo

## Plan de Validación

### Semana 1: Desarrollo y Testing Interno

- **Día 1-2**: Implementación captura continua
- **Día 3-4**: Implementación estimación ML
- **Día 5**: Testing interno y refinamiento

### Semana 2: Validación con Bruno Brito Macedo

- **Día 1**: Demo inicial en Hacienda Gamelera
- **Día 2-3**: Testing en condiciones reales de campo
- **Día 4**: Feedback y ajustes
- **Día 5**: Validación final y retrospectiva

## Métricas de Seguimiento

### Técnicas

- **Precisión ML**: % de precisión por raza
- **Tiempo procesamiento**: Segundos por estimación
- **Tasa de éxito captura**: % de capturas exitosas
- **Rendimiento app**: Tiempo de respuesta

### Métricas de Negocio

- **Satisfacción Bruno**: Escala 1-10
- **Facilidad de uso**: Tiempo para completar tarea
- **Comparación con método actual**: Tiempo ahorrado
- **Intención de adopción**: Bruno quiere continuar?

## Definición de Éxito

El Sprint 1 es exitoso cuando:

1. **Bruno Brito Macedo puede usar la app para estimar peso de bovinos en condiciones reales de campo**
2. **La precisión de estimación es >95% para al menos 3 razas principales**
3. **El tiempo de procesamiento es <3 segundos por estimación**
4. **Bruno confirma que la solución es superior al método actual**
5. **El equipo tiene claridad sobre próximos pasos para Sprint 2**

## Próximos Pasos (Sprint 2)

Basado en resultados de Sprint 1:

- **Si exitoso**: Implementar funcionalidades completas (historial, sincronización, reportes)
- **Si parcialmente exitoso**: Ajustar según feedback y continuar con validación
- **Si no exitoso**: Revisar enfoque técnico y pivotar según sea necesario

---

**Nota**: Este Sprint Goal se actualiza diariamente durante el Daily Scrum según progreso y aprendizajes del equipo.
