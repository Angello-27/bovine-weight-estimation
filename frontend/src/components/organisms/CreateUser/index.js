// frontend/src/components/organisms/CreateUser/index.js

import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from "../../atoms/ComboBox";

function CreateUser({ formData, onInputChange, onSubmit, roles, farms, onComboBoxChange }) {
    return (
        <Grid width="100%" component="form" method="post" onSubmit={onSubmit}>
            <Grid p={3}>
                <Grid container spacing={3}>
                    <InputField xs={12}
                        label="Nombre de usuario" name="username" value={formData.username} onChange={onInputChange} />
                    <InputField xs={12} label="Email" name="email" type="email" value={formData.email} onChange={onInputChange} />
                    <InputField xs={12} label="Contraseña" name="password" type="password" value={formData.password} onChange={onInputChange} />
                    <ComboBox xs={12} options={roles} label="Grupo de usuarios para el acceso" id="combo-box-role" fieldName="roleId" onChange={onComboBoxChange} value={formData.roleId} />
                    {farms && (
                        <ComboBox xs={12} options={farms} label="Finca (opcional)" id="combo-box-farm" fieldName="farmId" onChange={onComboBoxChange} value={formData.farmId} />
                    )}
                </Grid>
                <Grid container item justifyContent="center" xs={12} my={10}>
                    <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
                        Save
                    </CustomButton>
                </Grid>
            </Grid>
        </Grid>
    );
}

export default CreateUser;
