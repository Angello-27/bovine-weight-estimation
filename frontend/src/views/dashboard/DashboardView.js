import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import DashboardTemplate from '../../templates/dashboard/DashboardTemplate';
import DashboardStatsContainer from '../../containers/dashboard/DashboardStatsContainer';

function DashboardView() {
    const { stats, loading, error, refreshStats } = DashboardStatsContainer();

    return (
        <PanelTemplate content={
            <DashboardTemplate 
                stats={stats}
                loading={loading}
                error={error}
                refreshStats={refreshStats}
            />
        } />
    );
}

export default DashboardView;

