// frontend/src/components/organisms/EstimationForm/EstimationWizard.js

import Box from "@mui/material/Box";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import StepContent from "@mui/material/StepContent";
import { useTheme } from "@mui/material/styles";

const steps = [
    {
        label: 'Seleccionar Raza',
        description: 'Elige la raza del animal que deseas estimar'
    },
    {
        label: 'Seleccionar Animal y Estimar',
        description: 'Selecciona un animal (opcional) y sube una imagen para estimar su peso'
    }
];

function EstimationWizard({ activeStep, children, onStepClick }) {
    const theme = useTheme();

    return (
        <Box sx={{ mb: 4 }}>
            <Stepper activeStep={activeStep} orientation="vertical">
                {steps.map((step, index) => (
                    <Step key={step.label} completed={index < activeStep}>
                        <StepLabel
                            onClick={() => {
                                // Permitir click solo en el paso 1 cuando estamos en el paso 2
                                if (index === 0 && activeStep === 1 && onStepClick) {
                                    onStepClick(0);
                                }
                            }}
                            sx={{
                                '& .MuiStepLabel-label': {
                                    fontSize: '1rem',
                                    fontWeight: index === activeStep ? 600 : 500,
                                    cursor: index === 0 && activeStep === 1 ? 'pointer' : 'default',
                                    '&:hover': index === 0 && activeStep === 1 ? {
                                        color: theme.palette.primary.main,
                                        textDecoration: 'underline'
                                    } : {}
                                },
                                '& .MuiStepLabel-iconContainer .Mui-completed': {
                                    color: theme.palette.success.main,
                                },
                                '& .MuiStepLabel-iconContainer .Mui-active': {
                                    color: theme.palette.primary.main,
                                },
                            }}
                        >
                            {step.label}
                        </StepLabel>
                        <StepContent>
                            <Box sx={{ mb: 2 }}>
                                {index === activeStep && children}
                            </Box>
                        </StepContent>
                    </Step>
                ))}
            </Stepper>
        </Box>
    );
}

export default EstimationWizard;

