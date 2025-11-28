import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import SyncStatusTemplate from '../templates/SyncStatusTemplate';
import SyncStatusContainer from '../containers/sync/SyncStatusContainer';

function SyncStatusView() {
    const syncProps = SyncStatusContainer();

    return (
        <PanelTemplate content={<SyncStatusTemplate {...syncProps} />} />
    );
}

export default SyncStatusView;

