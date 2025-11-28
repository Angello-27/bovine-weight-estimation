// src/components/molecules/EmailInput/index.js

import InputField from '../../atoms/InputField';

function EmailInput({ value, onChange }) {
    return <InputField
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        autoFocus
        value={value}
        onChange={onChange}
    />;
}

export default EmailInput;
