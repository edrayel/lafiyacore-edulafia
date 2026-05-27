import React from 'react';
import { Box, Typography, useTheme, useMediaQuery } from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';

export function AuthLayout({ children }: { children: React.ReactNode }) {
  const theme = useTheme();
  const isMdUp = useMediaQuery(theme.breakpoints.up('md'));

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f8fafc' }}>
      {/* Left Side - Graphic/Branding */}
      {isMdUp && (
        <Box
          sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'flex-start',
            p: { md: 6, lg: 10 },
            backgroundColor: 'primary.dark',
            color: 'primary.contrastText',
            backgroundImage: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Subtle background decoration */}
          <Box
            sx={{
              position: 'absolute',
              top: '-15%',
              right: '-10%',
              width: '60%',
              height: '60%',
              borderRadius: '50%',
              backgroundColor: 'rgba(255,255,255,0.08)',
              filter: 'blur(100px)',
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              bottom: '-15%',
              left: '-10%',
              width: '60%',
              height: '60%',
              borderRadius: '50%',
              backgroundColor: 'rgba(255,255,255,0.08)',
              filter: 'blur(100px)',
            }}
          />

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 5, zIndex: 1 }}>
            <Box
              sx={{
                p: 1.5,
                backgroundColor: 'rgba(255,255,255,0.15)',
                backdropFilter: 'blur(12px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <SchoolIcon sx={{ fontSize: 44, color: '#ffffff' }} />
            </Box>
            <Typography
              variant="h3"
              sx={{ fontWeight: 800, letterSpacing: '-0.5px', color: '#ffffff' }}
            >
              EduLafia
            </Typography>
          </Box>

          <Typography
            variant="h4"
            sx={{
              fontWeight: 300,
              lineHeight: 1.4,
              maxWidth: 500,
              mb: 4,
              zIndex: 1,
              color: '#f8fafc',
            }}
          >
            Empowering the next generation of education and health tracking.
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: 'rgba(255,255,255,0.75)',
              maxWidth: 480,
              zIndex: 1,
              fontSize: '1.1rem',
              lineHeight: 1.6,
            }}
          >
            Access your comprehensive dashboard to manage students, staff, academics, and wellbeing
            all in one unified platform.
          </Typography>
        </Box>
      )}

      {/* Right Side - Form Container */}
      <Box
        sx={{
          flex: { xs: 1, md: 0.8, lg: 0.6 },
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          p: { xs: 3, sm: 6, md: 8 },
          backgroundColor: '#ffffff',
          color: '#0f172a', // Force dark text on the white background regardless of global theme
          boxShadow: { md: '-20px 0 40px rgba(0,0,0,0.04)' },
          zIndex: 2,
        }}
      >
        <Box sx={{ width: '100%', maxWidth: 440 }}>
          {/* Mobile Logo */}
          {!isMdUp && (
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 1.5,
                mb: 6,
                justifyContent: 'center',
              }}
            >
              <Box sx={{ p: 1, backgroundColor: 'primary.main', borderRadius: 2, display: 'flex' }}>
                <SchoolIcon sx={{ fontSize: 28, color: 'primary.contrastText' }} />
              </Box>
              <Typography
                variant="h4"
                sx={{ fontWeight: 800, color: '#0f172a', letterSpacing: '-0.5px' }}
              >
                EduLafia
              </Typography>
            </Box>
          )}

          {/* Override child typography colors to ensure visibility against white background */}
          <Box
            sx={{
              '& .MuiTypography-root': { color: '#0f172a' },
              '& .MuiTypography-colorTextSecondary': { color: '#64748b' },
              '& .MuiInputBase-input': { color: '#0f172a' },
              '& .MuiInputLabel-root': { color: '#64748b' },
              '& .MuiOutlinedInput-notchedOutline': { borderColor: '#cbd5e1' },
              '& .MuiOutlinedInput-root:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: '#94a3b8',
              },
            }}
          >
            {children}
          </Box>
        </Box>
      </Box>
    </Box>
  );
}
