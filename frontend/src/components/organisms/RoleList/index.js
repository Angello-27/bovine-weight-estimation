// frontend/src/components/organisms/RoleList/index.js

import DataTable from '../../molecules/DataTable';
import ActionButton from '../../molecules/ActionButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

function RoleList({ items, onEditClick, onDeleteClick }) {
    const getPriorityLabel = (priority) => {
        const labels = {
            'Administrador': 'Administrador',
            'Usuario': 'Usuario',
            'Invitado': 'Invitado'
        };
        return labels[priority] || priority;
    };

    const columns = [
        { label: 'Nombre', field: 'name' },
        { label: 'Descripción', field: 'descripcion' },
        {
            label: 'Nivel de Acceso',
            field: 'priority',
            render: (value) => getPriorityLabel(value)
        },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <>
                    <ActionButton
                        icon={<EditIcon />}
                        label="Editar"
                        onClick={(e) => {
                            e.stopPropagation();
                            onEditClick && onEditClick(value, row);
                        }}
                        variant="outlined"
                        size="small"
                        sx={{ mr: 1 }}
                    />
                    <ActionButton
                        icon={<DeleteIcon />}
                        label="Eliminar"
                        onClick={(e) => {
                            e.stopPropagation();
                            onDeleteClick && onDeleteClick(value, row);
                        }}
                        variant="outlined"
                        color="error"
                        size="small"
                    />
                </>
            ),
        },
    ];

    return (
        <DataTable
            columns={columns}
            rows={items}
            emptyMessage="No hay roles registrados."
        />
    );
}

export default RoleList;

