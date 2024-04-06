import * as React from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import { Link } from "@mui/material";
import { getRole } from "../utils/auth";

export default function DrawerList() {
  const [open, setOpen] = React.useState(false);
 
  const toggleDrawer = (newOpen) => () => {
     setOpen(newOpen);
  };
 
  const isAdmin = () => getRole() === "admin";
 
  const listItems = [
     { text: "Home", url: "/" },
     { text: "Name Entity recognition", url: "/ner" },
     { text: "Train", url: "/train" },
     { text: "Test", url: "/prueba" },
     ...(isAdmin() ? [{ text: "Train Model Admin", url: "/train_model_admin" }] : []),
     ...(isAdmin() ? [{ text: "Users Admin", url: "/users_admin" }] : []),
  ];
 
  const DrawerList = (
     <Box sx={{ width: 250 }} role="presentation">
       <List>
         {listItems.map((item, index) => (
           <ListItem key={item.text} disablePadding>
             <ListItemButton>
               <ListItemIcon>
                 {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
               </ListItemIcon>
               <Link href={item.url} color="inherit" underline="none">
                 {item.text}
               </Link>
             </ListItemButton>
           </ListItem>
         ))}
       </List>
     </Box>
  );
 
  return (
     <div>
       <IconButton
         size="large"
         edge="start"
         color="inherit"
         aria-label="menu"
         sx={{ mr: 2 }}
         onClick={toggleDrawer(true)}
       >
         <MenuIcon />
       </IconButton>
       <Drawer open={open} onClose={toggleDrawer(false)}>
         {DrawerList}
       </Drawer>
     </div>
  );
 }
 