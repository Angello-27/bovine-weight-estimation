// src/components/atoms/LabeledCheckbox/index.js

import FormControlLabel from '@mui/material/FormControlLabel';

function LabelCheckbox({ control, label, ...props }) {
    return (
        <FormControlLabel
            control={control}
            label={label}
            {...props}
        />
    );
}

export default LabelCheckbox;
