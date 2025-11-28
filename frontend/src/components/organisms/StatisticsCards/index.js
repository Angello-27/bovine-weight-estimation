// frontend/src/components/organisms/StatisticsCards/index.js

import Grid from "@mui/material/Grid";
import StatCard from '../../molecules/StatCard';

function StatisticsCards({ stats }) {
    return (
        <Grid container spacing={3}>
            <StatCard label="Total Animales" value={stats?.totalCattle} />
            <StatCard label="Peso Promedio" value={stats?.averageWeight} unit="kg" />
            <StatCard label="Razas" value={stats?.totalBreeds} />
            <StatCard label="Estimaciones" value={stats?.totalEstimations} />
        </Grid>
    );
}

export default StatisticsCards;

