import React, { useEffect } from 'react';
import { Grid, Typography, CircularProgress, Box, Alert } from '@mui/material';
import { useDashboard } from '../context/DashboardContext';

import MetricCard from '../components/cards/MetricCard';
import ContributionPie from '../components/charts/ContributionPie';
import EffortBar from '../components/charts/EffortBar';
import ImpactRadar from '../components/charts/ImpactRadar';
import WorkloadHeatmap from '../components/charts/WorkloadHeatmap';
import KnowledgeRiskTable from '../components/charts/KnowledgeRiskTable';

export default function Dashboard() {
  const { 
    overview, workload, knowledgeRisk, 
    loading, error, fetchGlobalMetrics 
  } = useDashboard();

  useEffect(() => {
    fetchGlobalMetrics();
  }, [fetchGlobalMetrics]);

  if (loading && !overview) {
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
        Engineering Overview
      </Typography>

      {/* Top Metrics Row */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard 
            title="Total Analyzed Requirements" 
            value={overview?.total_analyzed_requirements || 0} 
            color="#1976d2" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard 
            title="Avg System Effort Score" 
            value={overview?.average_effort_score || 0} 
            color="#ff9800" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard 
            title="Avg Architectural Impact" 
            value={overview?.average_impact_score || 0} 
            color="#ed6c02" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard 
            title="Active Developers (30d)" 
            value={workload?.length || 0} 
            color="#2e7d32" 
          />
        </Grid>
      </Grid>

      {/* Analytics Charts Rows */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={12}>
          <WorkloadHeatmap workload={workload} />
        </Grid>
      </Grid>
      
      {/* Knowledge Risk Bottom */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
           <KnowledgeRiskTable data={knowledgeRisk} />
        </Grid>
      </Grid>
      
    </Box>
  );
}
