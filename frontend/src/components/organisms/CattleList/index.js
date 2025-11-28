// frontend/src/components/organisms/CattleList/index.js

import DataTable from '../../molecules/DataTable';
import ActionButton from '../../molecules/ActionButton';
import VisibilityIcon from '@mui/icons-material/Visibility';

function CattleList({ items, onViewClick }) {
    const columns = [
        { label: 'Caravana', field: 'ear_tag' },
        { label: 'Nombre', field: 'name' },
        { label: 'Raza', field: 'breed' },
        {
            label: 'Género',
            field: 'gender',
            render: (value) => value === 'male' ? 'Macho' : 'Hembra',
        },
        {
            label: 'Edad',
            field: 'age_months',
            render: (value) => value ? `${value} meses` : '-',
        },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <ActionButton
                    icon={<VisibilityIcon />}
                    label="Ver"
                    onClick={(e) => {
                        e.stopPropagation();
                        onViewClick && onViewClick(value);
                    }}
                    variant="outlined"
                    size="small"
                />
            ),
        },
    ];

    return (
        <DataTable
            columns={columns}
            rows={items}
            onRowClick={(row) => onViewClick && onViewClick(row.id)}
            emptyMessage="No hay animales registrados."
        />
    );
}

export default CattleList;

