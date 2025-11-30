// frontend/src/components/molecules/DataTable/index.js

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Card from '../../atoms/Card';
import EmptyState from '../EmptyState';

/**
 * DataTable molecule - Tabla reutilizable con estilo consistente
 * @param {Array} columns - Array de objetos { label, field, render? }
 * @param {Array} rows - Array de objetos con datos
 * @param {Function} onRowClick - Callback cuando se hace click en una fila
 */
function DataTable({ columns, rows, onRowClick, emptyMessage = 'No hay datos disponibles.' }) {
    if (!rows || rows.length === 0) {
        return <EmptyState message={emptyMessage} />;
    }

    return (
        <Card>
            <TableContainer component={Paper} variant="outlined">
                <Table>
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell key={column.field}>
                                    <strong>{column.label}</strong>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows.map((row, index) => (
                            <TableRow
                                key={row.id || index}
                                hover={!!onRowClick}
                                onClick={() => onRowClick && onRowClick(row)}
                                sx={{ cursor: onRowClick ? 'pointer' : 'default' }}
                            >
                                {columns.map((column) => {
                                    const cellValue = row[column.field];
                                    let displayValue;
                                    
                                    if (column.render) {
                                        displayValue = column.render(cellValue, row);
                                    } else if (cellValue == null || cellValue === '') {
                                        displayValue = '-';
                                    } else if (typeof cellValue === 'object') {
                                        // Si es un objeto, intentar extraer un ID o mostrar una representación útil
                                        displayValue = cellValue.id || cellValue.name || cellValue.toString() || '-';
                                    } else {
                                        displayValue = cellValue;
                                    }
                                    
                                    return (
                                        <TableCell key={column.field}>
                                            {displayValue}
                                        </TableCell>
                                    );
                                })}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Card>
    );
}

export default DataTable;

