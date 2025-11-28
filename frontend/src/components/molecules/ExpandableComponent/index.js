// src/components/molecules/IframeExpandible/index.js
import { useState } from 'react';
import { Box } from '@mui/material';

import ExpandIconButton from '../../atoms/ExpandIconButton';
import expandableStyles from './Expandable';

function ExpandableComponent({ children }) {
    const [isFullscreen, setIsFullscreen] = useState(false);

    const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
    };

    const styles = expandableStyles(isFullscreen);

    return (
        <Box sx={styles}>
            {children}
            <ExpandIconButton isFullscreen={isFullscreen} toggleFullscreen={toggleFullscreen} />
        </Box>
    );
}

export default ExpandableComponent;
