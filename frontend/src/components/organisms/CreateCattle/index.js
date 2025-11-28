// frontend/src/components/organisms/CreateCattle/index.js

import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from '../../atoms/ComboBox';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';

function CreateCattle({ formData, onInputChange, onSubmit, onComboBoxChange }) {
    const breeds = breedToComboBox();

    const genderOptions = [
        { id: 'male', label: 'Macho' },
        { id: 'female', label: 'Hembra' }
    ];

    return (
        <Grid width="100%" component="form" method="post" onSubmit={onSubmit}>
            <Grid p={3}>
                <Grid container spacing={3}>
                    {/* Campos obligatorios */}
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Caravana *" 
                        name="ear_tag" 
                        value={formData.ear_tag || ''} 
                        onChange={onInputChange}
                        required
                    />
                    <ComboBox 
                        xs={12} 
                        md={6}
                        options={breeds} 
                        label="Raza *" 
                        id="combo-box-breed" 
                        fieldName="breed" 
                        onChange={onComboBoxChange} 
                        value={formData.breed || ''}
                        required
                    />
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Fecha de Nacimiento *" 
                        name="birth_date" 
                        type="date"
                        value={formData.birth_date || ''} 
                        onChange={onInputChange}
                        InputLabelProps={{ shrink: true }}
                        required
                    />
                    <ComboBox 
                        xs={12} 
                        md={6}
                        options={genderOptions} 
                        label="Género *" 
                        id="combo-box-gender" 
                        fieldName="gender" 
                        onChange={onComboBoxChange} 
                        value={formData.gender || ''}
                        required
                    />
                    
                    {/* Campos opcionales */}
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Nombre" 
                        name="name" 
                        value={formData.name || ''} 
                        onChange={onInputChange}
                    />
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Color" 
                        name="color" 
                        value={formData.color || ''} 
                        onChange={onInputChange}
                    />
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Peso al Nacer (kg)" 
                        name="birth_weight_kg" 
                        type="number"
                        value={formData.birth_weight_kg || ''} 
                        onChange={onInputChange}
                    />
                    <InputField 
                        xs={12} 
                        label="Observaciones" 
                        name="observations" 
                        multiline 
                        rows={3} 
                        value={formData.observations || ''} 
                        onChange={onInputChange}
                    />
                </Grid>
                <Grid container item justifyContent="center" xs={12} my={4}>
                    <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
                        Guardar
                    </CustomButton>
                </Grid>
            </Grid>
        </Grid>
    );
}

export default CreateCattle;

