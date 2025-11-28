// frontend/src/components/organisms/ErrorContent/index.js

import { Box } from "@mui/material";
import ErrorImage from '../../molecules/ErrorImage';
import ErrorMessage from '../../molecules/ErrorMessage';
import ErrorActionButton from '../../molecules/ErrorActionButton';

import errorImage from '../../../assets/img/error404.png';

function ErrorContent() {
    return (
        <Box
            sx={{
                alignItems: 'center',
                display: 'flex',
                flexDirection: 'column',
                gap: 3,
            }} >
            <ErrorImage errorImage={errorImage} />
            <ErrorMessage
                title="404: La página que busca no está aquí"
                description="O bien ha intentado una ruta sospechosa o ha llegado aquí por error. Sea lo que sea, pruebe a utilizar la navegación" />
            <ErrorActionButton>
                Volver a la pagina inicial
            </ErrorActionButton>
        </Box>
    );
}

export default ErrorContent;