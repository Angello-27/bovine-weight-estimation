// frontend/src/components/organisms/CattleTraceabilityTimeline/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import TimelineEvent from '../../molecules/TimelineEvent';
import EmptyState from '../../molecules/EmptyState';
import TimelineIcon from '@mui/icons-material/Timeline';
import { Box as IconBox } from '@mui/material';

function CattleTraceabilityTimeline({ events }) {
    if (!events || events.length === 0) {
        return (
            <Card>
                <EmptyState message="No hay eventos registrados para este animal." />
            </Card>
        );
    }

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <TimelineIcon color="primary" />
                <CustomTypography variant="h6">
                    Timeline de Eventos
                </CustomTypography>
            </Box>
            
            <Box>
                {events.map((event) => (
                    <TimelineEvent key={event.id} event={event} />
                ))}
            </Box>
        </Card>
    );
}

export default CattleTraceabilityTimeline;

