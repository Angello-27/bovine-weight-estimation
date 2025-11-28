// frontend/src/components/organisms/CreateFarm/index.js

import Grid from "@mui/material/Grid";
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import ComboBox from "../../atoms/ComboBox";

function CreateFarm({ formData, onInputChange, onSubmit, owners, onComboBoxChange }) {
    return (
        <Grid width="100%" component="form" method="post" onSubmit={onSubmit}>
            <Grid p={3}>
                <Grid container spacing={3}>
                    <InputField xs={12} label="Nombre de la finca" name="name" value={formData.name} onChange={onInputChange} />
                    <ComboBox xs={12} options={owners} label="Propietario" id="combo-box-owner" fieldName="owner_id" onChange={onComboBoxChange} value={formData.owner_id} />
                    <InputField xs={6} label="Latitud" name="latitude" type="number" step="any" value={formData.latitude} onChange={onInputChange} />
                    <InputField xs={6} label="Longitud" name="longitude" type="number" step="any" value={formData.longitude} onChange={onInputChange} />
                    <InputField xs={12} label="Capacidad máxima" name="capacity" type="number" value={formData.capacity} onChange={onInputChange} />
                </Grid>
                <Grid container item justifyContent="center" xs={12} my={10}>
                    <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
                        Guardar
                    </CustomButton>
                </Grid>
            </Grid>
        </Grid>
    );
}

export default CreateFarm;

