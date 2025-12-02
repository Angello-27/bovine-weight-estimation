// frontend/src/components/organisms/WeightEstimationList/index.js

import DataTable from '../../molecules/DataTable';
import LinkButton from '../../atoms/LinkButton';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import { useNavigate } from 'react-router-dom';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';

function WeightEstimationList({ 
    items, 
    onViewClick, 
    pagination, 
    onPageChange, 
    onPageSizeChange
}) {
    const navigate = useNavigate();

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    const getBreedLabel = (breed) => {
        const breeds = breedToComboBox();
        const breedOption = breeds.find(b => b.id === breed);
        return breedOption?.label || breed || '-';
    };

    const getConfidenceColor = (confidence) => {
        if (!confidence) return 'default';
        if (confidence >= 0.9) return 'success';
        if (confidence >= 0.7) return 'warning';
        return 'error';
    };

    const getConfidenceLabel = (confidence) => {
        if (!confidence) return '-';
        return `${(confidence * 100).toFixed(0)}%`;
    };

    const columns = [
        {
            label: 'Fecha',
            field: 'timestamp',
            render: (value) => formatDate(value)
        },
        {
            label: 'Animal',
            field: 'animal_id',
            render: (value, row) => {
                if (!value) return '-';
                return (
                    <LinkButton
                        onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/cattle/${value}`);
                        }}
                    >
                        Ver Animal
                    </LinkButton>
                );
            }
        },
        {
            label: 'Peso Estimado',
            field: 'estimated_weight_kg',
            render: (value) => {
                const weight = value || value === 0 ? value : null;
                return weight !== null ? (
                    <Box component="span" sx={{ fontWeight: 600, color: 'primary.main' }}>
                        {weight.toFixed(1)} kg
                    </Box>
                ) : '-';
            }
        },
        {
            label: 'Raza',
            field: 'breed',
            render: (value) => getBreedLabel(value)
        },
        {
            label: 'Confianza',
            field: 'confidence',
            render: (value) => (
                <Chip
                    label={getConfidenceLabel(value)}
                    size="small"
                    color={getConfidenceColor(value)}
                    variant="outlined"
                />
            )
        },
        {
            label: 'Modelo ML',
            field: 'ml_model_version',
            render: (value) => value || '-'
        },
        {
            label: 'Tiempo (ms)',
            field: 'processing_time_ms',
            render: (value) => value ? `${value} ms` : '-'
        }
    ];

    return (
        <DataTable
            columns={columns}
            rows={items}
            emptyMessage="No hay estimaciones de peso registradas."
            pagination={pagination}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
            onRowClick={(row) => {
                if (onViewClick) {
                    onViewClick(row.id, row);
                }
            }}
        />
    );
}

export default WeightEstimationList;
