import CustomTypography from "../../atoms/CustomTypography";
import { useTheme } from '@mui/material/styles'; // Importa useTheme

function ErrorMessage({ title, description }) {
    const theme = useTheme(); // Usa el hook para obtener el tema

    return (
        <div>
            <CustomTypography
                align="center"
                sx={{
                    mb: 3,
                    fontWeight: 'bold', // Establece el texto en negrita
                    fontSize: {
                        xs: theme.typography.h5.fontSize, // Para móviles y dispositivos pequeños
                        sm: theme.typography.h4.fontSize, // Para tablets y tamaños superiores
                        lg: theme.typography.h2.fontSize,
                        // Puedes continuar con md, lg, xl para otros tamaños de pantalla si es necesario
                    }
                }}
                variant="h2"
                color="primary" >
                {title}
            </CustomTypography>
            <CustomTypography align="center" variant="body1">
                {description}
            </CustomTypography>
        </div>
    );
}

export default ErrorMessage;
