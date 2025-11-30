import { useState } from 'react';

import { ThemeProvider } from '@mui/material/styles';
import { useTheme } from '../../../config/theme/ThemeContext';
import Header from '../Header';
import Footer from '../Footer';
import Sidebar from '../Sidebar';
import MainContainer from '../../molecules/MainContainer'
import MainContent from '../../atoms/MainContent';

function MainLayout({ menu, children }) {
    const { currentTheme } = useTheme();
    const [open, setOpen] = useState(false);

    const handleDrawerOpen = () => setOpen(true);
    const handleDrawerClose = () => setOpen(false);

    return (
        <ThemeProvider theme={currentTheme}>
            <MainContainer>
                <Header open={open} handleDrawerOpen={handleDrawerOpen} />
                <Sidebar menu={menu} open={open} handleDrawerClose={handleDrawerClose} />
                <MainContent open={open} >
                    {children}
                </MainContent>
                <Footer />
            </MainContainer>
        </ThemeProvider >
    );
}

export default MainLayout;
