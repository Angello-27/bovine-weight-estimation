import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import DashboardTemplate from '../templates/DashboardTemplate';
import DashboardStatsContainer from '../containers/dashboard/DashboardStatsContainer';

function DashboardView() {
    const statsProps = DashboardStatsContainer();

    return (
        <PanelTemplate content={<DashboardTemplate {...statsProps} />} />
    );
}

export default DashboardView;

