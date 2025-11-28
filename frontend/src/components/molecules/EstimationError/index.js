// frontend/src/components/molecules/EstimationError/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import ErrorIcon from '@mui/icons-material/Error';

function EstimationError({ error }) {
    if (!error) return null;

    return (
        <Card sx={{ bgcolor: 'error.light', color: 'error.contrastText' }}>
            <Box display="flex" alignItems="center" gap={1}>
                <ErrorIcon />
                <CustomTypography variant="body1">
                    {error}
                </CustomTypography>
            </Box>
        </Card>
    );
}

export default EstimationError;

