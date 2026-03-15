import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useDashboard } from '../../context/DashboardContext';
import { useParams } from 'react-router-dom';

export default function Header() {
  const { refreshAnalytics } = useDashboard();
  const { id } = useParams(); // will be undefined on main dashboard

  const handleRefresh = () => {
    refreshAnalytics(id);
  };

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
          Devhouse Engine Intelligence
        </Typography>
        <Box>
           <Button color="inherit" onClick={handleRefresh} startIcon={<RefreshIcon />}>
            Refresh Analytics
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
