import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import DrawerList from './DrawerList';
import { useNavigate } from 'react-router-dom';

export default function NavBar(props) {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token_ner')
    localStorage.removeItem('user_ner')
    navigate('/login')
  }

  return (
    <Box sx={{ flexGrow: 1}}>
      <AppBar position="static">
        <Toolbar sx={{background: "#25282F"}}>
          <DrawerList></DrawerList>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {props.title}
          </Typography>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}