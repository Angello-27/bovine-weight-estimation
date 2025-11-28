// src/components/atoms/CustomButton.js
import { Button } from '@mui/material';

function CustomButton({ variant, fullWidth, children, ...props }) {
    return (
        <Button variant={variant} fullWidth={fullWidth} {...props}>
            {children}
        </Button>
    );
}

export default CustomButton;
