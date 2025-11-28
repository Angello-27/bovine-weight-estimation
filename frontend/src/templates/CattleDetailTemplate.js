// frontend/src/templates/CattleDetailTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from "@mui/material/Box";
import CustomTypography from '../components/atoms/CustomTypography';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import CattleInfoCard from '../components/molecules/CattleInfoCard';
import CattleTraceabilityTimeline from '../components/organisms/CattleTraceabilityTimeline';
import CattleLineageTree from '../components/organisms/CattleLineageTree';
import CattleWeightHistoryChart from '../components/organisms/CattleWeightHistoryChart';
import { useState } from 'react';

function CattleDetailTemplate({
    cattle,
    estimations,
    timelineEvents,
    chartData,
    father,
    mother,
    loading,
    error,
    onViewFather,
    onViewMother
}) {
    const [tabValue, setTabValue] = useState(0);

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title={cattle ? `Animal: ${cattle.ear_tag}` : 'Detalle del Animal'}
                    description="Información completa y trazabilidad del animal"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && cattle && (
                        <>
                            {/* Información General */}
                            <Grid container spacing={3} mb={4}>
                                <Grid item xs={12}>
                                    <CattleInfoCard cattle={cattle} />
                                </Grid>
                            </Grid>

                            {/* Tabs para diferentes secciones */}
                            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                                <Tabs value={tabValue} onChange={handleTabChange}>
                                    <Tab label="Trazabilidad" />
                                    <Tab label="Historial de Pesos" />
                                    <Tab label="Linaje" />
                                </Tabs>
                            </Box>

                            {/* Contenido de Tabs */}
                            {tabValue === 0 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <CattleTraceabilityTimeline events={timelineEvents} />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 1 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <CattleWeightHistoryChart chartData={chartData} />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 2 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <CattleLineageTree
                                            cattle={cattle}
                                            father={father}
                                            mother={mother}
                                            onViewFather={onViewFather}
                                            onViewMother={onViewMother}
                                        />
                                    </Grid>
                                </Grid>
                            )}
                        </>
                    )}
                </LoadingState>
            </Container>
        </Grid>
    );
}

export default CattleDetailTemplate;

