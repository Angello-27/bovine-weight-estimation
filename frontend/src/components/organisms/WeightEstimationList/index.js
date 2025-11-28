// frontend/src/components/organisms/WeightEstimationList/index.js

import DataTable from '../../molecules/DataTable';
import ActionButton from '../../molecules/ActionButton';
import Chip from '@mui/material/Chip';
import VisibilityIcon from '@mui/icons-material/Visibility';

function WeightEstimationList({ items, onViewClick }) {
    const getConfidenceColor = (score) => {
        if (score >= 0.9) return 'success';
        if (score >= 0.7) return 'warning';
        return 'error';
    };

    const columns = [
        {
            label: 'Fecha',
            field: 'timestamp',
            render: (value) => value ? new Date(value).toLocaleDateString() : '-',
        },
        {
            label: 'Peso (kg)',
            field: 'estimated_weight',
            render: (value) => <strong>{value?.toFixed(1) || '-'}</strong>,
        },
        {
            label: 'Confianza',
            field: 'confidence_score',
            render: (value) => (
                <Chip
                    label={`${(value * 100).toFixed(0)}%`}
                    color={getConfidenceColor(value)}
                    size="small"
                />
            ),
        },
        { label: 'Raza', field: 'breed' },
        {
            label: 'Método',
            field: 'method',
            render: (value) => value || 'tflite',
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
            emptyMessage="No hay estimaciones registradas."
        />
    );
}

export default WeightEstimationList;

