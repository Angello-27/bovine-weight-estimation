// frontend/src/components/atoms/ComboBox/index.js

import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { Grid } from '@mui/material';
import styled from '@emotion/styled';

const StyledAutocomplete = styled(Autocomplete)(({ theme }) => ({
    '& .MuiAutocomplete-clearIndicator': {
        padding: theme.spacing(1),// Ajusta según tus necesidades
    },
    '& .MuiAutocomplete-popupIndicator': {
        padding: theme.spacing(1),
    },
}));

function ComboBox({ xs, md, options, label, fieldName, onChange, ...props }) {
    const handleSelectionChange = (event, value) => {
        onChange(fieldName, value);  // Pasamos el fieldName junto con el valor al onChange
    };

    return (
        <Grid item xs={xs} md={md}>
            <StyledAutocomplete
                disablePortal
                options={options}
                onChange={handleSelectionChange}
                getOptionLabel={(option) => option.label}
                isOptionEqualToValue={(option, value) => option.label === value.label && option.id === value.id}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label={label}
                        variant="standard"
                        fullWidth
                        {...props}
                        sx={{
                            ...params.sx,
                            '& .MuiAutocomplete-endAdornment': {
                                top: 'calc(50% - 30px)', // Ajusta este valor según lo que necesites
                            }
                        }}
                    />
                )}
            />
        </Grid>
    );
}

export default ComboBox;

