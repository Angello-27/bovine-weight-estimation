// frontend/src/components/organisms/CreateRole/index.js

import Box from '@mui/material/Box';
import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import TextAreaField from '../../atoms/TextAreaField';
import RadioButtonGroup from '../../atoms/RadioButtonGroup';
import CustomButton from '../../atoms/CustomButton';
import { radioButtonsRoles } from '../../../config/constants';
import BadgeIcon from '@mui/icons-material/Badge';
import DescriptionIcon from '@mui/icons-material/Description';

function CreateRole({ formData, errors = {}, onInputChange, onSubmit }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Box sx={{ px: 3, pb: 2 }}>
                <Grid container spacing={3}>
                    <InputField 
                        xs={12} 
                        label="Nombre del rol" 
                        name="name" 
                        value={formData.name || ''} 
                        onChange={onInputChange}
                        startIcon={<BadgeIcon />}
                        required
                        error={!!errors.name}
                        helperText={errors.name}
                    />
                    <TextAreaField 
                        xs={12} 
                        label="Descripción" 
                        rows={3} 
                        name="description" 
                        value={formData.description || ''} 
                        onChange={onInputChange}
                        startIcon={<DescriptionIcon />}
                        error={!!errors.description}
                        helperText={errors.description}
                    />
                    <RadioButtonGroup
                        xs={12}
                        options={radioButtonsRoles}
                        label="Nivel de acceso al sistema"
                        name="priority"
                        value={formData.priority || ''}
                        onChange={onInputChange}
                        row
                        required
                        error={!!errors.priority}
                        helperText={errors.priority}
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

export default CreateRole;
