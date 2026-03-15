import React from 'react';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip } from '@mui/material';

export default function KnowledgeRiskTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <Card sx={{ mt: 3, mb: 3 }}>
        <CardContent>
          <Typography variant="h6">Knowledge Concentration Risk</Typography>
          <Typography color="textSecondary" sx={{ mt: 2 }}>No risk data identified across analyzed modules.</Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ mt: 3, mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Knowledge Concentration Risk (Bus Factor)</Typography>
        <TableContainer component={Paper} elevation={0} variant="outlined">
          <Table size="small">
            <TableHead sx={{ backgroundColor: '#f9f9f9' }}>
              <TableRow>
                <TableCell><b>Module</b></TableCell>
                <TableCell><b>Developer</b></TableCell>
                <TableCell align="right"><b>Contributions</b></TableCell>
                <TableCell align="right"><b>% Ownership</b></TableCell>
                <TableCell align="right"><b>Risk Level</b></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row, idx) => (
                <TableRow key={idx}>
                  <TableCell>{row.module}</TableCell>
                  <TableCell>{row.developer}</TableCell>
                  <TableCell align="right">{row.commit_count} commits</TableCell>
                  <TableCell align="right">{(row.contribution_percent * 100).toFixed(0)}%</TableCell>
                  <TableCell align="right">
                    <Chip 
                      label={row.risk_level} 
                      color={row.risk_level === 'HIGH' ? 'error' : row.risk_level === 'MEDIUM' ? 'warning' : 'success'} 
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
}
