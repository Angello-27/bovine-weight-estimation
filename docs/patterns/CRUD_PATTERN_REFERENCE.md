# Guía de Referencia: Patrón CRUD Estándar

Este documento define el patrón estándar implementado para el módulo de **Haciendas (Farms)**, que debe ser seguido como referencia para implementar todos los demás módulos CRUD del sistema.

## 📋 Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Patrón de Componentes](#patrón-de-componentes)
4. [Servicios API](#servicios-api)
5. [Validación de Formularios](#validación-de-formularios)
6. [Manejo de Errores](#manejo-de-errores)
7. [Notificaciones](#notificaciones)
8. [Paginación](#paginación)
9. [Estilos y Diseño](#estilos-y-diseño)
10. [Flujo Completo del CRUD](#flujo-completo-del-crud)
11. [Checklist de Implementación](#checklist-de-implementación)

---

## 🏗️ Arquitectura General

El patrón CRUD sigue una arquitectura basada en **Atomic Design** y **Clean Architecture**:

```
View (Page) → Template → Organisms/Molecules → Atoms
     ↓
Containers (Hooks) → Services → API
```

### Separación de Responsabilidades

- **Views**: Componentes de página que orquestan la vista completa
- **Templates**: Componentes de layout específicos del módulo
- **Organisms**: Componentes complejos (listas, formularios)
- **Molecules**: Componentes intermedios (diálogos, notificaciones)
- **Atoms**: Componentes básicos (inputs, botones)
- **Containers**: Hooks que encapsulan la lógica de negocio
- **Services**: Funciones que interactúan con la API

---

## 📁 Estructura de Archivos

### Estructura Estándar para un Módulo CRUD

```
frontend/src/
├── views/
│   └── {module}/
│       ├── {Module}View.js              # Vista principal (Lista + Formulario)
│       └── {Module}DetailView.js        # Vista de detalle (opcional)
│
├── templates/
│   └── {module}/
│       ├── {Module}Template.js          # Template para lista
│       └── {Module}DetailTemplate.js    # Template para detalle (opcional)
│
├── containers/
│   └── {module}/
│       ├── GetAll{Modules}.js           # Hook para obtener lista
│       ├── CreateNew{Module}.js         # Hook para crear/editar
│       ├── Manage{Module}Form.js        # Hook para manejar formulario
│       ├── use{Module}View.js           # Hook principal de la vista
│       └── use{Module}Detail.js         # Hook para vista de detalle (opcional)
│
├── services/
│   └── {module}/
│       ├── getAll{Modules}.js           # GET /api/v1/{module}s
│       ├── get{Module}ById.js           # GET /api/v1/{module}/{id}
│       ├── create{Module}.js            # POST /api/v1/{module}
│       ├── update{Module}.js            # PUT /api/v1/{module}/{id}
│       ├── delete{Module}.js            # DELETE /api/v1/{module}/{id}
│       └── index.js                     # Exportaciones centralizadas
│
├── components/
│   └── organisms/
│       ├── {Module}List/
│       │   └── index.js                 # Componente de lista
│       └── Create{Module}/
│           └── index.js                 # Componente de formulario
│
└── utils/
    └── transformers/
        └── {entity}ToComboBox.js        # Transformador para ComboBox
```

### Ejemplo Real: Módulo de Haciendas

```
frontend/src/
├── views/farm/
│   ├── FarmView.js
│   └── FarmDetailView.js
├── templates/farm/
│   ├── FarmTemplate.js
│   └── FarmDetailTemplate.js
├── containers/farm/
│   ├── GetAllFarms.js
│   ├── CreateNewFarm.js
│   ├── ManageFarmForm.js
│   ├── useFarmView.js
│   └── useFarmDetail.js
├── services/farm/
│   ├── getAllFarms.js
│   ├── getFarmById.js
│   ├── createFarm.js
│   ├── updateFarm.js
│   ├── deleteFarm.js
│   └── index.js
└── components/organisms/
    ├── FarmList/
    │   └── index.js
    └── CreateFarm/
        └── index.js
```

---

## 🧩 Patrón de Componentes

### 1. View (Página Principal)

**Ubicación**: `views/{module}/{Module}View.js`

**Responsabilidades**:
- Orquestar todos los hooks necesarios
- Renderizar el `PanelTemplate` con el contenido
- Manejar las notificaciones (Snackbar)

**Estructura Estándar**:

```javascript
import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/{module}/{Module}Template';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import use{Module}View from '../../containers/{module}/use{Module}View';

function {Module}View() {
    const {
        {module}sProps,
        formProps,
        formActions,
        handleSubmit,
        handleConfirmDelete,
        handleViewClick,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = use{Module}View();

    return (
        <>
            <PanelTemplate content={
                <Content
                    {...{module}sProps}
                    formData={formProps.formData}
                    formErrors={formProps.errors || {}}
                    handleChange={formProps.handleChange}
                    handleSubmit={handleSubmit}
                    handleComboBoxChange={formProps.handleComboBoxChange}
                    showForm={formActions.showForm}
                    onCloseForm={formActions.handleCloseForm}
                    onCreateClick={formActions.handleCreateClick}
                    onViewClick={handleViewClick}
                    onEditClick={formActions.handleEditClick}
                    onDeleteClick={formActions.handleDeleteClick}
                    pagination={{module}sProps.pagination}
                    onPageChange={{module}sProps.onPageChange}
                    onPageSizeChange={{module}sProps.onPageSizeChange}
                    showDeleteDialog={formActions.showDeleteDialog}
                    deleteItem={formActions.deleteItem}
                    onCloseDeleteDialog={formActions.handleCloseDeleteDialog}
                    onConfirmDelete={handleConfirmDelete}
                />
            } />
            
            <SnackbarNotification
                errorSnackbar={errorSnackbar}
                successSnackbar={successSnackbar}
                onCloseError={closeErrorSnackbar}
                onCloseSuccess={closeSuccessSnackbar}
            />
        </>
    );
}

export default {Module}View;
```

### 2. Template (Layout del Módulo)

**Ubicación**: `templates/{module}/{Module}Template.js`

**Responsabilidades**:
- Definir el layout de la página
- Mostrar header con título y botón de acción
- Gestionar los diálogos (crear/editar y eliminar)
- Manejar estados de carga y error

**Estructura Estándar**:

```javascript
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Create{Module} from '../../components/organisms/Create{Module}';
import {Module}List from '../../components/organisms/{Module}List';
import CustomButton from '../../components/atoms/CustomButton';
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import ConfirmDialog from '../../components/molecules/ConfirmDialog';
import AddIcon from '@mui/icons-material/Add';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

function {Module}Template({ 
    items, 
    loading, 
    error, 
    formData,
    formErrors = {},
    handleChange, 
    handleSubmit, 
    handleComboBoxChange, 
    showForm, 
    onCloseForm, 
    onCreateClick, 
    onEditClick, 
    onDeleteClick,
    onViewClick,
    pagination,
    onPageChange,
    onPageSizeChange,
    showDeleteDialog,
    deleteItem,
    onCloseDeleteDialog,
    onConfirmDelete
}) {
    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de acción */}
                <Box sx={{ mb: 4 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                            <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                                {Module}s
                            </CustomTypography>
                        </Box>
                        <CustomButton
                            variant="contained"
                            startIcon={<AddIcon />}
                            onClick={onCreateClick}
                            sx={{ ml: 3 }}
                        >
                            Crear {Module}
                        </CustomButton>
                    </Box>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Box sx={{ width: '100%' }}>
                            <{Module}List
                                items={items}
                                onViewClick={onViewClick}
                                onEditClick={onEditClick}
                                onDeleteClick={onDeleteClick}
                                pagination={pagination}
                                onPageChange={onPageChange}
                                onPageSizeChange={onPageSizeChange}
                            />
                        </Box>
                    )}
                </LoadingState>

                {/* Dialog para crear/editar */}
                <Dialog 
                    open={showForm} 
                    onClose={onCloseForm} 
                    maxWidth="md" 
                    fullWidth
                    PaperProps={{
                        sx: {
                            borderRadius: 2,
                        }
                    }}
                >
                    <DialogTitle sx={{ pb: 3, pt: 4, px: 3 }}>
                        {formData?.id ? `Editar {Module}` : `Crear {Module}`}
                    </DialogTitle>
                    <DialogContent sx={{ px: 3, pb: 3 }}>
                        <Create{Module}
                            formData={formData}
                            errors={formErrors}
                            onInputChange={handleChange}
                            onSubmit={(e) => {
                                handleSubmit(e);
                            }}
                            onComboBoxChange={handleComboBoxChange}
                        />
                    </DialogContent>
                </Dialog>

                {/* Dialog de confirmación para eliminar */}
                <ConfirmDialog
                    open={showDeleteDialog || false}
                    onClose={onCloseDeleteDialog}
                    onConfirm={onConfirmDelete}
                    title={`Eliminar {Module}`}
                    message={deleteItem ? `¿Estás seguro de que deseas eliminar el {module} "${deleteItem.name}"? Esta acción no se puede deshacer.` : ''}
                    confirmText="Eliminar"
                    cancelText="Cancelar"
                    confirmColor="error"
                />
            </Container>
        </Box>
    );
}

export default {Module}Template;
```

### 3. Organisms: List Component

**Ubicación**: `components/organisms/{Module}List/index.js`

**Características**:
- Usa `DataTable` para mostrar los datos
- Incluye acciones: Ver, Editar, Eliminar
- Soporta paginación
- Muestra mensaje cuando no hay datos

**Estructura Estándar**:

```javascript
import DataTable from '../../molecules/DataTable';
import CustomIconButton from '../../atoms/IconButton';
import LinkButton from '../../atoms/LinkButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

function {Module}List({ items, onViewClick, onEditClick, onDeleteClick, pagination, onPageChange, onPageSizeChange }) {
    const columns = [
        { label: 'Nombre', field: 'name' },
        // ... más columnas
    ];

    const renderActions = (row) => (
        <>
            <CustomIconButton
                icon={<EditIcon />}
                onClick={() => onEditClick(row.id, row)}
                tooltip="Editar"
            />
            <CustomIconButton
                icon={<DeleteIcon />}
                onClick={() => onDeleteClick(row.id, row)}
                tooltip="Eliminar"
                color="error"
            />
        </>
    );

    return (
        <DataTable
            columns={columns}
            rows={items || []}
            renderActions={renderActions}
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
            emptyMessage={`No hay {module}s registrados`}
        />
    );
}

export default {Module}List;
```

### 4. Organisms: Form Component

**Ubicación**: `components/organisms/Create{Module}/index.js`

**Características**:
- Usa `InputFieldForm` para campos de texto
- Usa `ComboBox` para selecciones
- Valida campos requeridos
- Muestra errores de validación

**Estructura Estándar**:

```javascript
import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import ComboBox from "../../atoms/ComboBox";
import CustomButton from '../../atoms/CustomButton';
// Importar iconos necesarios

function Create{Module}({ formData, errors = {}, onInputChange, onSubmit, onComboBoxChange }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Box sx={{ px: 3, pb: 2 }}>
                <Grid container spacing={3}>
                    <InputField 
                        xs={12} 
                        label="Nombre" 
                        name="name" 
                        value={formData.name || ''} 
                        onChange={onInputChange}
                        required
                        error={!!errors.name}
                        helperText={errors.name}
                        startIcon={<Icon />}
                    />
                    {/* Más campos */}
                </Grid>
                <Box sx={{ mt: 4, mb: 2 }}>
                    <CustomButton type="submit" fullWidth variant="contained">
                        Guardar
                    </CustomButton>
                </Box>
            </Box>
        </Box>
    );
}

export default Create{Module};
```

---

## 🔌 Servicios API

### Estructura Estándar de Servicios

Todos los servicios deben seguir este patrón:

```javascript
import apiClient from '../../api/axiosClient';

/**
 * [Descripción de la función]
 * @param {Object} data - Datos necesarios
 * @returns {Promise<Object>} Respuesta del servidor
 */
const {action}{Module} = async (data) => {
    try {
        const response = await apiClient.{method}(`/{module}/{id?}`, data);
        return response.data;
    } catch (error) {
        // Extraer mensaje del backend si está disponible
        let backendMessage = null;
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
                backendMessage = detail;
            } else if (Array.isArray(detail) && detail.length > 0) {
                backendMessage = detail[0]?.msg || detail[0]?.message || String(detail[0]);
            } else if (typeof detail === 'object') {
                backendMessage = detail.message || detail.msg || String(detail);
            }
        }
        
        if (error.response && error.response.status === 400) {
            const message = backendMessage || 'Los datos proporcionados son incorrectos.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { {action}{Module} };
```

### Ejemplo: createFarm.js

```javascript
import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva hacienda
 * @param {Object} farmData - Datos de la hacienda
 * @returns {Promise<Object>} Datos de la hacienda creada
 */
const createFarm = async (farmData) => {
    try {
        const response = await apiClient.post('/farm', farmData);
        return response.data;
    } catch (error) {
        // ... manejo de errores como arriba
    }
};

export { createFarm };
```

---

## ✅ Validación de Formularios

### Patrón de Validación

**Ubicación**: `containers/{module}/CreateNew{Module}.js`

**Características**:
- Validación antes de enviar al backend
- Mensajes de error claros y específicos
- Los errores se muestran en cada campo
- Los errores se limpian cuando el usuario empieza a escribir

**Estructura Estándar**:

```javascript
const [errors, setErrors] = useState({});

const validateForm = () => {
    const newErrors = {};

    // Validar campo requerido
    if (!formData.name || formData.name.trim() === '') {
        newErrors.name = 'El nombre es requerido';
    }

    // Validar número
    if (!formData.capacity || formData.capacity === '') {
        newErrors.capacity = 'La capacidad es requerida';
    } else {
        const cap = parseInt(formData.capacity, 10);
        if (isNaN(cap) || cap < 1) {
            newErrors.capacity = 'La capacidad debe ser un número mayor a 0';
        }
    }

    // Validar rango de números
    if (!formData.latitude || formData.latitude === '') {
        newErrors.latitude = 'La latitud es requerida';
    } else {
        const lat = parseFloat(formData.latitude);
        if (isNaN(lat) || lat < -90 || lat > 90) {
            newErrors.latitude = 'La latitud debe ser un número entre -90 y 90';
        }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
};

const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
        ...prevData,
        [name]: value
    }));
    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[name]) {
        setErrors((prevErrors) => {
            const newErrors = { ...prevErrors };
            delete newErrors[name];
            return newErrors;
        });
    }
};

const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Validar antes de enviar
    if (!validateForm()) {
        return false;
    }

    try {
        // ... enviar datos
        setErrors({});
        return true;
    } catch (error) {
        throw error;
    }
};
```

### Campos Requeridos

Los campos requeridos deben tener:
- Prop `required={true}` en el componente
- Asterisco rojo y visible (`InputLabelProps` con estilos)
- Validación en `validateForm()`

**Estilos del Asterisco**:

```javascript
InputLabelProps={{
    ...customInputLabelProps,
    ...(required && {
        sx: {
            ...customInputLabelProps?.sx,
            '& .MuiInputLabel-asterisk': {
                color: 'error.main',
                fontSize: '1.5em',
                fontWeight: 'bold',
                verticalAlign: 'baseline',
                display: 'inline-block',
                lineHeight: '1em',
                transform: 'translateY(0.1em)',
                marginLeft: '2px',
            }
        }
    })
}}
```

---

## ⚠️ Manejo de Errores

### Niveles de Manejo de Errores

1. **Validación Frontend**: Antes de enviar al backend
2. **Errores de API**: En los servicios, extraer mensajes del backend
3. **Errores de Red**: Mostrar mensaje genérico
4. **Errores de Validación del Backend**: Mostrar mensajes específicos

### Patrón de Extracción de Errores

```javascript
let backendMessage = null;
if (error.response?.data?.detail) {
    const detail = error.response.data.detail;
    if (typeof detail === 'string') {
        backendMessage = detail;
    } else if (Array.isArray(detail) && detail.length > 0) {
        backendMessage = detail[0]?.msg || detail[0]?.message || String(detail[0]);
    } else if (typeof detail === 'object') {
        backendMessage = detail.message || detail.msg || String(detail);
    }
}
```

---

## 🔔 Notificaciones

### Componente SnackbarNotification

**Ubicación**: `components/molecules/SnackbarNotification/index.js`

**Uso**:

```javascript
const [errorSnackbar, setErrorSnackbar] = useState({
    open: false,
    message: ''
});
const [successSnackbar, setSuccessSnackbar] = useState({
    open: false,
    message: ''
});

// Mostrar error
showError('Mensaje de error');

// Mostrar éxito
showSuccess('Operación exitosa');

// En el render
<SnackbarNotification
    errorSnackbar={errorSnackbar}
    successSnackbar={successSnackbar}
    onCloseError={closeErrorSnackbar}
    onCloseSuccess={closeSuccessSnackbar}
/>
```

---

## 📄 Paginación

### Patrón de Paginación

**Ubicación**: `containers/{module}/GetAll{Modules}.js`

**Estructura**:

```javascript
const [page, setPage] = useState(0);
const [pageSize, setPageSize] = useState(10);
const [totalItems, setTotalItems] = useState(0);

const fetchData = async () => {
    try {
        const response = await getAll{Modules}({
            page: page + 1, // Backend usa página basada en 1
            page_size: pageSize
        });
        setItems(response.items || []);
        setTotalItems(response.total || 0);
    } catch (error) {
        setError(error.message);
    }
};

const pagination = {
    page,
    pageSize,
    totalItems,
};

const onPageChange = (event, newPage) => {
    setPage(newPage);
};

const onPageSizeChange = (event) => {
    setPageSize(parseInt(event.target.value, 10));
    setPage(0);
};
```

**Uso en DataTable**:

```javascript
<DataTable
    columns={columns}
    rows={items}
    pagination={pagination}
    onPageChange={onPageChange}
    onPageSizeChange={onPageSizeChange}
/>
```

---

## 🎨 Estilos y Diseño

### Layout Estándar

```javascript
<Box sx={{ width: '100%' }}>
    <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
        {/* Contenido */}
    </Container>
</Box>
```

### Header Estándar

```javascript
<Box sx={{ mb: 4 }}>
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Box sx={{ flex: 1 }}>
            <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                Título
            </CustomTypography>
        </Box>
        <CustomButton
            variant="contained"
            startIcon={<AddIcon />}
            onClick={onCreateClick}
            sx={{ ml: 3 }}
        >
            Crear Nuevo
        </CustomButton>
    </Box>
</Box>
```

### Diálogo Estándar

```javascript
<Dialog 
    open={showForm} 
    onClose={onCloseForm} 
    maxWidth="md" 
    fullWidth
    PaperProps={{
        sx: {
            borderRadius: 2,
        }
    }}
>
    <DialogTitle sx={{ pb: 3, pt: 4, px: 3 }}>
        {formData?.id ? 'Editar' : 'Crear'}
    </DialogTitle>
    <DialogContent sx={{ px: 3, pb: 3 }}>
        {/* Formulario */}
    </DialogContent>
</Dialog>
```

---

## 🔄 Flujo Completo del CRUD

### 1. Listar Items

```
Usuario → View → use{Module}View → GetAll{Modules} → getAll{Modules} → API → Backend
                                                                    ↓
Usuario ← View ← use{Module}View ← GetAll{Modules} ← Response ← API ← Backend
```

### 2. Crear Item

```
Usuario (click "Crear") → Manage{Module}Form (abre dialog)
    ↓
Usuario (llenar formulario) → Create{Module} (formData)
    ↓
Usuario (submit) → CreateNew{Module} (validar)
    ↓
Validación OK → create{Module} → API → Backend
    ↓
Éxito → use{Module}View (cierra dialog, muestra success, recarga)
    ↓
Error → use{Module}View (muestra error, mantiene dialog abierto)
```

### 3. Editar Item

```
Usuario (click "Editar") → Manage{Module}Form (carga datos en formData, abre dialog)
    ↓
Usuario (modificar datos) → Create{Module} (formData actualizado)
    ↓
Usuario (submit) → CreateNew{Module} (validar, usa formData.id)
    ↓
Validación OK → update{Module} → API → Backend
    ↓
Éxito → use{Module}View (cierra dialog, muestra success, recarga)
```

### 4. Eliminar Item

```
Usuario (click "Eliminar") → Manage{Module}Form (abre ConfirmDialog)
    ↓
Usuario (confirmar) → use{Module}View (handleConfirmDelete)
    ↓
delete{Module} → API → Backend
    ↓
Éxito → use{Module}View (cierra dialog, muestra success, recarga)
    ↓
Error → use{Module}View (muestra error, cierra dialog)
```

### 5. Ver Detalle

```
Usuario (click "Ver" o nombre) → use{Module}View (handleViewClick)
    ↓
Navegación → /{module}s/:id → {Module}DetailView
    ↓
use{Module}Detail → get{Module}ById → API → Backend
```

---

## ✅ Checklist de Implementación

### Fase 1: Estructura Base

- [ ] Crear estructura de carpetas (`views/`, `templates/`, `containers/`, `services/`)
- [ ] Crear servicios API (getAll, getById, create, update, delete)
- [ ] Crear servicio index.js con exportaciones centralizadas
- [ ] Crear transformers necesarios (ej: entityToComboBox)

### Fase 2: Containers (Hooks)

- [ ] Crear `GetAll{Modules}.js` con paginación
- [ ] Crear `CreateNew{Module}.js` con validación
- [ ] Crear `Manage{Module}Form.js` para gestión de formulario
- [ ] Crear `use{Module}View.js` para orquestar la vista

### Fase 3: Componentes

- [ ] Crear `{Module}List` organism con DataTable
- [ ] Crear `Create{Module}` organism con formulario
- [ ] Agregar validaciones a campos requeridos
- [ ] Agregar iconos a campos del formulario

### Fase 4: Templates y Views

- [ ] Crear `{Module}Template.js` con layout estándar
- [ ] Crear `{Module}View.js` que use el template
- [ ] Integrar notificaciones (SnackbarNotification)
- [ ] Integrar diálogos (crear/editar y eliminar)

### Fase 5: Validaciones y Errores

- [ ] Implementar validación de campos requeridos
- [ ] Agregar mensajes de error personalizados
- [ ] Implementar extracción de errores del backend
- [ ] Agregar estilos para campos requeridos (asterisco)

### Fase 6: Mejoras y Detalles

- [ ] Implementar vista de detalle (opcional)
- [ ] Agregar filtros de búsqueda (opcional)
- [ ] Agregar exportación de datos (opcional)
- [ ] Optimizar rendimiento (memoización si es necesario)

---

## 📝 Notas Importantes

### Convenciones de Nomenclatura

- **Vista**: `{Module}View.js` (PascalCase)
- **Template**: `{Module}Template.js` (PascalCase)
- **Container**: `use{Module}View.js` (camelCase con prefijo `use`)
- **Service**: `create{Module}.js` (camelCase)
- **Component**: `{Module}List/index.js` (PascalCase)

### Reglas de Validación

1. **Siempre validar en el frontend** antes de enviar al backend
2. **Extraer y mostrar** los mensajes de error del backend
3. **Limpiar errores** cuando el usuario empieza a escribir
4. **No cerrar el formulario** si hay errores de validación

### Manejo de Estado

1. **Usar hooks personalizados** para encapsular lógica
2. **Separar estado del formulario** del estado de la vista
3. **Manejar loading y error** en cada nivel apropiado
4. **Recargar datos** después de crear/editar/eliminar

### Componentes Reutilizables

- `DataTable`: Para listas con paginación
- `InputFieldForm`: Para campos de texto con iconos
- `ComboBox`: Para selecciones con autocompletado
- `CustomButton`: Para botones consistentes
- `CustomIconButton`: Para acciones en tablas
- `ConfirmDialog`: Para confirmar eliminación
- `SnackbarNotification`: Para notificaciones

---

## 🎯 Ejemplo Completo: Implementación de Haciendas

Este documento está basado en la implementación completa del módulo de **Haciendas (Farms)**. Puedes revisar los archivos en:

- `frontend/src/views/farm/FarmView.js`
- `frontend/src/templates/farm/FarmTemplate.js`
- `frontend/src/containers/farm/`
- `frontend/src/services/farm/`
- `frontend/src/components/organisms/FarmList/`
- `frontend/src/components/organisms/CreateFarm/`

---

## 📚 Referencias

- [Atomic Design](https://bradfrost.com/blog/post/atomic-web-design/)
- [Material-UI Documentation](https://mui.com/)
- [React Hooks](https://react.dev/reference/react)
- [API Integration Guide](../integration/API_INTEGRATION_GUIDE.md)

---

**Última actualización**: Diciembre 2024  
**Basado en**: Implementación del módulo de Haciendas

