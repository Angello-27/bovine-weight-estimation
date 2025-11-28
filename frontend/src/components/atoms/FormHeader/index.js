import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';

const StyledAvatar = {
    margin: 1,
    backgroundColor: 'primary.main', // o cualquier color que prefieras para el tema oscuro
};

function FormHeader({ title, children }) {
    return (
        <Box className="centeredBox">  {/* Usa la clase CSS */}
            <Avatar sx={StyledAvatar}>
                {children}
            </Avatar>
            <Typography component="h1" variant="h5" >
                {title}
            </Typography>
        </Box>
    );
}

export default FormHeader;
