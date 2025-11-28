import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import { useAuth } from '../services/auth/AuthContext';

function PanelTemplate({ content }) {
    const { username, role } = useAuth(); // Accedes a los datos del usuario

    if (!username && !role) return;

    return (
        <MainLayout title={username} menu={role}>
            {content}
        </MainLayout>
    );
}

export default PanelTemplate;
