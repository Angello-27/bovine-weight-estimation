import { Link } from "react-router-dom";
import CustomButton from "../../atoms/CustomButton";

import ArrowBackIcon from '@mui/icons-material/ArrowBack';

function ErrorActionButton({ children }) {
    return (
        <Link to="/">
            <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} startIcon={<ArrowBackIcon />} >
                {children}
            </CustomButton>
        </Link>
    );
}

export default ErrorActionButton;