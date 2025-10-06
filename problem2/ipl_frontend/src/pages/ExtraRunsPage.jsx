// src/pages/ExtraRunsPage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Typography, Container, Select, MenuItem, FormControl, InputLabel, Box, Paper, CircularProgress } from '@mui/material';

const years = Array.from({ length: (2017 - 2008 + 1) }, (_, i) => 2008 + i);

function ExtraRunsPage() {
    const [selectedYear, setSelectedYear] = useState(2017);
    const [extraRunsData, setExtraRunsData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchExtraRuns = async () => {
            if (!selectedYear) return;
            setLoading(true);
            setError(null);
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/extra-runs/?year=${selectedYear}`);
                setExtraRunsData(response.data);
            } catch (err) {
                setError("Failed to fetch extra runs data.");
            } finally {
                setLoading(false);
            }
        };
        fetchExtraRuns();
    }, [selectedYear]);

    const renderChart = () => {
        if (loading) {
            return (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
                    <CircularProgress />
                </Box>
            );
        }
        if (error) {
            return (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
                    <Typography color="error">{error}</Typography>
                </Box>
            );
        }
        return (
            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={extraRunsData} layout="vertical" margin={{ left: 50 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="bowling_team" type="category" width={150} tick={{ fontSize: 12 }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="extra_runs" fill="#fa8072" />
                </BarChart>
            </ResponsiveContainer>
        );
    };

    return (
        // THIS IS THE CENTERING WRAPPER
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4, width: '100%' }}>
            <Container maxWidth="lg">
                <Paper sx={{ p: 2 }}>
                    <Typography variant="h4" gutterBottom>
                        Extra Runs Conceded Per Team
                    </Typography>
                    <FormControl fullWidth sx={{ mb: 2 }}>
                        <InputLabel>Select Year</InputLabel>
                        <Select
                            value={selectedYear}
                            label="Select Year"
                            onChange={(e) => setSelectedYear(e.target.value)}
                        >
                            {years.map(year => (
                                <MenuItem key={year} value={year}>{year}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    {renderChart()}
                </Paper>
            </Container>
        </Box>
    );
}
export default ExtraRunsPage;