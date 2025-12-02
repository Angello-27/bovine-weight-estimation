// frontend/src/components/molecules/WeightLineChart/index.js

import Box from "@mui/material/Box";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Card, CardContent, Typography } from '@mui/material';

/**
 * Tooltip personalizado para el gráfico de peso
 */
const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <Card sx={{ p: 1.5, boxShadow: 3 }}>
                <CardContent sx={{ p: '8px !important', '&:last-child': { pb: '8px' } }}>
                    <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                        Fecha: {label}
                    </Typography>
                    <Typography variant="body2" color="primary" sx={{ fontWeight: 600 }}>
                        Peso: {payload[0].value?.toFixed(1)} kg
                    </Typography>
                    {payload[0].payload.confianza && (
                        <Typography variant="caption" color="text.secondary">
                            Confianza: {payload[0].payload.confianza}%
                        </Typography>
                    )}
                </CardContent>
            </Card>
        );
    }
    return null;
};

/**
 * WeightLineChart molecule - Gráfico de línea para evolución de peso
 * @param {Array} data - Datos formateados para el gráfico [{ fecha, peso, confianza }]
 */
function WeightLineChart({ data }) {
    if (!data || data.length === 0) {
        return null;
    }

    return (
        <Box sx={{ width: '100%', height: 400, mb: 3 }}>
            <ResponsiveContainer>
                <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 60 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                        dataKey="fecha" 
                        angle={-45}
                        textAnchor="end"
                        height={80}
                        tick={{ fontSize: 12 }}
                    />
                    <YAxis 
                        label={{ value: 'Peso (kg)', angle: -90, position: 'insideLeft' }}
                        tick={{ fontSize: 12 }}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line 
                        type="monotone" 
                        dataKey="peso" 
                        stroke="#255946" 
                        strokeWidth={3}
                        dot={{ fill: '#49A760', r: 5 }}
                        activeDot={{ r: 7 }}
                        name="Peso (kg)"
                    />
                </LineChart>
            </ResponsiveContainer>
        </Box>
    );
}

export default WeightLineChart;

