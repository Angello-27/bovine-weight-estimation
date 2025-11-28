// src/components/molecules/EmailInput/index.js

import InputField from '../../atoms/InputField';

function PolygonInput({ value, onChange }) {
    return <InputField
        margin="normal"
        required
        fullWidth
        id="polygon"
        label="Nombre del Poligono"
        name="polygon"
        autoFocus
        value={value}
        onChange={onChange}
    />;
}

export default PolygonInput;
