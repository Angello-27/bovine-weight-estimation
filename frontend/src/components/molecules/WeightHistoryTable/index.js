// frontend/src/components/molecules/WeightHistoryTable/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

/**
 * WeightHistoryTable molecule - Tabla de historial de pesos
 * @param {Array} data - Array de puntos de peso [{ label, weight, confidence }]
 */
function WeightHistoryTable({ data }) {
    if (!data || data.length === 0) {
        return null;
    }

    return (
        <Box>
            <CustomTypography variant="subtitle2" mb={2}>
                Historial Detallado
            </CustomTypography>
            <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell><strong>Fecha</strong></TableCell>
                            <TableCell align="right"><strong>Peso (kg)</strong></TableCell>
                            <TableCell align="center"><strong>Confianza</strong></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map((point, index) => (
                            <TableRow key={index} hover>
                                <TableCell>{point.label}</TableCell>
                                <TableCell align="right">
                                    <strong>{point.weight.toFixed(1)}</strong>
                                </TableCell>
                                <TableCell align="center">
                                    {point.confidence ? `${(point.confidence * 100).toFixed(0)}%` : '-'}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}

export default WeightHistoryTable;

