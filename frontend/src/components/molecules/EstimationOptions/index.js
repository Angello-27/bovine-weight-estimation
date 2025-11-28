// frontend/src/components/molecules/EstimationOptions/index.js

import Grid from "@mui/material/Grid";
import ComboBox from '../../atoms/ComboBox';
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';

function EstimationOptions({ cattleOptions, formData, onComboBoxChange }) {
    const breeds = breedToComboBox();

    return (
        <Card>
            <CustomTypography variant="h6" mb={2}>
                Opciones (Opcional)
            </CustomTypography>
            
            <Grid container spacing={2}>
                {cattleOptions && cattleOptions.length > 0 && (
                    <ComboBox
                        xs={12}
                        options={cattleOptions}
                        label="Animal"
                        id="combo-box-cattle"
                        fieldName="cattle_id"
                        onChange={onComboBoxChange}
                        value={formData.cattle_id || ''}
                    />
                )}
                
                <ComboBox
                    xs={12}
                    options={breeds}
                    label="Raza (ayuda al modelo)"
                    id="combo-box-breed"
                    fieldName="breed"
                    onChange={onComboBoxChange}
                    value={formData.breed || ''}
                />
            </Grid>
        </Card>
    );
}

export default EstimationOptions;

