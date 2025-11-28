import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/UserTemplate';
import GetAllRoles from '../containers/role/GetAllRoles';
import CreateNewUser from '../containers/user/CreateNewUser';

function UserView() {

    const rolesProps = GetAllRoles();
    const userProps = CreateNewUser(); // Usamos CreateNewUser para obtener las props

    return (
        <PanelTemplate content={<Content {...userProps} dataRol={rolesProps} />} />
    );
}

export default UserView;
