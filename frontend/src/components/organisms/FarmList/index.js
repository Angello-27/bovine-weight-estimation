// frontend/src/components/organisms/FarmList/index.js

import DataTable from '../../molecules/DataTable';
import CustomIconButton from '../../atoms/IconButton';
import LinkButton from '../../atoms/LinkButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';

function FarmList({ items, owners, onEditClick, onDeleteClick, onViewClick, pagination, onPageChange, onPageSizeChange }) {
    const getOwnerName = (ownerId) => {
        if (!owners || !ownerId) return '-';
        const owner = owners.find(o => o.id === ownerId);
        if (!owner) return '-';
        
        // Priorizar nombre completo, luego nombre o apellido individual, finalmente username
        if (owner.first_name && owner.last_name) {
            return `${owner.first_name} ${owner.last_name}`;
        }
        return owner.first_name || owner.last_name || owner.username || '-';
    };

    const formatCoordinate = (value) => {
        if (value == null) return '-';
        return typeof value === 'number' ? value.toFixed(6) : value;
    };

    const columns = [
        { 
            label: 'Nombre', 
            field: 'name',
            render: (value, row) => (
                <LinkButton
                    onClick={(e) => {
                        e.stopPropagation();
                        onViewClick && onViewClick(row.id, row);
                    }}
                >
                    {value || '-'}
                </LinkButton>
            )
        },
        {
            label: 'Propietario',
            field: 'owner_id',
            render: (value) => (
                <Chip
                    label={getOwnerName(value)}
                    size="small"
                    color="primary"
                    variant="outlined"
                />
            )
        },
        { 
            label: 'Latitud', 
            field: 'latitude',
            render: (value) => formatCoordinate(value)
        },
        { 
            label: 'Longitud', 
            field: 'longitude',
            render: (value) => formatCoordinate(value)
        },
        { label: 'Capacidad', field: 'capacity' },
        { label: 'Animales', field: 'total_animals' },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CustomIconButton
                        icon={<EditIcon />}
                        tooltip="Editar hacienda"
                        color="primary"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onEditClick && onEditClick(value, row);
                        }}
                    />
                    <CustomIconButton
                        icon={<DeleteIcon />}
                        tooltip="Eliminar hacienda"
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
            rows={items}
            emptyMessage="No hay haciendas registradas."
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
        />
    );
}

export default FarmList;

