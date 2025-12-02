// frontend/src/components/organisms/CattleList/index.js

import DataTable from '../../molecules/DataTable';
import CustomIconButton from '../../atoms/IconButton';
import LinkButton from '../../atoms/LinkButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Box from '@mui/material/Box';

function CattleList({ 
    items, 
    onViewClick, 
    onEditClick, 
    onDeleteClick, 
    pagination, 
    onPageChange, 
    onPageSizeChange,
    searchable = false,
    searchValue = '',
    onSearchChange,
    searchPlaceholder = 'Buscar por caravana, nombre o raza...'
}) {
    const columns = [
        {
            label: 'Caravana',
            field: 'ear_tag',
            render: (value, row) => (
                <LinkButton
                    onClick={(e) => {
                        e.stopPropagation();
                        onViewClick && onViewClick(row.id);
                    }}
                >
                    {value || '-'}
                </LinkButton>
            )
        },
        { label: 'Nombre', field: 'name', render: (value) => value || '-' },
        { label: 'Raza', field: 'breed' },
        {
            label: 'Género',
            field: 'gender',
            render: (value) => value === 'male' ? 'Macho' : value === 'female' ? 'Hembra' : '-',
        },
        {
            label: 'Edad',
            field: 'age_months',
            render: (value) => value ? `${value} meses` : '-',
        },
        {
            label: 'Estado',
            field: 'status',
            render: (value) => {
                const statusMap = {
                    'active': 'Activo',
                    'inactive': 'Inactivo',
                    'sold': 'Vendido',
                    'deceased': 'Fallecido'
                };
                return statusMap[value] || value || '-';
            }
        },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CustomIconButton
                        icon={<EditIcon />}
                        tooltip="Editar animal"
                        color="primary"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onEditClick && onEditClick(value, row);
                        }}
                    />
                    <CustomIconButton
                        icon={<DeleteIcon />}
                        tooltip="Eliminar animal"
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
            emptyMessage="No hay animales registrados."
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
            searchable={searchable}
            searchValue={searchValue}
            onSearchChange={onSearchChange}
            searchPlaceholder={searchPlaceholder}
        />
    );
}

export default CattleList;

