// frontend/src/components/organisms/WeightEstimationList/index.js

import DataTable from '../../molecules/DataTable';
import LinkButton from '../../atoms/LinkButton';
import CustomIconButton from '../../atoms/IconButton';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useNavigate } from 'react-router-dom';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';

function WeightEstimationList({ 
    items, 
    onViewClick,
    onDeleteClick,
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
                const animalName = row.animal?.name;
                const animalEarTag = row.animal?.ear_tag;
                
                if (!animalName && !animalEarTag) {
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
                
                const displayText = animalEarTag 
                    ? (animalName ? `${animalEarTag} - ${animalName}` : animalEarTag)
                    : animalName;
                
                return (
                    <LinkButton
                        onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/cattle/${value}`);
                        }}
                        sx={{ textTransform: 'none' }}
                    >
                        <Typography variant="body2" component="span">
                            {displayText}
                        </Typography>
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
        },
        {
            label: 'Acciones',
            field: 'id',
            render: (value, row) => (
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CustomIconButton
                        icon={<VisibilityIcon />}
                        tooltip="Ver detalle de estimación"
                        color="primary"
                        size="small"
                        onClick={(e) => {
                            e.stopPropagation();
                            if (onViewClick && value) {
                                onViewClick(value, row);
                            }
                        }}
                    />
                    {onDeleteClick && (
                        <CustomIconButton
                            icon={<DeleteIcon />}
                            tooltip="Eliminar estimación"
                            color="error"
                            size="small"
                            onClick={(e) => {
                                e.stopPropagation();
                                if (onDeleteClick && value) {
                                    onDeleteClick(value, row);
                                }
                            }}
                        />
                    )}
                </Box>
            )
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
