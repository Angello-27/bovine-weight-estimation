# Propuesta: Alertas con Cronograma

**Objetivo**: Extender el modelo Alert para incluir funcionalidad de cronograma/calendario  
**Fecha**: 2024-12-XX  
**Estado**: Propuesta

---

## 🎯 Casos de Uso

### 1. Sesiones de Pesaje Masivo
- Programar sesión de pesaje para 50 animales el próximo viernes
- Recordatorio 1 día antes
- Recordatorio el día del evento

### 2. Tratamientos Veterinarios
- Programar vacunación para grupo de animales
- Recordatorios recurrentes (cada 3 meses)

### 3. Planificación de Rutas
- Programar visita a diferentes potreros
- Optimización de rutas basada en ubicación GPS

### 4. Eventos del Calendario
- Competencias ASOCEBU
- Ferias ganaderas
- Inspecciones

---

## 📊 Modelo Extendido

### AlertModel con Cronograma

```python
from beanie import Document, Indexed
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional

class AlertType(str, Enum):
    # Alertas automáticas
    WEIGHT_LOSS = "weight_loss"
    STAGNATION = "stagnation"
    SYSTEM = "system"
    
    # Alertas programadas (cronograma)
    SCHEDULED_WEIGHING = "scheduled_weighing"
    VETERINARY_TREATMENT = "veterinary_treatment"
    CALENDAR_EVENT = "calendar_event"
    ROUTE_PLANNING = "route_planning"
    REMINDER = "reminder"  # Genérico para recordatorios

class AlertStatus(str, Enum):
    PENDING = "pending"      # Programada, aún no enviada
    SENT = "sent"            # Enviada al usuario
    READ = "read"            # Leída por el usuario
    CANCELLED = "cancelled"  # Cancelada
    COMPLETED = "completed"  # Evento completado

class RecurrenceType(str, Enum):
    NONE = "none"           # Una sola vez
    DAILY = "daily"         # Diario
    WEEKLY = "weekly"       # Semanal
    MONTHLY = "monthly"      # Mensual
    QUARTERLY = "quarterly"  # Trimestral
    YEARLY = "yearly"       # Anual
    CUSTOM = "custom"       # Personalizado

class AlertModel(Document):
    """Modelo de alertas y notificaciones con soporte para cronograma."""
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    user_id: Indexed(UUID) = Field(..., description="ID del usuario")
    farm_id: UUID | None = Field(None, description="ID de la finca (opcional)")
    
    # Tipo y contenido
    type: AlertType = Field(..., description="Tipo de alerta")
    title: str = Field(..., description="Título de la alerta")
    message: str = Field(..., description="Mensaje de la alerta")
    status: AlertStatus = Field(default=AlertStatus.PENDING)
    
    # Cronograma (nuevo)
    scheduled_at: datetime | None = Field(
        None, 
        description="Fecha/hora programada para la alerta o evento"
    )
    recurrence: RecurrenceType = Field(
        default=RecurrenceType.NONE,
        description="Tipo de recurrencia"
    )
    recurrence_end: datetime | None = Field(
        None,
        description="Fecha de fin de recurrencia"
    )
    reminder_before_days: list[int] = Field(
        default_factory=list,
        description="Días antes del evento para enviar recordatorios (ej: [7, 1])"
    )
    
    # Relaciones (nuevo)
    related_entity_type: str | None = Field(
        None,
        description="Tipo de entidad relacionada: 'animal', 'farm', 'session'"
    )
    related_entity_id: UUID | None = Field(
        None,
        description="ID de la entidad relacionada"
    )
    
    # Ubicación (para rutas)
    location: dict | None = Field(
        None,
        description="GeoJSON Point para eventos con ubicación"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: datetime | None = None
    read_at: datetime | None = None
    completed_at: datetime | None = None
    
    class Settings:
        name = "alerts"
        indexes = [
            "user_id",
            "status",
            "type",
            "scheduled_at",  # Para consultas de cronograma
            "farm_id",
        ]
    
    def is_scheduled(self) -> bool:
        """Verifica si la alerta está programada para el futuro."""
        return (
            self.scheduled_at is not None 
            and self.scheduled_at > datetime.utcnow()
        )
    
    def should_send_reminder(self, days_before: int) -> bool:
        """Verifica si debe enviarse recordatorio X días antes."""
        if not self.scheduled_at:
            return False
        
        days_until = (self.scheduled_at - datetime.utcnow()).days
        return days_until == days_before
```

---

## 🔄 Flujo de Trabajo

### 1. Crear Evento Programado

```python
# Ejemplo: Programar sesión de pesaje masivo
alert = AlertModel(
    user_id=user_id,
    farm_id=farm_id,
    type=AlertType.SCHEDULED_WEIGHING,
    title="Sesión de Pesaje Masivo - Potrero Norte",
    message="Pesar 50 animales del potrero norte",
    scheduled_at=datetime(2024, 12, 20, 8, 0),  # 20 dic, 8 AM
    reminder_before_days=[7, 1],  # Recordatorio 7 días antes y 1 día antes
    related_entity_type="session",
    location={
        "type": "Point",
        "coordinates": [-60.797889, -15.859500]
    }
)
```

### 2. Procesar Recordatorios (Cron Job)

```python
async def process_scheduled_alerts():
    """Procesa alertas programadas y envía recordatorios."""
    now = datetime.utcnow()
    
    # Alertas que deben enviarse ahora
    alerts_to_send = await AlertModel.find(
        AlertModel.status == AlertStatus.PENDING,
        AlertModel.scheduled_at <= now
    ).to_list()
    
    # Recordatorios (X días antes)
    for alert in await AlertModel.find(
        AlertModel.status == AlertStatus.PENDING,
        AlertModel.scheduled_at > now
    ).to_list():
        for days_before in alert.reminder_before_days:
            if alert.should_send_reminder(days_before):
                await send_reminder(alert, days_before)
    
    # Enviar alertas programadas
    for alert in alerts_to_send:
        await send_alert(alert)
        alert.status = AlertStatus.SENT
        alert.sent_at = now
        await alert.save()
```

### 3. Recurrencia

```python
async def create_recurring_alert(
    base_alert: AlertModel,
    recurrence: RecurrenceType
):
    """Crea alertas recurrentes basadas en una alerta base."""
    if recurrence == RecurrenceType.NONE:
        return
    
    # Generar próximas ocurrencias
    next_date = base_alert.scheduled_at
    while next_date <= base_alert.recurrence_end:
        alert = AlertModel(
            **base_alert.model_dump(exclude={"id", "scheduled_at"}),
            scheduled_at=next_date
        )
        await alert.insert()
        
        # Calcular siguiente fecha
        if recurrence == RecurrenceType.WEEKLY:
            next_date += timedelta(weeks=1)
        elif recurrence == RecurrenceType.MONTHLY:
            next_date += timedelta(days=30)
        # ... otros tipos
```

---

## 📱 Frontend - Vista de Cronograma

### Componente: CalendarView

```javascript
// frontend/src/views/CalendarView.js
function CalendarView() {
    const [events, setEvents] = useState([]);
    
    // Cargar eventos programados
    useEffect(() => {
        getAllScheduledAlerts().then(setEvents);
    }, []);
    
    return (
        <Calendar
            events={events.map(alert => ({
                id: alert.id,
                title: alert.title,
                start: alert.scheduled_at,
                type: alert.type,
            }))}
            onEventClick={handleEventClick}
        />
    );
}
```

---

## 🎨 Beneficios

1. **Unificación**: Un solo modelo para alertas y cronograma
2. **Flexibilidad**: Soporta eventos únicos y recurrentes
3. **Recordatorios**: Sistema automático de recordatorios
4. **Integración**: Vinculado con animales, fincas, sesiones
5. **Ubicación**: Soporte GPS para planificación de rutas

---

## 📋 Implementación Sugerida

### Fase 1: Modelo Base
- [ ] Extender AlertModel con campos de cronograma
- [ ] Crear schemas (AlertCreateRequest, AlertResponse)
- [ ] Crear servicio básico (CRUD)

### Fase 2: Programación
- [ ] Endpoint para crear eventos programados
- [ ] Cron job para procesar alertas programadas
- [ ] Sistema de recordatorios

### Fase 3: Recurrencia
- [ ] Lógica de recurrencia (diario, semanal, etc.)
- [ ] Generación automática de eventos recurrentes

### Fase 4: Frontend
- [ ] Vista de calendario
- [ ] Formulario de creación de eventos
- [ ] Notificaciones push

---

**Conclusión**: Extender Alert con cronograma es una excelente idea que unifica alertas automáticas y programación de eventos en un solo modelo coherente.

