import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/RoleTemplate';
import CreateNewRole from '../containers/role/CreateNewRole';

function RoleView() {

    const roleProps = CreateNewRole(); // Usamos CreateNewRole para obtener las props

    return (
        <PanelTemplate content={<Content {...roleProps} />} />
    );
}

export default RoleView;
