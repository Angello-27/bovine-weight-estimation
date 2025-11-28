// frontend/src/containers/cattle/ManageCattleNavigation.js

import { useNavigate } from 'react-router-dom';

/**
 * ManageCattleNavigation container hook - Maneja la navegación relacionada con ganado
 * @returns {Object} { handleViewClick, handleViewFather, handleViewMother }
 */
function ManageCattleNavigation() {
    const navigate = useNavigate();

    const handleViewClick = (cattleId) => {
        navigate(`/cattle/${cattleId}`);
    };

    const handleViewFather = (fatherId) => {
        navigate(`/cattle/${fatherId}`);
    };

    const handleViewMother = (motherId) => {
        navigate(`/cattle/${motherId}`);
    };

    return {
        handleViewClick,
        handleViewFather,
        handleViewMother
    };
}

export default ManageCattleNavigation;

