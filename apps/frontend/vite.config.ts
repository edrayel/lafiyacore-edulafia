import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
import path from 'path';

export default defineConfig(({ mode }) => {
  // Load env variables including .env.local
  const env = loadEnv(mode, process.cwd(), '');

  // Read dynamic ports, fallback to defaults
  const frontendPort = parseInt(env.FRONTEND_PORT || '5173', 10);
  const backendPort = env.BACKEND_PORT || '8000';
  const backendUrl = env.VITE_API_URL || `http://localhost:${backendPort}`;

  return {
    plugins: [
      react(),
      VitePWA({
        registerType: 'autoUpdate',
        workbox: {
          maximumFileSizeToCacheInBytes: 5000000,
          globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2,ttf}'],
          runtimeCaching: [
            {
                urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
              handler: 'CacheFirst',
              options: {
                cacheName: 'google-fonts-cache',
                expiration: {
                  maxEntries: 10,
                  maxAgeSeconds: 60 * 60 * 24 * 365, // 1 year
                },
                cacheableResponse: {
                  statuses: [0, 200],
                },
              },
            },
          ],
        },
        manifest: {
          name: 'EduLafia',
          short_name: 'EduLafia',
          description: 'Integrated school management and adolescent health surveillance',
          theme_color: '#0c8ce9',
          background_color: '#ffffff',
          display: 'standalone',
          start_url: '/',
          icons: [
            {
              src: '/icons/icon-192x192.png',
              sizes: '192x192',
              type: 'image/png',
            },
            {
              src: '/icons/icon-512x512.png',
              sizes: '512x512',
              type: 'image/png',
            },
          ],
        },
      }),
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        events: 'events',
      },
    },
    define: {
      global: 'window',
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: [
              'react',
              'react-dom',
              '@mui/material',
              '@mui/icons-material',
              '@tanstack/react-query',
              '@tanstack/react-router',
            ],
            pouchdb: ['pouchdb'],
          },
        },
      },
    },
    server: {
      port: frontendPort,
      proxy: {
        '/api': {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
    test: {
      globals: true,
      environment: 'jsdom',
      setupFiles: ['./src/setupTests.ts'],
      exclude: ['e2e/**', 'node_modules/**'],
    },
  };
});
