import { useState } from "react";
import { useLocation, Link } from "@tanstack/react-router";
import {
  AppBar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Avatar,
  useTheme,
  useMediaQuery,
  ListSubheader,
  Collapse,
} from "@mui/material";
import {
  Menu as MenuIcon,
  Logout,
  ExpandLess,
  ExpandMore,
  School as SchoolIcon,
} from "@mui/icons-material";
import { useAuthStore } from "../stores/authStore";
import { ThemeSwitcher } from "./ThemeSwitcher";
import { useNavPermissions } from "../auth/permissions";

const DRAWER_WIDTH = 260;

export function AppLayout({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    Core: true,
  });

  const location = useLocation();
  const { user, logout } = useAuthStore();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("lg"));
  const filteredSections = useNavPermissions();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const toggleSection = (label: string) => {
    setExpandedSections((prev) => ({ ...prev, [label]: !prev[label] }));
  };

  const isActive = (path: string) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  const drawerContent = (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        bgcolor: "background.paper",
        color: "text.primary",
        borderRight: "1px solid",
        borderColor: "divider",
      }}
    >
      <Box
        component={Link}
        to="/"
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          px: 3,
          py: 3,
          borderBottom: "1px solid",
          borderColor: "divider",
          textDecoration: "none",
          cursor: "pointer",
        }}
      >
        <Box
          sx={{
            p: 0.75,
            backgroundColor: "primary.main",
            borderRadius: 1.5,
            display: "flex",
            boxShadow: (t) => `0 2px 10px ${t.palette.mode === "dark" ? "rgba(56, 189, 248, 0.3)" : "rgba(37, 99, 235, 0.3)"}`,
          }}
        >
          <SchoolIcon sx={{ fontSize: 20, color: "#fff" }} />
        </Box>
        <Typography
          variant="h6"
          sx={{ fontWeight: 700, color: "text.primary", letterSpacing: "-0.5px", fontSize: "1.1rem" }}
        >
          EduLafia
        </Typography>
      </Box>

      <List sx={{ p: 2, overflowY: "auto", flexGrow: 1 }}>
        {filteredSections.map((section) => (
          <Box key={section.label} sx={{ mb: 2 }}>
            <ListSubheader
              component="div"
              onClick={() => toggleSection(section.label)}
              onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleSection(section.label); } }}
              role="button"
              aria-expanded={expandedSections[section.label]}
              tabIndex={0}
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                cursor: "pointer",
                bgcolor: "transparent",
                lineHeight: "24px",
                px: 1,
                py: 0.5,
                mb: 0.5,
                "&:hover": { "& .MuiTypography-root": { color: "text.primary" } },
              }}
            >
              <Typography
                variant="overline"
                sx={{
                  fontWeight: 600,
                  color: "text.secondary",
                  letterSpacing: "0.5px",
                  textTransform: "uppercase",
                  transition: "color 0.2s",
                }}
              >
                {section.label}
              </Typography>
              {expandedSections[section.label] ? (
                <ExpandLess sx={{ fontSize: 16, color: "text.secondary" }} />
              ) : (
                <ExpandMore sx={{ fontSize: 16, color: "text.secondary" }} />
              )}
            </ListSubheader>
            <Collapse in={expandedSections[section.label]} timeout="auto" unmountOnExit>
              <List
                component="div"
                disablePadding
                sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}
              >
                {section.items.map((item) => {
                  const active = isActive(item.path);
                  return (
                    <ListItem key={item.label} disablePadding>
                      <ListItemButton
                        component={Link}
                        to={item.path}
                        onClick={() => isMobile && setMobileOpen(false)}
                        sx={{
                          py: 1,
                          px: 1.5,
                          borderRadius: 1.5,
                          color: active ? "primary.main" : "text.secondary",
                          bgcolor: active ? (t) => t.palette.mode === "dark" ? "rgba(56, 189, 248, 0.08)" : "rgba(37, 99, 235, 0.08)" : "transparent",
                          transition: "all 0.2s",
                          "&:hover": {
                            bgcolor: active ? (t) => t.palette.mode === "dark" ? "rgba(56, 189, 248, 0.12)" : "rgba(37, 99, 235, 0.12)" : "action.hover",
                            color: "primary.main",
                            "& .MuiListItemIcon-root": { color: "primary.main" },
                          },
                        }}
                      >
                        <ListItemIcon
                          sx={{
                            minWidth: 32,
                            color: active ? "primary.main" : "text.secondary",
                            transition: "color 0.2s",
                          }}
                        >
                          <item.icon sx={{ fontSize: 20 }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={item.label}
                          primaryTypographyProps={{
                            variant: "body2",
                            fontWeight: active ? 500 : 400,
                            fontSize: "0.9rem",
                          }}
                        />
                      </ListItemButton>
                    </ListItem>
                  );
                })}
              </List>
            </Collapse>
          </Box>
        ))}
      </List>

      <Box sx={{ p: 2, borderTop: "1px solid", borderColor: "divider" }}>
        <List disablePadding>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => logout()}
              sx={{
                py: 1,
                px: 1.5,
                borderRadius: 1.5,
                color: "text.secondary",
                transition: "all 0.2s",
                "&:hover": {
                  bgcolor: (t) => t.palette.mode === "dark" ? "rgba(239, 68, 68, 0.1)" : "rgba(239, 68, 68, 0.06)",
                  color: "error.main",
                  "& .MuiListItemIcon-root": { color: "error.main" },
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 32, color: "text.secondary" }}>
                <Logout sx={{ fontSize: 20 }} />
              </ListItemIcon>
              <ListItemText
                primary="Sign Out"
                primaryTypographyProps={{ variant: "body2", fontSize: "0.9rem" }}
              />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", bgcolor: "background.default" }}>
      <Box
        component="nav"
        sx={{
          width: { lg: DRAWER_WIDTH },
          flexShrink: { lg: 0 },
        }}
      >
        {isMobile ? (
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{ keepMounted: true }}
            sx={{
              display: { xs: "block", lg: "none" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: DRAWER_WIDTH,
                borderRight: "none",
              },
            }}
          >
            {drawerContent}
          </Drawer>
        ) : (
          <Drawer
            variant="permanent"
            open
            sx={{
              display: { xs: "none", lg: "block" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: DRAWER_WIDTH,
                borderRight: "none",
              },
            }}
          >
            {drawerContent}
          </Drawer>
        )}
      </Box>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          width: { lg: `calc(100% - ${DRAWER_WIDTH}px)` },
          minHeight: "100vh",
        }}
      >
        <AppBar
          position="sticky"
          elevation={0}
          sx={{
            bgcolor: (t) => t.palette.mode === "dark" ? "rgba(15, 23, 42, 0.8)" : "rgba(255, 255, 255, 0.8)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid",
            borderColor: "divider",
            color: "text.primary",
            zIndex: theme.zIndex.drawer - 1,
          }}
        >
          <Toolbar sx={{ px: { xs: 2, sm: 4 }, minHeight: "64px !important" }}>
            {isMobile && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2, color: "text.secondary" }}
              >
                <MenuIcon />
              </IconButton>
            )}

            <Box sx={{ flexGrow: 1 }} />

            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <ThemeSwitcher />
              <Box sx={{ height: 32, width: "1px", bgcolor: "divider", mx: 1 }} />
              <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, cursor: "pointer" }}>
                <Box sx={{ display: { xs: "none", sm: "block" }, textAlign: "right" }}>
                  <Typography
                    variant="body2"
                    sx={{ fontWeight: 600, color: "text.primary", lineHeight: 1.2 }}
                  >
                    {user?.first_name} {user?.last_name}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: "text.secondary", textTransform: "capitalize" }}
                  >
                    {user?.role?.replace("_", " ")}
                  </Typography>
                </Box>
                <Avatar
                  alt={user?.first_name || "User"}
                  sx={{
                    width: 36,
                    height: 36,
                    bgcolor: "primary.main",
                    color: "primary.contrastText",
                    fontWeight: 600,
                    fontSize: "0.9rem",
                  }}
                >
                  {user?.first_name?.[0] || "U"}
                </Avatar>
              </Box>
            </Box>
          </Toolbar>
        </AppBar>

        <Box
          sx={{
            p: { xs: 2, sm: 3, md: 4 },
            flexGrow: 1,
            display: "flex",
            flexDirection: "column",
            maxWidth: 1600,
            mx: "auto",
            width: "100%",
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
}
