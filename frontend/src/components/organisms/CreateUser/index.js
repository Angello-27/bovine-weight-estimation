// frontend/src/components/organisms/CreateUser/index.js

import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from "../../atoms/ComboBox";
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import BusinessIcon from '@mui/icons-material/Business';
import DriveFileRenameOutlineIcon from '@mui/icons-material/DriveFileRenameOutline';
import AssignmentIndIcon from '@mui/icons-material/AssignmentInd';

function CreateUser({ formData, errors = {}, onInputChange, onSubmit, roles = [], farms, onComboBoxChange }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Box sx={{ px: 3, pb: 2 }}>
                <Grid container spacing={3}>
                    <InputField 
                        xs={12} 
                        label="Nombre" 
                        name="first_name" 
                        value={formData.first_name || ''} 
                        onChange={onInputChange}
                        startIcon={<DriveFileRenameOutlineIcon />}
                        error={!!errors.first_name}
                        helperText={errors.first_name}
                    />
                    <InputField 
                        xs={12} 
                        label="Apellido" 
                        name="last_name" 
                        value={formData.last_name || ''} 
                        onChange={onInputChange}
                        startIcon={<AssignmentIndIcon />}
                        error={!!errors.last_name}
                        helperText={errors.last_name}
                    />
                    <InputField 
                        xs={12} 
                        label="Email" 
                        name="email" 
                        type="email" 
                        value={formData.email || ''} 
                        onChange={onInputChange}
                        startIcon={<EmailIcon />}
                        required
                        error={!!errors.email}
                        helperText={errors.email}
                    />
                    
                    <InputField 
                        xs={12}
                        label="Nombre de usuario" 
                        name="username" 
                        value={formData.username || ''} 
                        onChange={onInputChange}
                        startIcon={<PersonIcon />}
                        required
                        error={!!errors.username}
                        helperText={errors.username}
                    />
                    <ComboBox 
                        xs={12} 
                        options={roles} 
                        label="Rol" 
                        id="combo-box-role" 
                        fieldName="roleId" 
                        onChange={onComboBoxChange} 
                        value={formData.roleId}
                        startIcon={<AdminPanelSettingsIcon />}
                        required
                        error={!!errors.roleId}
                        helperText={errors.roleId}
                    />
                    {farms && (
                        <ComboBox 
                            xs={12} 
                            options={farms} 
                            label="Hacienda (opcional)" 
                            id="combo-box-farm" 
                            fieldName="farmId" 
                            onChange={onComboBoxChange} 
                            value={formData.farmId}
                            startIcon={<BusinessIcon />}
                            error={!!errors.farmId}
                            helperText={errors.farmId}
                        />
                    )}
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

export default CreateUser;
