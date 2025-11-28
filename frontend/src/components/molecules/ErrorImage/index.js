// frontend/src/components/molecules/ErrorImage/index.js

import { Box } from "@mui/material";
import CustomImage from "../../atoms/CustomImage";

function ErrorImage({ errorImage }) {
    return (
        <Box sx={{ textAlign: 'center' }}>
            <CustomImage
                src={errorImage}
                style={{
                    display: 'inline-block',
                    maxWidth: '100%',
                    width: 'auto',
                }}
            />
        </Box>
    );
}

export default ErrorImage;