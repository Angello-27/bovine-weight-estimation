// frontend/src/views/farm/FarmDetailView.js
import React from 'react';
import { useParams } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import FarmDetailTemplate from '../../templates/farm/FarmDetailTemplate';
import useFarmDetail from '../../containers/farm/useFarmDetail';

function FarmDetailView() {
    const { id } = useParams();
    const farmDetailProps = useFarmDetail(id);

    return (
        <PanelTemplate content={
            <FarmDetailTemplate {...farmDetailProps} />
        } />
    );
}

export default FarmDetailView;

