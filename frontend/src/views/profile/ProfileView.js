// frontend/src/views/profile/ProfileView.js

import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/profile/ProfileTemplate';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import useProfileView from '../../containers/profile/useProfileView';

function ProfileView() {
    const {
        user,
        loading,
        error,
        profileFormProps,
        passwordFormProps,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = useProfileView();

    return (
        <>
            <PanelTemplate
                content={
                    <Content
                        user={user}
                        loading={loading}
                        error={error}
                        profileFormData={profileFormProps.formData}
                        profileFormErrors={profileFormProps.errors}
                        handleProfileChange={profileFormProps.handleChange}
                        handleProfileSubmit={profileFormProps.handleSubmit}
                        passwordFormData={passwordFormProps.formData}
                        passwordFormErrors={passwordFormProps.errors}
                        handlePasswordChange={passwordFormProps.handleChange}
                        handlePasswordSubmit={passwordFormProps.handleSubmit}
                        showPasswordForm={passwordFormProps.showForm}
                        onShowPasswordForm={passwordFormProps.onShowForm}
                        onClosePasswordForm={passwordFormProps.onCloseForm}
                    />
                }
            />

            <SnackbarNotification
                errorSnackbar={errorSnackbar}
                successSnackbar={successSnackbar}
                onCloseError={closeErrorSnackbar}
                onCloseSuccess={closeSuccessSnackbar}
            />
        </>
    );
}

export default ProfileView;

