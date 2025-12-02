// frontend/src/components/organisms/EstimationForm/EstimationBreedStep.js

import Grid from "@mui/material/Grid";
import Card from '../../atoms/Card';
import BreedSelector from '../../molecules/BreedSelector';

function EstimationBreedStep({ selectedBreed, onBreedSelect }) {
    return (
        <Grid item xs={12}>
            <Card sx={{ p: 3 }}>
                <BreedSelector
                    selectedBreed={selectedBreed}
                    onBreedSelect={onBreedSelect}
                />
            </Card>
        </Grid>
    );
}

export default EstimationBreedStep;

