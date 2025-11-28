// frontend/src/components/organisms/FarmList/index.js

import DataTable from '../../molecules/DataTable';
import ActionButton from '../../molecules/ActionButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Chip from '@mui/material/Chip';

function FarmList({ items, owners, onEditClick, onDeleteClick }) {
    const getOwnerName = (ownerId) => {
        if (!owners || !ownerId) return '-';
        const owner = owners.find(o => o.id === ownerId);
        return owner ? owner.username : '-';
    };

    const columns = [
        { label: 'Nombre', field: 'name' },
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
        { label: 'Latitud', field: 'latitude' },
        { label: 'Longitud', field: 'longitude' },
        { label: 'Capacidad', field: 'capacity' },
        { label: 'Animales', field: 'total_animals' },
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
            emptyMessage="No hay fincas registradas."
        />
    );
}

export default FarmList;

