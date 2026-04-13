import { useState } from "react";
import {
  Box,
  Card,
  TextField,
  Button,
  Typography,
  Alert,
} from "@mui/material";
import { Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();
  const baseURL = import.meta.env.VITE_BACK_URL;

  const signupMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch(`${baseURL}/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      let data = {};
      const text = await response.text();

      if (text) {
        try {
          data = JSON.parse(text);
        } catch {
          data = { message: text };
        }
      }

      if (!response.ok) {
        throw data;
      }

      return data;
    },

    onSuccess: (data) => {
      const displayMessage =
        data.message ||
        (data.detail?.[0]?.msg
          ? data.detail[0].msg
          : "Success");

      setMessage(displayMessage);

      if (data.access_token)
        localStorage.setItem("access_token", data.access_token);
      if (data.refresh_token)
        localStorage.setItem("refresh_token", data.refresh_token);
      if (data.user_id)
        localStorage.setItem("user_id", data.user_id);
      if (data.role)
        localStorage.setItem("role", data.role);

      navigate("/tasks");
    },

    onError: (error) => {
      const msg =
        error?.message ||
        (Array.isArray(error?.detail)
          ? error.detail[0].msg
          : error?.detail) ||
        "❌ Server connection error";

      setMessage(msg);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!name || !email || !password) {
      setMessage("Please fill all fields!");
      return;
    }

    setMessage("");
    signupMutation.mutate();
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
      <Card
        sx={{
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
          Create Account
        </Typography>

        {message && (
          <Alert
            severity={message.toLowerCase().includes("error") ? "error" : "success"}
            sx={{ mb: 2 }}
          >
            {message}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            size="small"
            label="Full Name"
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

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
            size="small"
            variant="contained"
            type="submit"
            sx={{ mt: 1 ,
              width:120,
              height: 27,
              borderRadius: "20px",
              mx: "auto",
              display: "block",
              fontSize: "12px",
              marginTop: 2,
            }}
            disabled={signupMutation.isPending}
          >
            {signupMutation.isPending ? "Signing up..." : "Sign Up"}
          </Button>
        </form>

        <Typography mt={2} textAlign="center"
        sx={{
              marginTop: 2.5,
              fontSize: "13px",
            }}
        >
          Already have an account?{" "}
          <Link to="/users/login">Login</Link>
        </Typography>
      </Card>
    </Box>
  );
}