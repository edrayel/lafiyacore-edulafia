import { useState, useRef } from "react";
import { useNavigate } from "@tanstack/react-router";
import {
  Box,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
} from "@mui/material";
import { Mail, Lock, Eye, EyeOff } from "lucide-react";
import { useAuthStore } from "@/shared/stores/authStore";
import { AuthLayout } from "./components/AuthLayout";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoading, error, clearError } = useAuthStore();
  const navigate = useNavigate();
  const formRef = useRef<HTMLFormElement>(null);

  const validateEmail = (value: string): boolean => {
    if (!value) {
      setEmailError("Email is required");
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      setEmailError("Please enter a valid email address");
      return false;
    }
    setEmailError("");
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    let valid = true;
    if (!validateEmail(email)) valid = false;
    if (!password) {
      setPasswordError("Password is required");
      valid = false;
    }
    if (!valid) return;
    try {
      await login(email, password);
      navigate({ to: "/" });
    } catch {
      // Error surfaced through authStore.error
    }
  };

  return (
    <AuthLayout>
      <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 700, color: "#0f172a", mb: 1 }}>
          Welcome back
        </Typography>
        <Typography variant="body2" sx={{ color: "#64748b" }}>
          Please enter your details to sign in to EduLafia
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={clearError} role="alert">
          {error}
        </Alert>
      )}

      <Box
        component="form"
        ref={formRef}
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          fullWidth
          autoFocus
          label="Email address"
          placeholder="you@school.edu"
          value={email}
          onChange={(e) => { setEmail(e.target.value); if (emailError) setEmailError(""); }}
          onBlur={() => validateEmail(email)}
          error={!!emailError}
          helperText={emailError}
          disabled={isLoading}
          variant="outlined"
          required
          inputProps={{ autoComplete: "email" }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Mail size={20} color="#94a3b8" />
              </InputAdornment>
            ),
          }}
        />
        <TextField
          fullWidth
          label="Password"
          type={showPassword ? "text" : "password"}
          placeholder="Enter your password"
          value={password}
          onChange={(e) => { setPassword(e.target.value); if (passwordError) setPasswordError(""); }}
          error={!!passwordError}
          helperText={passwordError}
          disabled={isLoading}
          variant="outlined"
          required
          inputProps={{ autoComplete: "current-password" }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Lock size={20} color="#94a3b8" />
              </InputAdornment>
            ),
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() => setShowPassword(!showPassword)}
                  edge="end"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  sx={{ color: "#94a3b8" }}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <Button
          fullWidth
          type="submit"
          variant="contained"
          disabled={isLoading}
          sx={{
            mt: 2,
            py: 1.5,
            borderRadius: "9999px",
            fontSize: "1rem",
            fontWeight: 600,
            textTransform: "none",
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : "Sign In"}
        </Button>
      </Box>

      <Typography
        variant="body2"
        align="center"
        onClick={() => navigate({ to: "/forgot-password" })}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") navigate({ to: "/forgot-password" }); }}
        sx={{
          mt: 2,
          color: "#64748b",
          cursor: "pointer",
          transition: "color 0.2s",
          "&:hover": { color: "#0f172a" },
          "&:focus-visible": { outline: "2px solid #2563eb", outlineOffset: "4px", borderRadius: "4px" },
        }}
      >
        Forgot your password? Reset password
      </Typography>
    </AuthLayout>
  );
}
