// frontend/src/components/molecules/DataTable/index.js

import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import SearchField from '../../atoms/SearchField';
import EmptyState from '../EmptyState';

/**
 * DataTable molecule - Tabla reutilizable con estilo consistente y paginación
 * @param {Array} columns - Array de objetos { label, field, render? }
 * @param {Array} rows - Array de objetos con datos
 * @param {Function} onRowClick - Callback cuando se hace click en una fila
 * @param {string} emptyMessage - Mensaje cuando no hay datos
 * @param {Object} pagination - Objeto con { page, pageSize, total } para paginación controlada
 * @param {Function} onPageChange - Callback cuando cambia la página (page, pageSize)
 * @param {Function} onPageSizeChange - Callback cuando cambia el tamaño de página
 * @param {boolean} searchable - Si es true, muestra un campo de búsqueda integrado
 * @param {string} searchValue - Valor del campo de búsqueda (controlado)
 * @param {Function} onSearchChange - Callback cuando cambia el valor de búsqueda
 * @param {string} searchPlaceholder - Placeholder del campo de búsqueda
 */
function DataTable({ 
    columns, 
    rows, 
    onRowClick, 
    emptyMessage = 'No hay datos disponibles.',
    pagination,
    onPageChange,
    onPageSizeChange,
    searchable = false,
    searchValue = '',
    onSearchChange,
    searchPlaceholder = 'Buscar...'
}) {
    // Si hay paginación controlada, usar esos valores
    const isControlled = pagination !== undefined;
    const [internalPage, setInternalPage] = React.useState(0);
    const [internalPageSize, setInternalPageSize] = React.useState(10);

    const page = isControlled ? pagination.page : internalPage;
    const pageSize = isControlled ? pagination.pageSize : internalPageSize;
    const total = isControlled ? pagination.total : rows.length;

    // Para paginación no controlada, mostrar solo las filas de la página actual
    const paginatedRows = isControlled 
        ? rows 
        : rows.slice(page * pageSize, page * pageSize + pageSize);

    const handleChangePage = (event, newPage) => {
        if (isControlled && onPageChange) {
            onPageChange(newPage, pageSize);
        } else {
            setInternalPage(newPage);
        }
    };

    const handleChangeRowsPerPage = (event) => {
        const newPageSize = parseInt(event.target.value, 10);
        if (isControlled && onPageSizeChange) {
            onPageSizeChange(newPageSize);
        } else {
            setInternalPageSize(newPageSize);
            setInternalPage(0);
        }
    };

    if (!rows || rows.length === 0) {
        return <EmptyState message={emptyMessage} />;
    }

    return (
        <Box sx={{ width: '100%' }}>
            <TableContainer 
                component={Paper} 
                variant="outlined"
                sx={{ 
                    width: '100%',
                    overflowX: 'auto'
                }}
            >
                {/* Barra de búsqueda integrada */}
                {searchable && (
                    <Box sx={{ p: 2, borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}>
                        <SearchField
                            value={searchValue}
                            placeholder={searchPlaceholder}
                            onChange={(e) => {
                                // Solo actualizar el valor del input, no buscar aún
                                if (onSearchChange) {
                                    onSearchChange(e);
                                }
                            }}
                            onSearch={(value) => {
                                // Aplicar búsqueda cuando se presiona el botón o Enter
                                if (onSearchChange) {
                                    const syntheticEvent = {
                                        target: { value },
                                        type: 'search'
                                    };
                                    onSearchChange(syntheticEvent);
                                }
                            }}
                            onClear={() => {
                                // Limpiar búsqueda
                                if (onSearchChange) {
                                    const syntheticEvent = {
                                        target: { value: '' },
                                        type: 'clear'
                                    };
                                    onSearchChange(syntheticEvent);
                                }
                            }}
                        />
                    </Box>
                )}
                <Table sx={{ minWidth: 650 }}>
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell 
                                    key={column.field}
                                    sx={{ 
                                        fontWeight: 600,
                                        backgroundColor: (theme) => 
                                            theme.palette.mode === 'dark' 
                                                ? theme.palette.grey[800] 
                                                : theme.palette.grey[100],
                                    }}
                                >
                                    {column.label}
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {paginatedRows.map((row, index) => (
                            <TableRow
                                key={row.id || index}
                                hover={!!onRowClick}
                                onClick={() => onRowClick && onRowClick(row)}
                                sx={{ 
                                    cursor: onRowClick ? 'pointer' : 'default',
                                    '&:nth-of-type(odd)': {
                                        backgroundColor: (theme) => 
                                            theme.palette.mode === 'dark' 
                                                ? 'rgba(255, 255, 255, 0.02)' 
                                                : 'rgba(0, 0, 0, 0.02)',
                                    },
                                }}
                            >
                                {columns.map((column) => {
                                    const cellValue = row[column.field];
                                    let displayValue;
                                    
                                    if (column.render) {
                                        displayValue = column.render(cellValue, row);
                                    } else if (cellValue == null || cellValue === '') {
                                        displayValue = '-';
                                    } else if (typeof cellValue === 'object') {
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
                {pagination && (
                    <TablePagination
                        component="div"
                        count={total}
                        page={page}
                        onPageChange={handleChangePage}
                        rowsPerPage={pageSize}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                        rowsPerPageOptions={[5, 10, 25, 50, 100]}
                        labelRowsPerPage="Filas por página:"
                        labelDisplayedRows={({ from, to, count }) => 
                            `${from}-${to} de ${count !== -1 ? count : `más de ${to}`}`
                        }
                        sx={{
                            borderTop: (theme) => `1px solid ${theme.palette.divider}`,
                        }}
                    />
                )}
            </TableContainer>
        </Box>
    );
}

export default DataTable;

