// frontend/src/components/organisms/UserList/index.js

import DataTable from '../../molecules/DataTable';
import CustomIconButton from '../../atoms/IconButton';
import LinkButton from '../../atoms/LinkButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import { useNavigate } from 'react-router-dom';

function UserList({ items, roles, farms, onEditClick, onDeleteClick, pagination, onPageChange, onPageSizeChange }) {
    const navigate = useNavigate();
    const getRoleName = (roleId) => {
        if (!roles || !roleId) return '-';
        const role = roles.find(r => r.id === roleId);
        return role ? role.name : '-';
    };

    const getFarmName = (farmId) => {
        if (!farms || !farmId) return '-';
        const farm = farms.find(f => f.id === farmId);
        return farm ? farm.name : '-';
    };

    const getUserDisplayName = (user) => {
        if (user.first_name && user.last_name) {
            return `${user.first_name} ${user.last_name}`;
        }
        return user.first_name || user.last_name || user.username || '-';
    };

    const columns = [
        { 
            label: 'Usuario', 
            field: 'username',
            render: (value, row) => (
                <LinkButton
                    onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/users/${row.id}`);
                    }}
                >
                    {value || '-'}
                </LinkButton>
            )
        },
        { label: 'Nombre', field: 'first_name', render: (value, row) => getUserDisplayName(row) },
        { label: 'Email', field: 'email' },
        {
            label: 'Rol',
            field: 'role_id',
            render: (value) => (
                <Chip
                    label={getRoleName(value)}
                    size="small"
                    color="primary"
                    variant="outlined"
                />
            )
        },
        {
            label: 'Hacienda',
            field: 'farm_id',
            render: (value) => (
                <Chip
                    label={getFarmName(value) || '-'}
                    size="small"
                    color="secondary"
                    variant="outlined"
                />
            )
        },
        {
            label: 'Estado',
            field: 'is_active',
            render: (value) => (
                <Chip
                    label={value ? 'Activo' : 'Inactivo'}
                    size="small"
                    color={value ? 'success' : 'default'}
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
                        tooltip="Editar usuario"
                        color="primary"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            onEditClick && onEditClick(value, row);
                        }}
                    />
                    <CustomIconButton
                        icon={<DeleteIcon />}
                        tooltip="Eliminar usuario"
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
            emptyMessage="No hay usuarios registrados."
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
        />
    );
}

export default UserList;

