// frontend/src/components/molecules/CattleFilters/index.js

import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import CustomTypography from '../../atoms/CustomTypography';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';

/**
 * CattleFilters molecule - Filtros para la lista de ganado
 * @param {Object} filters - Objeto con los valores de los filtros { breed, gender, status }
 * @param {Function} onChange - Callback cuando cambia un filtro (name, value)
 */
function CattleFilters({ filters, onChange }) {
    const breeds = breedToComboBox();

    const handleChange = (event) => {
        const { name, value } = event.target;
        onChange(name, value);
    };

    return (
        <Box mb={3}>
            <CustomTypography variant="subtitle2" mb={2}>
                Filtros
            </CustomTypography>
            <Grid container spacing={2}>
                <Grid item xs={12} md={3}>
                    <FormControl fullWidth>
                        <InputLabel>Raza</InputLabel>
                        <Select
                            name="breed"
                            value={filters.breed || ''}
                            label="Raza"
                            onChange={handleChange}
                        >
                            <MenuItem value="">Todas las razas</MenuItem>
                            {breeds.map((breed) => (
                                <MenuItem key={breed.id} value={breed.id}>
                                    {breed.label}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Grid>
                
                <Grid item xs={12} md={3}>
                    <FormControl fullWidth>
                        <InputLabel>Género</InputLabel>
                        <Select
                            name="gender"
                            value={filters.gender || ''}
                            label="Género"
                            onChange={handleChange}
                        >
                            <MenuItem value="">Todos</MenuItem>
                            <MenuItem value="male">Macho</MenuItem>
                            <MenuItem value="female">Hembra</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>

                <Grid item xs={12} md={3}>
                    <FormControl fullWidth>
                        <InputLabel>Estado</InputLabel>
                        <Select
                            name="status"
                            value={filters.status || ''}
                            label="Estado"
                            onChange={handleChange}
                        >
                            <MenuItem value="">Todos los estados</MenuItem>
                            <MenuItem value="active">Activo</MenuItem>
                            <MenuItem value="inactive">Inactivo</MenuItem>
                            <MenuItem value="sold">Vendido</MenuItem>
                            <MenuItem value="deceased">Fallecido</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
            </Grid>
        </Box>
    );
}

export default CattleFilters;

