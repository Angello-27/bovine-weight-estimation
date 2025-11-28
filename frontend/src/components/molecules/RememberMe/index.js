// src/components/molecules/RememberMe/index.js

import Checkbox from '@mui/material/Checkbox';
import LabeledCheckbox from '../../atoms/LabelCheckbox';

function RememberMe({ onRememberMeChange, rememberMe }) {

    return <LabeledCheckbox
        control={<Checkbox value="remember" color="primary" onChange={onRememberMeChange} checked={rememberMe} />}
        label="Remember me"
    />;
}

export default RememberMe;
