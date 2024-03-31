import React, {useState, useEffect} from "react";
import { Stack, Container, IconButton, Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button } from '@mui/material';
import { Select, MenuItem } from '@mui/material';

export default function AddUser(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [rol, setRol] = useState('');
    const [open, setOpen] = useState(false)
    const handleInsert = () => {
        setOpen(true); 
    };
  
    const handleClose = () => {
        setOpen(false);
    };
  
    const handleSave = async () => {
        
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: username, password: password, rol: rol })
        };
  
        try {
            const response = await fetch("http://localhost:5000/insert_user", requestOptions);
            if (!response.ok) {
                throw new Error('Error al crear el usuario');
            }
            const data = await response.json();
            console.log("Resultado de crear un usuario:", data);
        } catch (error) {
            console.error("Error al realizar la solicitud:", error);
        }
        handleClose(); 
    };

    return(
        <Stack sx={{display: "grid", placeItems: "start", width: "80%", marginY: "20px"}}>
            <Stack >
                <Button variant="contained" onClick={handleInsert}>Add User</Button>
            </Stack>

            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>New User</DialogTitle>
                <DialogContent sx={{padding: "20px", gap: "20px"}}>
                    <TextField label="Username" fullWidth sx={{marginTop: "10px"}} onChange={(e) => setUsername(e.target.value)} value={username}/>
                    <TextField label="Password" fullWidth sx={{marginTop: "20px"}} onChange={(e) => setPassword(e.target.value)} value={password} />
                    <Select
                      label="Rol"
                      value={rol}
                      onChange={(e) => setRol(e.target.value)}
                      fullWidth
                      sx={{marginTop: "20px"}}
                    >
                        <MenuItem value="user">user</MenuItem>
                        <MenuItem value="admin">admin</MenuItem>
                    </Select>

                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>CLose</Button>
                    <Button onClick={handleSave}>Save</Button>
                </DialogActions>
          </Dialog>
            
        </Stack>
    )
}