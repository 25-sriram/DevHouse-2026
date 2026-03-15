import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';

export default function EffortBar({ effort }) {
  if (!effort) {
    return (
      <Card sx={{ height: 350 }}>
        <CardContent>
          <Typography variant="h6">Effort Estimation</Typography>
          <Typography color="textSecondary" sx={{ mt: 2 }}>No effort data available.</Typography>
        </CardContent>
      </Card>
    );
  }

  const chartData = [
    { name: 'Lines Changed', value: effort.lines_changed || 0 },
    { name: 'Files Changed', value: effort.files_changed || 0 },
    { name: 'Modules', value: effort.modules_changed || 0 }
  ];

  return (
    <Card sx={{ height: 350 }}>
      <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6">Effort Estimation</Typography>
          <Chip 
            label={effort.effort_level || 'UNKNOWN'} 
            color={effort.effort_level === 'HIGH' ? 'error' : effort.effort_level === 'MEDIUM' ? 'warning' : 'success'} 
            size="small"
          />
        </Box>
        
        <Box sx={{ flexGrow: 1, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#1976d2" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
}
