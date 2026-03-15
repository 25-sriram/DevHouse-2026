import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, Typography, Box } from '@mui/material';

export default function WorkloadHeatmap({ workload }) {
  if (!workload || workload.length === 0) {
     return (
      <Card sx={{ height: 350 }}>
        <CardContent>
          <Typography variant="h6">Developer Workload</Typography>
          <Typography color="textSecondary" sx={{ mt: 2 }}>No workload data available.</Typography>
        </CardContent>
      </Card>
    );
  }

  // To simulate heatmap in a stacked bar, we paint overtime logic onto a composite graph
  return (
    <Card sx={{ height: 350 }}>
      <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h6" gutterBottom>Workload Distribution (Last 30 Days)</Typography>
        <Box sx={{ flexGrow: 1, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={workload}
              margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="developer" />
              <YAxis yAxisId="left" orientation="left" stroke="#1976d2" />
              <YAxis yAxisId="right" orientation="right" stroke="#dc004e" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="lines_changed" name="Lines Changed" fill="#1976d2" />
              <Bar yAxisId="right" dataKey="hours" name="Active Hours" fill="#00bfa5" />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
}
