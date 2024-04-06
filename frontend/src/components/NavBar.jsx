import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import DrawerList from './DrawerList';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Stack } from '@mui/material';
import { getUser } from "../utils/auth";
import { getRole } from "../utils/auth";

export default function NavBar(props) {
  const navigate = useNavigate()
  const [t,i18n] =useTranslation("global");

  const handleLogout = () => {
    localStorage.removeItem('access_token_ner')
    localStorage.removeItem('user_ner')
    navigate('/login')
  }

  const handleChangeLanguaje = (lang) =>{
    i18n.changeLanguage(lang);
  }

  return (
    <Box sx={{ flexGrow: 1}}>
      <AppBar position="static">
        <Toolbar sx={{background: "#25282F"}}>
          <DrawerList></DrawerList>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {props.title}
          </Typography>
          <Stack display={'flex'} flexDirection={'row'} gap={1} marginRight={4}>
            <Button onClick={() => handleChangeLanguaje("en")} variant="outlined" style={{color: "white", border: "1px solid white"}}>🇺🇸 EN</Button>
            <Button onClick={() => handleChangeLanguaje("es")} variant="outlined" style={{color: "white", border: "1px solid white"}}>🇪🇸 ES</Button>
          </Stack>
          
          <Button color="inherit" onClick={handleLogout}>{t("header.logout")}</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}