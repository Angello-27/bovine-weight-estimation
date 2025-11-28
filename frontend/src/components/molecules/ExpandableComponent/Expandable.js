// src/components/molecules/IframeExpandible/ExpandableComponent.styles.js
const expandableStyles = (isFullscreen) => ({
    top: 0,
    left: 0,
    position: isFullscreen ? 'fixed' : 'relative',
    width: isFullscreen ? '100%' : 'auto',
    height: isFullscreen ? '100vh' : 'auto',
    zIndex: isFullscreen ? 1300 : 'auto',
});

export default expandableStyles;
