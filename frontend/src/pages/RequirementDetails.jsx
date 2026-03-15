import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Grid, Typography, CircularProgress, Box, Alert, Card, CardContent } from '@mui/material';
import { useDashboard } from '../context/DashboardContext';

import RequirementCard from '../components/cards/RequirementCard';
import ContributionPie from '../components/charts/ContributionPie';
import EffortBar from '../components/charts/EffortBar';
import ImpactRadar from '../components/charts/ImpactRadar';

export default function RequirementDetails() {
  const { id } = useParams();
  const { 
    selectedRequirement, contribution, effort, impact, businessSummary,
    loading, error, fetchRequirementMetrics 
  } = useDashboard();

  useEffect(() => {
    if (id) {
      fetchRequirementMetrics(id);
    }
  }, [id, fetchRequirementMetrics]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
        Intelligence Drill-Down
      </Typography>

      {/* Main Requirement Summary Card */}
      <RequirementCard requirement={selectedRequirement} />

      {/* Business Translation Component */}
      {businessSummary && businessSummary.technical_activity && (
        <Card sx={{ mb: 4, backgroundColor: '#e3f2fd' }} elevation={0} variant="outlined">
          <CardContent>
             <Typography variant="subtitle2" color="primary" gutterBottom>Business Translator (Phase 14)</Typography>
             <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
               {businessSummary.business_explanation}
             </Typography>
             <Typography variant="body2" color="textSecondary" sx={{ mt: 1, fontFamily: 'monospace' }}>
               Technical: {businessSummary.technical_activity}
             </Typography>
          </CardContent>
        </Card>
      )}

      {/* Analytics Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <ContributionPie data={contribution} />
        </Grid>
        <Grid item xs={12} md={4}>
          <EffortBar effort={effort} />
        </Grid>
        <Grid item xs={12} md={4}>
          <ImpactRadar impact={impact} />
        </Grid>
      </Grid>
    </Box>
  );
}
