// frontend/src/components/organisms/CreateRole/index.js

import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import PriorityForm from "../../molecules/PriorityForm";
import { radioButtonsRoles } from '../../../config/constants'

function CreateRole({ formData, onInputChange, onSubmit }) {

    return (
        <Grid width="100%" component="form" method="post" onSubmit={onSubmit}>
            <Grid p={3}>
                <Grid container spacing={3}>
                    <InputField xs={12} label="Nombre del rol" name="name" value={formData.name} onChange={onInputChange} />
                    <InputField xs={12} label="Descripcion" multiline rows={3} name="descripcion" value={formData.descripcion} onChange={onInputChange} />
                    <PriorityForm data={radioButtonsRoles} xs={12} defaultValue={formData.priority} handleChange={onInputChange} title="Nivel de acceso al sistema" name="priority" row />
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

export default CreateRole;
