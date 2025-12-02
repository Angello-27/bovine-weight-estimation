// frontend/src/components/organisms/CreateCattle/index.js

import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import DateField from '../../atoms/DateField';
import TextAreaField from '../../atoms/TextAreaField';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from '../../atoms/ComboBox';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';
import TagIcon from '@mui/icons-material/Tag';
import PetsIcon from '@mui/icons-material/Pets';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import WcIcon from '@mui/icons-material/Wc';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';
import PaletteIcon from '@mui/icons-material/Palette';
import ScaleIcon from '@mui/icons-material/Scale';
import NotesIcon from '@mui/icons-material/Notes';
import BusinessIcon from '@mui/icons-material/Business';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import { animalToComboBox } from '../../../utils/transformers/animalToComboBox';

function CreateCattle({ 
    formData, 
    errors = {}, 
    onInputChange, 
    onSubmit, 
    onComboBoxChange, 
    farms = [],
    femaleAnimals = [],
    maleAnimals = []
}) {
    const breeds = breedToComboBox();

    const genderOptions = [
        { id: 'male', label: 'Macho' },
        { id: 'female', label: 'Hembra' }
    ];

    const statusOptions = [
        { id: 'active', label: 'Activo' },
        { id: 'inactive', label: 'Inactivo' },
        { id: 'sold', label: 'Vendido' },
        { id: 'deceased', label: 'Fallecido' }
    ];

    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Box sx={{ px: 3, pb: 2 }}>
                <Grid container spacing={3}>
                    {/* Campos obligatorios */}
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Caravana" 
                        name="ear_tag" 
                        value={formData.ear_tag || ''} 
                        onChange={onInputChange}
                        startIcon={<TagIcon />}
                        required
                        error={!!errors.ear_tag}
                        helperText={errors.ear_tag}
                    />
                    <ComboBox 
                        xs={12} 
                        md={6}
                        options={breeds} 
                        label="Raza" 
                        id="combo-box-breed" 
                        fieldName="breed" 
                        onChange={onComboBoxChange} 
                        value={formData.breed || ''}
                        startIcon={<PetsIcon />}
                        required
                        error={!!errors.breed}
                        helperText={errors.breed}
                    />
                    <DateField 
                        xs={12} 
                        md={6}
                        label="Fecha de Nacimiento" 
                        name="birth_date" 
                        value={formData.birth_date || ''} 
                        onChange={onInputChange}
                        startIcon={<CalendarTodayIcon />}
                        required
                        error={!!errors.birth_date}
                        helperText={errors.birth_date}
                    />
                    <ComboBox 
                        xs={12} 
                        md={6}
                        options={genderOptions} 
                        label="Género" 
                        id="combo-box-gender" 
                        fieldName="gender" 
                        onChange={onComboBoxChange} 
                        value={formData.gender || ''}
                        startIcon={<WcIcon />}
                        required
                        error={!!errors.gender}
                        helperText={errors.gender}
                    />
                    {farms && farms.length > 0 && (
                        <ComboBox 
                            xs={12} 
                            md={6}
                            options={farms} 
                            label="Hacienda" 
                            id="combo-box-farm" 
                            fieldName="farm_id" 
                            onChange={onComboBoxChange} 
                            value={formData.farm_id || ''}
                            startIcon={<BusinessIcon />}
                            error={!!errors.farm_id}
                            helperText={errors.farm_id}
                        />
                    )}
                    <ComboBox 
                        xs={12} 
                        md={6}
                        options={statusOptions} 
                        label="Estado" 
                        id="combo-box-status" 
                        fieldName="status" 
                        onChange={onComboBoxChange} 
                        value={formData.status || 'active'}
                        startIcon={<CheckCircleIcon />}
                        error={!!errors.status}
                        helperText={errors.status}
                    />
                    
                    {/* Campos opcionales */}
                    <InputField 
                        xs={12} 
                        label="Nombre" 
                        name="name" 
                        value={formData.name || ''} 
                        onChange={onInputChange}
                        startIcon={<DriveFileRenameOutlineIcon />}
                    />
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Color" 
                        name="color" 
                        value={formData.color || ''} 
                        onChange={onInputChange}
                        startIcon={<PaletteIcon />}
                    />
                    <InputField 
                        xs={12} 
                        md={6}
                        label="Peso al Nacer (kg)" 
                        name="birth_weight_kg" 
                        type="number"
                        value={formData.birth_weight_kg || ''} 
                        onChange={onInputChange}
                        startIcon={<ScaleIcon />}
                        error={!!errors.birth_weight_kg}
                        helperText={errors.birth_weight_kg}
                    />
                    {femaleAnimals && femaleAnimals.length > 0 && (
                        <ComboBox 
                            xs={12} 
                            md={6}
                            options={animalToComboBox(femaleAnimals)} 
                            label="Madre (opcional)" 
                            id="combo-box-mother" 
                            fieldName="mother_id" 
                            onChange={onComboBoxChange} 
                            value={formData.mother_id || ''}
                            startIcon={<FamilyRestroomIcon />}
                            error={!!errors.mother_id}
                            helperText={errors.mother_id}
                        />
                    )}
                    {maleAnimals && maleAnimals.length > 0 && (
                        <ComboBox 
                            xs={12} 
                            md={6}
                            options={animalToComboBox(maleAnimals)} 
                            label="Padre (opcional)" 
                            id="combo-box-father" 
                            fieldName="father_id" 
                            onChange={onComboBoxChange} 
                            value={formData.father_id || ''}
                            startIcon={<FamilyRestroomIcon />}
                            error={!!errors.father_id}
                            helperText={errors.father_id}
                        />
                    )}
                    <TextAreaField 
                        xs={12} 
                        label="Observaciones" 
                        name="observations" 
                        rows={3} 
                        value={formData.observations || ''} 
                        onChange={onInputChange}
                        startIcon={<NotesIcon />}
                    />
                </Grid>
                <Box sx={{ mt: 4, mb: 2 }}>
                    <CustomButton type="submit" fullWidth variant="contained">
                        Guardar
                    </CustomButton>
                </Box>
            </Box>
        </Box>
    );
}

export default CreateCattle;

