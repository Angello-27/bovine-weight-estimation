// frontend\src\templates\UserTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CustomTypography from '../components/atoms/CustomTypography';
import CreateUser from '../components/organisms/CreateUser';

import { roleToComboBox } from '../utils/transformers/roleToComboBox.js';

function UserTemplate(props) {
    const transformedRole = roleToComboBox(props.dataRol.items);

    return (
        <Grid component="section" py={12}>
            <Container>
                <Grid container item justifyContent="center" xs={12} lg={8} mx="auto" textAlign="center">
                    <CustomTypography variant="h3" mb={4}>
                        Create New User
                    </CustomTypography>
                </Grid>
                <Grid container item xs={12} lg={8} sx={{ mx: "auto" }}>
                    <CreateUser
                        formData={props.formData}
                        onInputChange={props.handleChange}
                        onSubmit={props.handleSubmit}
                        roles={transformedRole}
                        onComboBoxChange={props.handleComboBoxChange}
                    />
                </Grid>
            </Container>
        </Grid>
    );
}

export default UserTemplate;
