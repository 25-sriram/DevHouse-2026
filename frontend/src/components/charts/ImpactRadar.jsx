import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';

export default function ImpactRadar({ impact }) {
  if (!impact || !impact.modules_affected || impact.modules_affected.length === 0) {
    return (
      <Card sx={{ height: 350 }}>
        <CardContent>
          <Typography variant="h6">Architectural Impact</Typography>
          <Typography color="textSecondary" sx={{ mt: 2 }}>No impact data to display.</Typography>
        </CardContent>
      </Card>
    );
  }

  // Format array of strings into Radar objects
  const chartData = impact.modules_affected.map(mod => ({
    subject: mod,
    A: impact.impact_score || 50,
    fullMark: 100
  }));

  return (
    <Card sx={{ height: 350 }}>
      <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
         <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6">Architectural Blast Radius</Typography>
          <Chip 
            label={impact.impact_level || 'UNKNOWN'} 
            color={impact.impact_level === 'HIGH' ? 'error' : impact.impact_level === 'MEDIUM' ? 'warning' : 'primary'} 
            size="small"
          />
        </Box>
        <Box sx={{ flexGrow: 1, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis />
              <Radar name="Impact Score" dataKey="A" stroke="#00bfa5" fill="#00bfa5" fillOpacity={0.6} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
}
