// frontend/src/components/molecules/CattleListByBreed/index.js

import { useState, useMemo } from 'react';
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import Typography from "@mui/material/Typography";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import CustomTypography from '../../atoms/CustomTypography';
import CustomButton from '../../atoms/CustomButton';
import PetsIcon from '@mui/icons-material/Pets';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import IconButton from '@mui/material/IconButton';
import { useTheme } from "@mui/material/styles";

function CattleListByBreed({ cattle, selectedCattleId, onCattleSelect, breed }) {
    const theme = useTheme();
    const [searchTerm, setSearchTerm] = useState('');

    // Filtrar animales por término de búsqueda
    const filteredCattle = useMemo(() => {
        if (!cattle) return [];
        if (!searchTerm.trim()) return cattle;

        const term = searchTerm.toLowerCase();
        return cattle.filter(animal => {
            const earTag = (animal.ear_tag || '').toLowerCase();
            const name = (animal.name || '').toLowerCase();
            return earTag.includes(term) || name.includes(term);
        });
    }, [cattle, searchTerm]);

    if (!cattle || cattle.length === 0) {
        return (
            <Box>
                <CustomTypography variant="h6" sx={{ mb: 2 }}>
                    Ganado - {breed}
                </CustomTypography>
                <Box
                    sx={{
                        textAlign: 'center',
                        py: 4,
                        borderRadius: 2,
                        border: `2px dashed ${theme.palette.grey[300]}`,
                    }}
                >
                    <Box
                        sx={{
                            display: 'inline-flex',
                            p: 2,
                            borderRadius: '50%',
                            backgroundColor: theme.palette.grey[100],
                            mb: 2,
                        }}
                    >
                        <PetsIcon sx={{ fontSize: 40, color: theme.palette.grey[400] }} />
                    </Box>
                    <Typography variant="body2" color="text.primary" fontWeight={500} gutterBottom>
                        No hay ganado registrado
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                        Continúa sin seleccionar animal
                    </Typography>
                </Box>
            </Box>
        );
    }

    return (
        <Box>
            {/* Header */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <CustomTypography variant="h6">
                    Ganado - {breed}
                </CustomTypography>
                <Chip
                    label={`${cattle.length}`}
                    color="primary"
                    size="small"
                />
            </Box>

            {/* Barra de búsqueda */}
            <TextField
                fullWidth
                size="small"
                placeholder="Buscar por caravana o nombre..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <SearchIcon sx={{ color: theme.palette.grey[400], fontSize: 20 }} />
                        </InputAdornment>
                    ),
                    endAdornment: searchTerm && (
                        <InputAdornment position="end">
                            <IconButton
                                size="small"
                                onClick={() => setSearchTerm('')}
                                edge="end"
                            >
                                <ClearIcon sx={{ fontSize: 18 }} />
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
                sx={{
                    mb: 2,
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 2,
                    }
                }}
            />

            {/* Contador de resultados */}
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1.5 }}>
                {filteredCattle.length === cattle.length
                    ? `${cattle.length} animal${cattle.length !== 1 ? 'es' : ''} disponible${cattle.length !== 1 ? 's' : ''}`
                    : `${filteredCattle.length} de ${cattle.length} animal${cattle.length !== 1 ? 'es' : ''}`
                }
            </Typography>

            {/* Lista de animales con scroll */}
            <Box
                sx={{
                    maxHeight: '400px',
                    overflowY: 'auto',
                    overflowX: 'hidden',
                    pr: 0.5,
                    '&::-webkit-scrollbar': {
                        width: '6px',
                    },
                    '&::-webkit-scrollbar-track': {
                        backgroundColor: theme.palette.grey[100],
                        borderRadius: '3px',
                    },
                    '&::-webkit-scrollbar-thumb': {
                        backgroundColor: theme.palette.grey[300],
                        borderRadius: '3px',
                        '&:hover': {
                            backgroundColor: theme.palette.grey[400],
                        },
                    },
                }}
            >
                {filteredCattle.length === 0 ? (
                    <Box sx={{ textAlign: 'center', py: 4 }}>
                        <Typography variant="body2" color="text.secondary">
                            No se encontraron animales
                        </Typography>
                    </Box>
                ) : (
                    <List sx={{ p: 0 }}>
                        {filteredCattle.map((animal) => {
                            const isSelected = selectedCattleId === animal.id;
                            const isMale = animal.gender === 'male';

                            return (
                                <ListItem
                                    key={animal.id}
                                    disablePadding
                                    sx={{ mb: 1 }}
                                >
                                    <ListItemButton
                                        onClick={() => onCattleSelect(animal.id)}
                                        selected={isSelected}
                                        sx={{
                                            borderRadius: 2,
                                            border: isSelected
                                                ? `2px solid ${theme.palette.primary.main}`
                                                : `1px solid ${theme.palette.grey[200]}`,
                                            transition: 'all 0.2s ease',
                                            '&:hover': {
                                                borderColor: theme.palette.primary.main,
                                                transform: 'translateX(4px)',
                                            },
                                            px: 2,
                                            py: 1.5,
                                        }}
                                    >
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, width: '100%' }}>
                                            {/* Icono */}
                                            <Box
                                                sx={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    width: 36,
                                                    height: 36,
                                                    borderRadius: 1.5,
                                                    flexShrink: 0,
                                                }}
                                            >
                                                <PetsIcon
                                                    sx={{
                                                        fontSize: 20,
                                                        color: theme.palette.primary.main
                                                    }}
                                                />
                                            </Box>

                                            {/* Información */}
                                            <Box sx={{ flex: 1, minWidth: 0 }}>
                                                <Typography
                                                    variant="body2"
                                                    fontWeight={600}
                                                    sx={{
                                                        color: isSelected
                                                            ? theme.palette.primary.main
                                                            : theme.palette.text.primary,
                                                        overflow: 'hidden',
                                                        textOverflow: 'ellipsis',
                                                        whiteSpace: 'nowrap',
                                                    }}
                                                >
                                                    {animal.ear_tag || 'Sin caravana'}
                                                </Typography>
                                                {animal.name && (
                                                    <Typography
                                                        variant="caption"
                                                        color="text.secondary"
                                                        sx={{
                                                            display: 'block',
                                                            overflow: 'hidden',
                                                            textOverflow: 'ellipsis',
                                                            whiteSpace: 'nowrap',
                                                        }}
                                                    >
                                                        {animal.name}
                                                    </Typography>
                                                )}
                                            </Box>

                                            {/* Género */}
                                            <Box
                                                sx={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    width: 28,
                                                    height: 28,
                                                    borderRadius: '50%',
                                                    backgroundColor: isMale
                                                        ? theme.palette.info.light
                                                        : theme.palette.secondary.light,
                                                    flexShrink: 0,
                                                }}
                                            >
                                                {isMale ? (
                                                    <MaleIcon sx={{ fontSize: 16, color: theme.palette.info.dark }} />
                                                ) : (
                                                    <FemaleIcon sx={{ fontSize: 16, color: theme.palette.secondary.dark }} />
                                                )}
                                            </Box>

                                            {/* Indicador de selección */}
                                            {isSelected && (
                                                <CheckCircleIcon
                                                    sx={{
                                                        fontSize: 20,
                                                        color: theme.palette.primary.main,
                                                        flexShrink: 0,
                                                    }}
                                                />
                                            )}
                                        </Box>
                                    </ListItemButton>
                                </ListItem>
                            );
                        })}
                    </List>
                )}
            </Box>

            {/* Botón para continuar sin selección */}
            <Box sx={{ mt: 2, pt: 2, borderTop: `1px solid ${theme.palette.grey[200]}` }}>
                <CustomButton
                    variant="text"
                    onClick={() => onCattleSelect(null)}
                    size="small"
                    fullWidth
                    sx={{
                        textTransform: 'none',
                        fontSize: '0.875rem',
                    }}
                >
                    Continuar sin seleccionar
                </CustomButton>
            </Box>
        </Box>
    );
}

export default CattleListByBreed;