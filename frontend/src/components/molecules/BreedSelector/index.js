// frontend/src/components/molecules/BreedSelector/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { useTheme } from "@mui/material/styles";
import CustomTypography from '../../atoms/CustomTypography';

const breeds = [
    { id: 'nelore', label: 'Nelore', image: '/nelore.jpg' },
    { id: 'brahman', label: 'Brahman', image: '/brahman.jpg' },
    { id: 'guzerat', label: 'Guzerat', image: '/guzerat.webp' },
    { id: 'senepol', label: 'Senepol', image: '/senepol.jpg' },
    { id: 'girolando', label: 'Girolando', image: '/girolando.webp' },
    { id: 'gyr_lechero', label: 'Gyr Lechero', image: '/gyr_lechero.jpg' },
    { id: 'sindi', label: 'Sindi', image: '/sindi.webp' }
];

function BreedSelector({ selectedBreed, onBreedSelect }) {
    const theme = useTheme();

    return (
        <Box>
            <CustomTypography variant="h6" sx={{ mb: 3 }}>
                Selecciona la Raza del Animal
            </CustomTypography>
            <Grid container spacing={2.5}>
                {breeds.map((breed) => {
                    const isSelected = selectedBreed === breed.id;
                    
                    return (
                        <Grid item xs={6} sm={4} md={3} key={breed.id}>
                            <Card
                                onClick={() => onBreedSelect(breed.id)}
                                sx={{
                                    cursor: 'pointer',
                                    position: 'relative',
                                    overflow: 'hidden',
                                    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                                    border: isSelected 
                                        ? `2px solid ${theme.palette.primary.main}` 
                                        : `2px solid ${theme.palette.grey[300]}`,
                                    borderRadius: 2,
                                    boxShadow: isSelected 
                                        ? `0 8px 24px ${theme.palette.primary.main}25` 
                                        : '0 2px 8px rgba(0,0,0,0.08)',
                                    '&:hover': {
                                        transform: 'translateY(-6px)',
                                        boxShadow: isSelected
                                            ? `0 12px 32px ${theme.palette.primary.main}35`
                                            : '0 8px 20px rgba(0,0,0,0.15)',
                                        borderColor: isSelected 
                                            ? theme.palette.primary.main 
                                            : theme.palette.primary.light,
                                        '& .breed-image': {
                                            transform: 'scale(1.08)',
                                        },
                                    },
                                    height: '100%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                }}
                            >
                                {/* Indicador de selección */}
                                {isSelected && (
                                    <Box
                                        sx={{
                                            position: 'absolute',
                                            top: 12,
                                            right: 12,
                                            zIndex: 2,
                                            backgroundColor: theme.palette.primary.main,
                                            borderRadius: '50%',
                                            width: 36,
                                            height: 36,
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                                        }}
                                    >
                                        <CheckCircleIcon sx={{ color: 'white', fontSize: 22 }} />
                                    </Box>
                                )}

                                {/* Contenedor de imagen con aspect ratio fijo */}
                                <Box
                                    sx={{
                                        position: 'relative',
                                        width: '100%',
                                        paddingTop: '75%', // Aspect ratio 4:3 (más alto que antes)
                                        overflow: 'hidden',
                                        backgroundColor: theme.palette.grey[100],
                                    }}
                                >
                                    <CardMedia
                                        component="img"
                                        image={breed.image}
                                        alt={breed.label}
                                        className="breed-image"
                                        sx={{
                                            position: 'absolute',
                                            top: 0,
                                            left: 0,
                                            width: '100%',
                                            height: '100%',
                                            objectFit: 'cover',
                                            objectPosition: 'center',
                                            transition: 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                                        }}
                                        onError={(e) => {
                                            e.target.src = '/cattle.jpeg';
                                        }}
                                    />
                                    
                                    {/* Overlay gradiente sutil en la parte inferior */}
                                    <Box
                                        sx={{
                                            position: 'absolute',
                                            bottom: 0,
                                            left: 0,
                                            right: 0,
                                            height: '40%',
                                            background: 'linear-gradient(to top, rgba(0,0,0,0.3), transparent)',
                                            pointerEvents: 'none',
                                        }}
                                    />
                                </Box>

                                {/* Sección de texto más compacta */}
                                <CardContent 
                                    sx={{ 
                                        flexGrow: 0,
                                        p: 1.5,
                                        textAlign: 'center',
                                        backgroundColor: isSelected 
                                            ? `${theme.palette.primary.main}08` 
                                            : 'transparent',
                                        transition: 'background-color 0.3s ease',
                                    }}
                                >
                                    <CustomTypography  
                                        customVariant="sectionTitle" 
                                        sx={{
                                            fontWeight: isSelected ? 600 : 500,
                                            transition: 'all 0.3s ease',
                                        }}
                                    >
                                        {breed.label}
                                    </CustomTypography>
                                </CardContent>
                            </Card>
                        </Grid>
                    );
                })}
            </Grid>
        </Box>
    );
}

export default BreedSelector;