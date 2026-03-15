import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

export default function MetricCard({ title, value, color }) {
  return (
    <Card sx={{ height: '100%', minWidth: 200 }}>
      <CardContent>
        <Typography color="textSecondary" gutterBottom variant="subtitle2">
          {title}
        </Typography>
        <Typography variant="h4" component="div" sx={{ color: color || 'text.primary', fontWeight: 'bold' }}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}
