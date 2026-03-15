import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';

export default function RequirementCard({ requirement }) {
  if (!requirement) return null;

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" component="div">
            Requirement: {requirement.requirement_id}
          </Typography>
          <Chip 
            label={requirement.completion_percent === 100 ? "Completed" : "In Progress"} 
            color={requirement.completion_percent === 100 ? "success" : "warning"} 
          />
        </Box>
        
        <Box display="flex" gap={4}>
          <Box>
            <Typography color="textSecondary" variant="body2">Effort Score</Typography>
            <Typography variant="h6">{Math.round(requirement.effort_score)}</Typography>
          </Box>
          <Box>
            <Typography color="textSecondary" variant="body2">Impact Score</Typography>
            <Typography variant="h6">{Math.round(requirement.impact_score)}</Typography>
          </Box>
          <Box>
            <Typography color="textSecondary" variant="body2">Top Contributor</Typography>
            <Typography variant="h6">{requirement.top_contributor}</Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
