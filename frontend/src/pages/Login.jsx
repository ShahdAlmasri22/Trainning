import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import "../index.css";


import {
  Box,
  Card,
  TextField,
  Button,
  Typography,
  Alert,
} from "@mui/material";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();
  const baseURL = import.meta.env.VITE_BACK_URL;

  const loginMutation = useMutation({
    mutationFn: async ({ email, password }) => {
      const response = await fetch(`${baseURL}/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error("Server returned empty response");
      }

      if (!response.ok) {
        throw new Error(data?.message || "Login failed");
      }

      return data;
    },

    onSuccess: (data) => {
      localStorage.clear();

      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
      }

      if (data.refresh_token) {
        localStorage.setItem("refresh_token", data.refresh_token);
      }

      if (data.user_id) {
        localStorage.setItem("user_id", data.user_id);
      }

      if (data.role) {
        localStorage.setItem("role", data.role);
      }


      navigate("/tasks");
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !password) return;

    loginMutation.mutate({
      email,
      password,
    });
  };

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "linear-gradient(135deg, #667eea, #764ba2)",
      }}
    >
      <Card sx={{
          p: 4,
          width: 370,
          borderRadius: 3,

          "& .MuiTextField-root": {
            marginBottom: 1,
          },

          "& .MuiInputLabel-root": {
            fontSize: "12px",
          },

          "& .MuiInputBase-input": {
            fontSize: "14px",
          },
        }}
      >
        <Typography variant="h5" mb={2} textAlign="center">
          Login
        </Typography>

        {loginMutation.isError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {loginMutation.error.message}
          </Alert>
        )}

        {loginMutation.isSuccess && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Login successful!
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            size="small"
            label="Email"
            type="email"
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <TextField
            fullWidth
            size="small"
            label="Password"
            type="password"
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            fullWidth
            variant="contained"
            type="submit"
            disabled={loginMutation.isPending}
            sx={{ mt: 1 ,
              width:120,
              height: 27,
              borderRadius: "20px",
              mx: "auto",
              display: "block",
              fontSize: "12px",
              marginTop: 2,
            }}
          >
            {loginMutation.isPending ? "Signing in..." : "Sign In"}
          </Button>
        </form>

        <Typography mt={2} textAlign="center"
         sx={{
              marginTop: 2.5,
              fontSize: "13px",
            }}
        >
          Don't have an account? <a href="/users/signup">Sign Up</a>
        </Typography>
      </Card>
    </Box>
  );
}
