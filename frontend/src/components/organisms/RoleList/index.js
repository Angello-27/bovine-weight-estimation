// frontend/src/components/organisms/RoleList/index.js

import DataTable from '../../molecules/DataTable';
import CustomIconButton from '../../atoms/IconButton';
import LinkButton from '../../atoms/LinkButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import { useNavigate } from 'react-router-dom';

function RoleList({ items, onEditClick, onDeleteClick, pagination, onPageChange, onPageSizeChange }) {
    const navigate = useNavigate();
    const getPriorityLabel = (priority) => {
        const labels = {
            'Administrador': 'Administrador',
            'Usuario': 'Usuario',
            'Invitado': 'Invitado'
        };
        return labels[priority] || priority;
    };

    const getPriorityColor = (priority) => {
        const colors = {
            'Administrador': 'error',
            'Usuario': 'primary',
            'Invitado': 'default'
        };
        return colors[priority] || 'default';
    };

    const columns = [
        { 
            label: 'Nombre', 
            field: 'name',
            render: (value, row) => (
                <LinkButton
                    onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/roles/${row.id}`);
                    }}
                >
                    {value || '-'}
                </LinkButton>
            )
        },
        { label: 'Descripción', field: 'description' },
        {
            label: 'Nivel de Acceso',
            field: 'priority',
            render: (value) => (
                <Chip
                    label={getPriorityLabel(value)}
                    size="small"
                    color={getPriorityColor(value)}
                    variant="outlined"
                />
            )
        },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CustomIconButton
                        icon={<EditIcon />}
                        tooltip="Editar rol"
                        color="primary"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onEditClick && onEditClick(value, row);
                        }}
                    />
                    <CustomIconButton
                        icon={<DeleteIcon />}
                        tooltip="Eliminar rol"
                        color="error"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onDeleteClick && onDeleteClick(value, row);
                        }}
                    />
                </Box>
            ),
        },
    ];

    return (
        <DataTable
            columns={columns}
            rows={items || []}
            emptyMessage="No hay roles registrados."
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
        />
    );
}

export default RoleList;

