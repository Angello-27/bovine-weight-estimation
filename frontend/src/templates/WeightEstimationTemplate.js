import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import WeightEstimationList from '../components/organisms/WeightEstimationList';
import ActionButton from '../components/molecules/ActionButton';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import AddIcon from '@mui/icons-material/Add';

function WeightEstimationTemplate({ items, loading, error, onViewClick, onEstimateClick }) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title="Estimaciones de Peso"
                    description="Historial de estimaciones de peso realizadas"
                    action={
                        <ActionButton
                            icon={<AddIcon />}
                            label="Estimar Peso"
                            onClick={onEstimateClick}
                        />
                    }
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <WeightEstimationList items={items} onViewClick={onViewClick} />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>
            </Container>
        </Grid>
    );
}

export default WeightEstimationTemplate;

