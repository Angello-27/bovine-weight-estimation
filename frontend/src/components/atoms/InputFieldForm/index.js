// components/molecules/InputField/index.js
import Grid from "@mui/material/Grid";
import TextField from '@mui/material/TextField';

function InputFieldForm({ xs, md, ...props }) {
    return (
        <Grid item xs={xs} md={md}>
            <TextField
                variant="standard"
                fullWidth
                {...props}
            />
        </Grid>
    );
}

export default InputFieldForm;
