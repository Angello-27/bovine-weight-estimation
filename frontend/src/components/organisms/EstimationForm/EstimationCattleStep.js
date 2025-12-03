// frontend/src/components/organisms/EstimationForm/EstimationCattleStep.js

import Grid from "@mui/material/Grid";
import Card from '../../atoms/Card';
import CattleListByBreed from '../../molecules/CattleListByBreed';

function EstimationCattleStep({ cattle, selectedCattleId, onCattleSelect, breedLabel }) {
    return (
        <Grid item xs={12} md={4}>
            <Card
                sx={{
                    p: 2,
                    height: '100%',
                    minHeight: { md: '500px' },
                    maxHeight: { md: 'calc(100vh - 200px)' },
                    position: 'sticky',
                    top: 20,
                    display: 'flex',
                    flexDirection: 'column',
                }}
            >
                <CattleListByBreed
                    cattle={cattle}
                    selectedCattleId={selectedCattleId}
                    onCattleSelect={onCattleSelect}
                    breed={breedLabel}
                />
            </Card>
        </Grid>
    );
}

export default EstimationCattleStep;

