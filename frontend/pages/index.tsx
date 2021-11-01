import { Menu } from '@mui/icons-material/';
import { AppBar, IconButton, Toolbar, Typography } from '@mui/material';
import Dashboard from '../components/Dashboard';

const App = () => {
  return (
    <div className="App">
      <AppBar position="sticky">
        <Toolbar variant="dense">
          <IconButton edge="start" color="inherit" aria-label="menu">
            <Menu />
          </IconButton>
          <Typography variant="h6" color="inherit">
            Datafy
          </Typography>
        </Toolbar>
      </AppBar>
      {/* <Toolbar /> */}
      <div className="dashboard">
        <Dashboard></Dashboard>
      </div>
    </div>
  );
}

export default App;