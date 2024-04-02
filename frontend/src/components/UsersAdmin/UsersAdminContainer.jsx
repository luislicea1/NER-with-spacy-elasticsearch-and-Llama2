import * as React from "react";
import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import {
  Stack,
  Container,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
  LinearProgress,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { Select, MenuItem } from "@mui/material";
import AddUser from "./AddUser";

export default function UsersAdminContainer() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState({});
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rol, setRol] = useState("");

  const columns = [
    { field: "id", headerName: "ID", width: 200 },
    {
      field: "username",
      headerName: "Username",
      width: 200,
    },
    {
      field: "rol",
      headerName: "Rol",
      width: 200,
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 200,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <IconButton onClick={() => handleEdit(params.row)}>
            <EditIcon />
          </IconButton>
          <IconButton onClick={() => handleDelete(params.row)}>
            <DeleteIcon />
          </IconButton>
        </Stack>
      ),
    },
  ];

  const fetchData = async () => {
    setLoading(true);
    const response = await fetch("http://localhost:5000/get_users");
    const data = await response.json();

    setUsers(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleEdit = (row) => {
    setSelectedUser(row);
    setUsername(row.username);
    setPassword(row.password);
    setRol(row.rol);
    setOpen(true);
  };

  const handleClose = async () => {
    setOpen(false);
    await fetchData();
  };

  const handleSave = async () => {
    console.log("Guardar cambios:", selectedUser);
    const requestOptions = {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        old_username: selectedUser.username,
        new_username: username,
        password: password,
        rol: rol,
      }),
    };

    try {
      const response = await fetch(
        "http://localhost:5000/update_user",
        requestOptions
      );
      if (!response.ok) {
        throw new Error("Error al editar el usuario");
      }
      const data = await response.json();

      console.log("Resultado de editar un usuario:", data);
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
    handleClose();
  };

  const handleDelete = async (row) => {
    const requestOptions = {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: row.username }),
    };

    try {
      const response = await fetch(
        "http://localhost:5000/delete_user",
        requestOptions
      );
      if (!response.ok) {
        throw new Error("Error al eliminar el usuario");
      }
      const data = await response.json();
      console.log("Resultado de la eliminación:", data);
      await fetchData();
    } catch (error) {
      console.error("Error al realizar la solicitud:", error);
    }
  };

  return (
    <Container sx={{ display: "grid", placeItems: "center" }}>
      <AddUser fetchData={fetchData}></AddUser>
      {loading && <LinearProgress />}
      <Box
        sx={{ height: 400, width: "80%", borderRadius: "10px" }}
        boxShadow={20}
      >
        <DataGrid
          rows={users}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 5,
              },
            },
          }}
          pageSizeOptions={[5]}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Box>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>User Edit</DialogTitle>
        <DialogContent sx={{ padding: "20px", gap: "20px" }}>
          <TextField
            label="Username"
            value={username}
            fullWidth
            sx={{ marginTop: "10px" }}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            label="Password"
            value={password}
            fullWidth
            sx={{ marginTop: "20px" }}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Select
            label="Rol"
            value={rol}
            onChange={(e) => setRol(e.target.value)}
            fullWidth
            sx={{ marginTop: "20px" }}
          >
            <MenuItem value="user">user</MenuItem>
            <MenuItem value="admin">admin</MenuItem>
          </Select>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
          <Button onClick={handleSave}>Save</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}
