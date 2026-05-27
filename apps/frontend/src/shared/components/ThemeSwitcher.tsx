import { useState } from 'react';
import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText, Tooltip } from '@mui/material';
import {
  Brightness7 as LightModeIcon,
  Brightness4 as DarkModeIcon,
  AutoMode as AutoModeIcon,
  Accessibility as HighContrastIcon,
} from '@mui/icons-material';
import { useThemeStore } from '../stores/themeStore';
import type { ThemeMode } from '../theme';

interface ThemeOption {
  mode: ThemeMode;
  label: string;
  icon: React.ReactNode;
}

const themeOptions: ThemeOption[] = [
  { mode: 'light', label: 'Light Mode', icon: <LightModeIcon /> },
  { mode: 'dark', label: 'Dark Mode', icon: <DarkModeIcon /> },
  { mode: 'auto', label: 'Auto (System)', icon: <AutoModeIcon /> },
  { mode: 'high-contrast', label: 'High Contrast', icon: <HighContrastIcon /> },
];

export function ThemeSwitcher() {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const { mode, setMode } = useThemeStore();

  const handleOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleModeChange = (newMode: ThemeMode) => {
    setMode(newMode);
    handleClose();
  };

  const getCurrentIcon = () => {
    switch (mode) {
      case 'dark':
        return <DarkModeIcon />;
      case 'auto':
        return <AutoModeIcon />;
      case 'high-contrast':
        return <HighContrastIcon />;
      default:
        return <LightModeIcon />;
    }
  };

  const getCurrentLabel = () => {
    const option = themeOptions.find((opt) => opt.mode === mode);
    return option?.label || 'Theme';
  };

  return (
    <>
      <Tooltip title={getCurrentLabel()}>
        <IconButton color="inherit" onClick={handleOpen}>
          {getCurrentIcon()}
        </IconButton>
      </Tooltip>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        PaperProps={{
          elevation: 0,
          sx: {
            minWidth: 180,
            mt: 1.5,
            borderRadius: 3,
            border: '1px solid',
            borderColor: 'divider',
            bgcolor: 'background.paper',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
            overflow: 'visible',
            '&::before': {
              content: '""',
              display: 'block',
              position: 'absolute',
              top: 0,
              right: 14,
              width: 10,
              height: 10,
              bgcolor: 'background.paper',
              transform: 'translateY(-50%) rotate(45deg)',
              zIndex: 0,
              borderLeft: '1px solid',
              borderTop: '1px solid',
              borderColor: 'divider',
            },
          },
        }}
      >
        {themeOptions.map((option) => (
          <MenuItem
            key={option.mode}
            onClick={() => handleModeChange(option.mode)}
            selected={mode === option.mode}
            sx={{
              borderRadius: 1.5,
              mx: 1,
              my: 0.5,
              py: 1,
              px: 2,
              '&.Mui-selected': {
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                color: '#2563eb',
                fontWeight: 600,
                '&:hover': {
                  backgroundColor: 'rgba(37, 99, 235, 0.15)',
                },
                '& .MuiListItemIcon-root': {
                  color: '#2563eb',
                },
              },
              '&:hover': {
                backgroundColor: 'rgba(15, 23, 42, 0.04)',
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 32 }}>{option.icon}</ListItemIcon>
            <ListItemText
              primary={option.label}
              primaryTypographyProps={{
                variant: 'body2',
                fontWeight: mode === option.mode ? 600 : 500,
              }}
            />
          </MenuItem>
        ))}
      </Menu>
    </>
  );
}
