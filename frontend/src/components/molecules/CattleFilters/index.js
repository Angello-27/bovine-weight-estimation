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
 * @param {Object} filters - Objeto con los valores de los filtros { breed, gender }
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
                <Grid item xs={12} md={4}>
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
                                <MenuItem key={breed.id} value={breed.label}>
                                    {breed.label}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Grid>
                
                <Grid item xs={12} md={4}>
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
            </Grid>
        </Box>
    );
}

export default CattleFilters;

