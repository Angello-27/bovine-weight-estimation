// frontend/src/views/user/UserDetailView.js
import React from 'react';
import { useParams } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import UserDetailTemplate from '../../templates/user/UserDetailTemplate';
import useUserDetail from '../../containers/user/useUserDetail';

      function UserDetailView() {
          const { id } = useParams();
          const { user, ownedFarms, stats, loading, error, userId } = useUserDetail(id);

          return (
              <PanelTemplate content={
                  <UserDetailTemplate 
                      user={user}
                      ownedFarms={ownedFarms}
                      stats={stats}
                      loading={loading}
                      error={error}
                      userId={userId}
                  />
              } />
          );
      }

export default UserDetailView;

