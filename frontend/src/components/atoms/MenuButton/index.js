import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

function MenuButton({ open, onClick }) {
    return (
        <IconButton
            aria-label="open drawer"
            onClick={onClick}
            edge="start"
            sx={{
                padding: '12px',
                color: 'primary.main',
                ...(open && { display: 'none' })
            }}
        >
            <MenuIcon />
        </IconButton>
    );
}

export default MenuButton;
