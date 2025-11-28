// frontend\src\components\molecules\PriorityForm\index.js

import Grid from "@mui/material/Grid";
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import PriorityRadioGroup from '../PriorityRadioGroup';

function PriorityForm({ data, xs, md, defaultValue, handleChange, title, ...props }) {
    return (
        <Grid item xs={xs} md={md}>
            <FormControl>
                <FormLabel id="radio-buttons">{title}</FormLabel>
                <PriorityRadioGroup data={data} defaultValue={defaultValue} handleChange={handleChange} {...props} />
            </FormControl>
        </Grid>
    );
}

export default PriorityForm;
