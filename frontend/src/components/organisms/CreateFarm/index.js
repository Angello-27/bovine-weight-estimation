// frontend/src/components/organisms/CreateFarm/index.js

import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from "../../atoms/ComboBox";
import BusinessIcon from '@mui/icons-material/Business';
import PersonIcon from '@mui/icons-material/Person';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import MapIcon from '@mui/icons-material/Map';
import GroupsIcon from '@mui/icons-material/Groups';

function CreateFarm({ formData, errors = {}, onInputChange, onSubmit, owners, onComboBoxChange }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Box sx={{ px: 3, pb: 2 }}>
                <Grid container spacing={3}>
                    <InputField 
                        xs={12} 
                        label="Nombre de la hacienda" 
                        name="name" 
                        value={formData.name || ''} 
                        onChange={onInputChange}
                        startIcon={<BusinessIcon />}
                        required
                        error={!!errors.name}
                        helperText={errors.name}
                    />
                    <ComboBox 
                        xs={12} 
                        options={owners} 
                        label="Propietario" 
                        id="combo-box-owner" 
                        fieldName="owner_id" 
                        onChange={onComboBoxChange} 
                        value={formData.owner_id}
                        startIcon={<PersonIcon />}
                        required
                        error={!!errors.owner_id}
                        helperText={errors.owner_id}
                    />
                    <InputField 
                        xs={6} 
                        label="Latitud" 
                        name="latitude" 
                        type="number" 
                        step="any" 
                        value={formData.latitude || ''} 
                        onChange={onInputChange}
                        startIcon={<LocationOnIcon />}
                        required
                        error={!!errors.latitude}
                        helperText={errors.latitude}
                    />
                    <InputField 
                        xs={6} 
                        label="Longitud" 
                        name="longitude" 
                        type="number" 
                        step="any" 
                        value={formData.longitude || ''} 
                        onChange={onInputChange}
                        startIcon={<MapIcon />}
                        required
                        error={!!errors.longitude}
                        helperText={errors.longitude}
                    />
                    <InputField 
                        xs={12} 
                        label="Capacidad máxima" 
                        name="capacity" 
                        type="number" 
                        value={formData.capacity || ''} 
                        onChange={onInputChange}
                        startIcon={<GroupsIcon />}
                        required
                        error={!!errors.capacity}
                        helperText={errors.capacity}
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

export default CreateFarm;

