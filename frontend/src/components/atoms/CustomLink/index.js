// src/components/atoms/CustomLink.js
import { Link } from '@mui/material';

function CustomLink({ children, ...props }) {
    return (
        <Link
            variant="body2"
            {...props}>
            {children}
        </Link>
    );
}

export default CustomLink;
