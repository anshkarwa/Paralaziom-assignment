// src/pages/HomePage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Typography, Container, Grid, Paper, Box, CircularProgress } from '@mui/material';

// --- (Your data processing functions and teamColors object remain the same) ---
const processStackedChartData = (apiData) => {
    const seasons = [...new Set(apiData.map(item => item.season))].sort();
    const teams = [...new Set(apiData.map(item => item.winner))];
    const data = seasons.map(season => {
        let entry = { season };
        teams.forEach(team => {
            const teamData = apiData.find(d => d.season === season && d.winner === team);
            entry[team] = teamData ? teamData.wins : 0;
        });
        return entry;
    });
    return { data, teams };
};
const teamColors = { "Kolkata Knight Riders": "#2E0854", "Chennai Super Kings": "#FDB913", "Rajasthan Royals": "#004B8C", "Mumbai Indians": "#006CB7", "Sunrisers Hyderabad": "#FF822A", "Royal Challengers Bangalore": "#EC1C24", "Delhi Capitals": "#00008B", "Kings XI Punjab": "#DD1F2D", "Pune Warriors": "#2F9BE3", "Deccan Chargers": "#A0213A", "Gujarat Lions": "#E04622", "Kochi Tuskers Kerala": "#D4803A" };

function HomePage() {
    const [matchesPerYear, setMatchesPerYear] = useState([]);
    const [matchesWon, setMatchesWon] = useState({ data: [], teams: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const matchesYearlyResponse = await axios.get('http://127.0.0.1:8000/api/matches-per-year/');
                setMatchesPerYear(matchesYearlyResponse.data);
                const matchesWonResponse = await axios.get('http://127.0.0.1:8000/api/matches-won/');
                setMatchesWon(processStackedChartData(matchesWonResponse.data));
            } catch (err) {
                setError("Failed to fetch data. Is the backend server running?");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    return (
        // THIS IS THE CENTERING WRAPPER
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4, width: '100%' }}>
            <Container maxWidth="xl">
                <Grid container spacing={3} justifyContent="center">
                    {/* Chart 1 */}
                    <Grid item xs={12} lg={6}>
                        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 400 }}>
                            <Typography variant="h6" color="primary" gutterBottom>
                                Matches Played Per Year
                            </Typography>
                            <ResponsiveContainer>
                                <BarChart data={matchesPerYear}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="season" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="matches_played" fill="#8884d8" />
                                </BarChart>
                            </ResponsiveContainer>
                        </Paper>
                    </Grid>
                    {/* Chart 2 */}
                    <Grid item xs={12}>
                        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 500 }}>
                            <Typography variant="h6" color="primary" gutterBottom>
                                Matches Won By Team (All Years)
                            </Typography>
                            <ResponsiveContainer>
                                <BarChart data={matchesWon.data}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="season" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend wrapperStyle={{ overflowX: 'auto', maxHeight: 80 }} />
                                    {matchesWon.teams.map(team => (
                                        <Bar key={team} dataKey={team} stackId="a" fill={teamColors[team] || '#82ca9d'} />
                                    ))}
                                </BarChart>
                            </ResponsiveContainer>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </Box>
    );
}
export default HomePage;