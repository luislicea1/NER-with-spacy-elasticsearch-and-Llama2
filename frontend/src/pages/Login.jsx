import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import { Stack } from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";

import { Toaster, toast } from "sonner";
import { authService } from "../services/auth";
import { useNavigate } from "react-router-dom";
import { LoadingButton } from "@mui/lab";
import { useLoadingStore } from "../../stores/useLoadingStore";
import { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const loading = useLoadingStore((state) => state.loading);
  const setLoading = useLoadingStore((state) => state.setLoading);

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      const response = await authService.loginUser(username, password);
      if (response === true) return navigate("/");

      toast.error("Las credenciales no son válidas");
    } catch (error) {
      toast.error("Las credenciales no son válidas");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack
      height="100vh"
      justifyContent="center"
      alignItems="center"
      sx={{ padding: "0 20px" }}
    >
      <Box boxShadow={20} sx={{ borderRadius: "10px" }}>
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 2,
              marginBottom: 2,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box
              component="form"
              onSubmit={handleSubmit}
              noValidate
              sx={{ mt: 1 }}
            >
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                type="password"
                id="password"
                label="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <Toaster
                duration={3000}
                position="bottom-center"
                richColors
                theme="dark"
                closeButton
              />
              {loading ? (
                <LoadingButton
                  loading
                  loadingIndicator="Iniciando..."
                  variant="outlined"
                  fullWidth
                >
                  Iniciando...
                </LoadingButton>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSubmit}
                  fullWidth
                  marginBottom= {"px"}
                  sx={{margin: "10px 0"}}
                >
                  Sign In
                </Button>
              )}
            </Box>
          </Box>
        </Container>
      </Box>
    </Stack>
  );
}
