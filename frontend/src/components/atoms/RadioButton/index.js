import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';

function RadioButton({ value, label, ...props }) {
    return (
        <FormControlLabel
            value={value}
            control={<Radio />}
            label={label}
            {...props} />
    );
}

export default RadioButton;