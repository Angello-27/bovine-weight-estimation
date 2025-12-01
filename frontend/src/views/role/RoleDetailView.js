// frontend/src/views/role/RoleDetailView.js
import React from 'react';
import { useParams } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import RoleDetailTemplate from '../../templates/role/RoleDetailTemplate';
import useRoleDetail from '../../containers/role/useRoleDetail';

function RoleDetailView() {
    const { id } = useParams();
    const roleDetailProps = useRoleDetail(id);

    return (
        <PanelTemplate content={
            <RoleDetailTemplate {...roleDetailProps} />
        } />
    );
}

export default RoleDetailView;

