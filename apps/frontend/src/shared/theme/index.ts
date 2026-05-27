import { createTheme, responsiveFontSizes } from "@mui/material/styles";
import type {} from "@mui/x-data-grid/themeAugmentation";

const headingFont = "\"Plus Jakarta Sans\", \"Inter\", sans-serif";
const bodyFont = "\"Inter\", \"Helvetica\", \"Arial\", sans-serif";

const BASE_CONFIG = {
  typography: {
    fontFamily: bodyFont,
    h1: { fontFamily: headingFont, fontSize: "3.5rem", fontWeight: 800, letterSpacing: "-0.03em", lineHeight: 1.1 },
    h2: { fontFamily: headingFont, fontSize: "2.5rem", fontWeight: 700, letterSpacing: "-0.02em", lineHeight: 1.2 },
    h3: { fontFamily: headingFont, fontSize: "2rem", fontWeight: 700, letterSpacing: "-0.01em", lineHeight: 1.2 },
    h4: { fontFamily: headingFont, fontSize: "1.5rem", fontWeight: 700, letterSpacing: "-0.01em", lineHeight: 1.3 },
    h5: { fontFamily: headingFont, fontSize: "1.25rem", fontWeight: 600, letterSpacing: "-0.01em", lineHeight: 1.4 },
    h6: { fontFamily: headingFont, fontSize: "1.125rem", fontWeight: 600, letterSpacing: "-0.005em", lineHeight: 1.5 },
    subtitle1: { fontSize: "1rem", fontWeight: 600, lineHeight: 1.5 },
    subtitle2: { fontSize: "0.875rem", fontWeight: 600, letterSpacing: "0.01em", lineHeight: 1.57 },
    body1: { fontSize: "1rem", fontWeight: 400, lineHeight: 1.6 },
    body2: { fontSize: "0.875rem", fontWeight: 400, lineHeight: 1.57 },
    caption: { fontSize: "0.75rem", fontWeight: 500, letterSpacing: "0.02em", lineHeight: 1.66 },
    button: { fontFamily: headingFont, fontSize: "0.9rem", fontWeight: 600, textTransform: "none" as const, letterSpacing: "0.01em" },
  },
  shape: { borderRadius: 12 },
  spacing: 8,
};

const LIGHT_THEME = createTheme({
  ...BASE_CONFIG,
  palette: {
    mode: "light",
    primary: { main: "#2563eb", light: "#60a5fa", dark: "#1d4ed8", contrastText: "#ffffff" },
    secondary: { main: "#64748b", light: "#94a3b8", dark: "#475569", contrastText: "#ffffff" },
    background: { default: "#f8fafc", paper: "#ffffff" },
    text: { primary: "#0f172a", secondary: "#475569", disabled: "#94a3b8" },
    divider: "rgba(15, 23, 42, 0.08)",
    error: { main: "#ef4444", light: "#fca5a5", dark: "#b91c1c" },
    warning: { main: "#f59e0b", light: "#fcd34d", dark: "#b45309" },
    success: { main: "#10b981", light: "#6ee7b7", dark: "#047857" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: { WebkitFontSmoothing: "antialiased", MozOsxFontSmoothing: "grayscale" },
        "@keyframes shimmer": { "0%": { backgroundPosition: "200% 0" }, "100%": { backgroundPosition: "-200% 0" } },
        "@keyframes pulse": { "0%, 100%": { opacity: 0.5, transform: "scale(1)" }, "50%": { opacity: 0.8, transform: "scale(1.05)" } },
        "@keyframes fadeIn": { from: { opacity: 0, transform: "translateY(8px)" }, to: { opacity: 1, transform: "translateY(0)" } },
        "*, *::before, *::after": { "&:focus-visible": { outline: "2px solid #2563eb", outlineOffset: 2 } },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 12, padding: "8px 24px", transition: "box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)" },
        contained: { boxShadow: "0 4px 14px 0 rgba(37, 99, 235, 0.28)", "&:hover": { boxShadow: "0 6px 20px rgba(37, 99, 235, 0.22)", transform: "translateY(-1px)" }, "&:active": { transform: "translateY(0)" } },
        containedError: { boxShadow: "0 4px 14px 0 rgba(239, 68, 68, 0.22)", "&:hover": { boxShadow: "0 6px 20px rgba(239, 68, 68, 0.18)" } },
        outlined: { borderWidth: "1.5px", borderColor: "rgba(15, 23, 42, 0.15)", color: "#0f172a", "&:hover": { borderWidth: "1.5px", borderColor: "#0f172a", backgroundColor: "transparent" } },
        text: { color: "#475569", "&:hover": { backgroundColor: "rgba(15, 23, 42, 0.04)", color: "#0f172a" } },
      },
    },
    MuiCard: { styleOverrides: { root: { borderRadius: 12, border: "1px solid rgba(15, 23, 42, 0.06)", boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -2px rgba(0, 0, 0, 0.02)", backgroundImage: "none" } } },
    MuiPaper: {
      styleOverrides: {
        elevation1: { boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05)", border: "1px solid rgba(15, 23, 42, 0.06)" },
        elevation2: { boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)", border: "1px solid rgba(15, 23, 42, 0.06)" },
        elevation3: { boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05)", border: "1px solid rgba(15, 23, 42, 0.06)" },
      },
    },
    MuiTextField: {
      defaultProps: { size: "small" },
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 12, backgroundColor: "#ffffff", transition: "box-shadow 0.2s, border-color 0.2s, background-color 0.2s",
            "& fieldset": { borderColor: "rgba(15, 23, 42, 0.15)" }, "&:hover fieldset": { borderColor: "rgba(15, 23, 42, 0.3)" },
            "&.Mui-focused fieldset": { borderWidth: "2px", borderColor: "#2563eb" }, "&.Mui-focused": { boxShadow: "0 0 0 4px rgba(37, 99, 235, 0.1)" },
          },
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          border: "none",
          "& .MuiDataGrid-cell": { borderBottom: "1px solid rgba(15, 23, 42, 0.04)", color: "#475569", fontSize: "0.9rem" },
          "& .MuiDataGrid-columnHeaders": { backgroundColor: "#f8fafc", borderBottom: "1px solid rgba(15, 23, 42, 0.08)", borderTop: "none" },
          "& .MuiDataGrid-columnHeaderTitle": { fontWeight: 600, color: "#0f172a", textTransform: "none", fontSize: "0.75rem", letterSpacing: "0.03em" },
          "& .MuiDataGrid-row:hover": { backgroundColor: "rgba(15, 23, 42, 0.02)" },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { borderRadius: 8, fontWeight: 600, letterSpacing: "0.02em" },
        colorSuccess: { backgroundColor: "rgba(16, 185, 129, 0.1)", color: "#047857" },
        colorWarning: { backgroundColor: "rgba(245, 158, 11, 0.1)", color: "#b45309" },
        colorError: { backgroundColor: "rgba(239, 68, 68, 0.1)", color: "#b91c1c" },
        colorInfo: { backgroundColor: "rgba(59, 130, 246, 0.1)", color: "#1d4ed8" },
        colorSecondary: { backgroundColor: "rgba(15, 23, 42, 0.06)", color: "#475569" },
      },
    },
  },
});

const DARK_THEME = createTheme({
  ...BASE_CONFIG,
  palette: {
    mode: "dark",
    primary: { main: "#38bdf8", light: "#7dd3fc", dark: "#0284c7", contrastText: "#0f172a" },
    secondary: { main: "#94a3b8", light: "#cbd5e1", dark: "#64748b", contrastText: "#0f172a" },
    background: { default: "#020617", paper: "#0f172a" },
    text: { primary: "#f8fafc", secondary: "#94a3b8", disabled: "#475569" },
    divider: "rgba(255, 255, 255, 0.08)",
    error: { main: "#f87171", light: "#fca5a5", dark: "#ef4444" },
    warning: { main: "#fbbf24", light: "#fcd34d", dark: "#f59e0b" },
    success: { main: "#34d399", light: "#6ee7b7", dark: "#10b981" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: { WebkitFontSmoothing: "antialiased", MozOsxFontSmoothing: "grayscale" },
        "@keyframes shimmer": { "0%": { backgroundPosition: "200% 0" }, "100%": { backgroundPosition: "-200% 0" } },
        "@keyframes pulse": { "0%, 100%": { opacity: 0.5, transform: "scale(1)" }, "50%": { opacity: 0.8, transform: "scale(1.05)" } },
        "@keyframes fadeIn": { from: { opacity: 0, transform: "translateY(8px)" }, to: { opacity: 1, transform: "translateY(0)" } },
        "*, *::before, *::after": { "&:focus-visible": { outline: "2px solid #38bdf8", outlineOffset: 2 } },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 12, padding: "8px 24px", transition: "box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)" },
        contained: { boxShadow: "0 4px 14px 0 rgba(56, 189, 248, 0.39)", "&:hover": { boxShadow: "0 6px 20px rgba(56, 189, 248, 0.23)", transform: "translateY(-1px)" }, "&:active": { transform: "translateY(0)" } },
        containedError: { boxShadow: "0 4px 14px 0 rgba(248, 113, 113, 0.26)", "&:hover": { boxShadow: "0 6px 20px rgba(248, 113, 113, 0.2)" } },
        outlined: { borderWidth: "1.5px", borderColor: "rgba(255, 255, 255, 0.2)", color: "#f8fafc", "&:hover": { borderWidth: "1.5px", borderColor: "#f8fafc", backgroundColor: "rgba(255, 255, 255, 0.05)" } },
        text: { color: "#cbd5e1", "&:hover": { backgroundColor: "rgba(255, 255, 255, 0.05)", color: "#ffffff" } },
      },
    },
    MuiCard: { styleOverrides: { root: { borderRadius: 12, border: "1px solid rgba(255, 255, 255, 0.08)", boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2)", backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0))" } } },
    MuiPaper: {
      styleOverrides: {
        elevation1: { boxShadow: "0 1px 3px 0 rgba(0, 0, 0, 0.3)", border: "1px solid rgba(255, 255, 255, 0.08)", backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0))" },
        elevation2: { boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.3)", border: "1px solid rgba(255, 255, 255, 0.08)", backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0))" },
        elevation3: { boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.4)", border: "1px solid rgba(255, 255, 255, 0.08)", backgroundImage: "linear-gradient(rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0))" },
      },
    },
    MuiTextField: {
      defaultProps: { size: "small" },
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 12, backgroundColor: "rgba(15, 23, 42, 0.5)", transition: "box-shadow 0.2s, border-color 0.2s, background-color 0.2s",
            "& fieldset": { borderColor: "rgba(255, 255, 255, 0.15)" }, "&:hover fieldset": { borderColor: "rgba(255, 255, 255, 0.3)" },
            "&.Mui-focused fieldset": { borderWidth: "2px", borderColor: "#38bdf8" }, "&.Mui-focused": { boxShadow: "0 0 0 4px rgba(56, 189, 248, 0.1)" },
          },
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          border: "none",
          "& .MuiDataGrid-cell": { borderBottom: "1px solid rgba(255, 255, 255, 0.04)", color: "#cbd5e1", fontSize: "0.9rem" },
          "& .MuiDataGrid-columnHeaders": { backgroundColor: "rgba(15, 23, 42, 0.5)", borderBottom: "1px solid rgba(255, 255, 255, 0.08)", borderTop: "none" },
          "& .MuiDataGrid-columnHeaderTitle": { fontWeight: 600, color: "#f8fafc", textTransform: "none", fontSize: "0.75rem", letterSpacing: "0.03em" },
          "& .MuiDataGrid-row:hover": { backgroundColor: "rgba(255, 255, 255, 0.02)" },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { borderRadius: 8, fontWeight: 600, letterSpacing: "0.02em" },
        colorSuccess: { backgroundColor: "rgba(52, 211, 153, 0.15)", color: "#34d399", border: "1px solid rgba(52, 211, 153, 0.2)" },
        colorWarning: { backgroundColor: "rgba(251, 191, 36, 0.15)", color: "#fbbf24", border: "1px solid rgba(251, 191, 36, 0.2)" },
        colorError: { backgroundColor: "rgba(248, 113, 113, 0.15)", color: "#f87171", border: "1px solid rgba(248, 113, 113, 0.2)" },
        colorInfo: { backgroundColor: "rgba(56, 189, 248, 0.15)", color: "#38bdf8", border: "1px solid rgba(56, 189, 248, 0.2)" },
        colorSecondary: { backgroundColor: "rgba(255, 255, 255, 0.08)", color: "#cbd5e1", border: "1px solid rgba(255, 255, 255, 0.1)" },
      },
    },
    MuiTooltip: { styleOverrides: { tooltip: { backgroundColor: "#1e293b", color: "#f8fafc", fontSize: "0.8125rem", borderRadius: 8, border: "1px solid rgba(255, 255, 255, 0.08)" } } },
  },
});

const HIGH_CONTRAST_THEME = createTheme({
  ...BASE_CONFIG,
  palette: {
    mode: "light",
    primary: { main: "#000000", light: "#333333", dark: "#000000", contrastText: "#ffffff" },
    secondary: { main: "#000080", light: "#3333ff", dark: "#000050", contrastText: "#ffffff" },
    background: { default: "#ffffff", paper: "#ffffff" },
    text: { primary: "#000000", secondary: "#000080", disabled: "#808080" },
    divider: "#000000",
    error: { main: "#cc0000", light: "#ff3333", dark: "#990000" },
    warning: { main: "#cc6600", light: "#ff9933", dark: "#994d00" },
    success: { main: "#006600", light: "#009900", dark: "#003300" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: { WebkitFontSmoothing: "antialiased" },
        "*::before, *::after": { "&:focus-visible": { outline: "3px solid #000000", outlineOffset: 2 } },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 8, fontWeight: 700, py: 1.5, px: 4, borderWidth: "2px" },
        contained: { boxShadow: "0 2px 4px 0 rgba(0, 0, 0, 0.2)", "&:hover": { boxShadow: "0 6px 8px -1px rgba(0, 0, 0, 0.3)" } },
        outlined: { borderWidth: "2px", borderColor: "#000000", color: "#000000", "&:hover": { borderWidth: "2px", borderColor: "#000000", backgroundColor: "rgba(0, 0, 0, 0.05)" } },
      },
    },
    MuiCard: { styleOverrides: { root: { borderRadius: 8, border: "2px solid #000000", boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)", backgroundImage: "none" } } },
    MuiPaper: {
      styleOverrides: {
        elevation1: { border: "1px solid #000000" },
        elevation2: { border: "2px solid #000000" },
        elevation3: { border: "2px solid #000000" },
      },
    },
    MuiTextField: {
      defaultProps: { size: "medium" },
      styleOverrides: {
        root: {
          borderRadius: 8,
          "& .MuiOutlinedInput-root": {
            borderRadius: 8, backgroundColor: "#ffffff",
            "& fieldset": { borderColor: "#000000", borderWidth: "2px" },
            "&:hover fieldset": { borderColor: "#000000", borderWidth: "2px" },
            "&.Mui-focused fieldset": { borderWidth: "3px", borderColor: "#000000" },
          },
        },
      },
    },
    MuiDataGrid: {
      styleOverrides: {
        root: {
          border: "2px solid #000000",
          "& .MuiDataGrid-cell": { borderBottom: "1px solid #000000", color: "#000000", fontSize: "0.95rem" },
          "& .MuiDataGrid-columnHeaders": { backgroundColor: "#e0e0e0", borderBottom: "2px solid #000000" },
          "& .MuiDataGrid-columnHeaderTitle": { fontWeight: 700, color: "#000000", textTransform: "none", fontSize: "0.8rem" },
          "& .MuiDataGrid-row:hover": { backgroundColor: "rgba(0, 0, 0, 0.05)" },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { borderRadius: 6, fontWeight: 700, border: "1px solid #000000", fontSize: "0.8rem" },
        colorSuccess: { backgroundColor: "#ccffcc", color: "#006600", border: "2px solid #006600" },
        colorWarning: { backgroundColor: "#ffffcc", color: "#663300", border: "2px solid #cc6600" },
        colorError: { backgroundColor: "#ffcccc", color: "#cc0000", border: "2px solid #cc0000" },
        colorInfo: { backgroundColor: "#cce5ff", color: "#000080", border: "2px solid #000080" },
      },
    },
    MuiTooltip: { styleOverrides: { tooltip: { backgroundColor: "#000000", color: "#ffffff", fontSize: "0.875rem", borderRadius: 4, border: "2px solid #ffffff" } } },
  },
});

const createResponsiveTheme = (baseTheme: import("@mui/material").Theme) =>
  responsiveFontSizes(baseTheme, { breakpoints: ["sm", "md", "lg", "xl"], factor: 0.5 });

export type ThemeMode = "light" | "dark" | "auto" | "high-contrast";

export const createAppTheme = (mode: ThemeMode = "light") => {
  let baseTheme;
  if (mode === "dark") baseTheme = DARK_THEME;
  else if (mode === "high-contrast") baseTheme = HIGH_CONTRAST_THEME;
  else if (mode === "auto") {
    const prefersDark = typeof window !== "undefined" && window.matchMedia("(prefers-color-scheme: dark)").matches;
    baseTheme = prefersDark ? DARK_THEME : LIGHT_THEME;
  } else baseTheme = LIGHT_THEME;
  return createResponsiveTheme(baseTheme);
};
