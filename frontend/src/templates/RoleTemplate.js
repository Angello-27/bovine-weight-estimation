import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CustomTypography from '../components/atoms/CustomTypography';
import CreateRole from '../components/organisms/CreateRole';

function RoleTemplate(props) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <Grid container item justifyContent="center" xs={12} lg={8} mx="auto" textAlign="center">
                    <CustomTypography variant="h3" mb={4}>
                        Create Role
                    </CustomTypography>
                </Grid>
                <Grid container item xs={12} lg={8} sx={{ mx: "auto" }}>
                    <CreateRole
                        formData={props.formData}
                        onInputChange={props.handleChange}
                        onSubmit={props.handleSubmit}
                    />
                </Grid>
            </Container>
        </Grid>
    );
}

export default RoleTemplate
