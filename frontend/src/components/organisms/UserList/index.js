// frontend/src/components/organisms/UserList/index.js

import DataTable from '../../molecules/DataTable';
import ActionButton from '../../molecules/ActionButton';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import Chip from '@mui/material/Chip';

function UserList({ items, roles, onEditClick, onDeleteClick }) {
    const getRoleName = (roleId) => {
        if (!roles || !roleId) return '-';
        const role = roles.find(r => r.id === roleId);
        return role ? role.name : '-';
    };

    const columns = [
        { label: 'Usuario', field: 'username' },
        {
            label: 'Rol',
            field: 'roleId',
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
            emptyMessage="No hay usuarios registrados."
        />
    );
}

export default UserList;

