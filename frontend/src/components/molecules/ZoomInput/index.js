// src/components/molecules/EmailInput/index.js

import InputField from '../../atoms/InputField';

function ZoomInput({ value, onChange }) {
    return <InputField
        margin="normal"
        required
        fullWidth
        id="zoom"
        label="Zoom"
        name="zoom"
        autoFocus
        value={value}
        onChange={onChange}
    />;
}

export default ZoomInput;
