import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, Typography } from '@mui/material';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export default function ContributionPie({ data }) {
  if (!data || !data.developers || data.developers.length === 0) {
    return (
      <Card sx={{ height: 350 }}>
        <CardContent>
          <Typography variant="h6">Contribution Attribution</Typography>
          <Typography color="textSecondary" sx={{ mt: 2 }}>No contribution data available.</Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ height: 350 }}>
      <CardContent sx={{ height: '100%' }}>
        <Typography variant="h6" gutterBottom>Contribution Attribution</Typography>
        <ResponsiveContainer width="100%" height="85%">
          <PieChart>
            <Pie
              data={data.developers}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="contribution"
              nameKey="name"
            >
              {data.developers.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
