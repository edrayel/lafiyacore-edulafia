import { Suspense, useMemo } from 'react';
import { QueryClient, QueryClientProvider, MutationCache } from '@tanstack/react-query';
import { RouterProvider, createRouter } from '@tanstack/react-router';
import { ThemeProvider, CssBaseline, CircularProgress, Box } from '@mui/material';
import { routeTree } from './app/router';
import { createAppTheme } from './shared/theme';
import { ToastContainer } from './shared/components/ToastContainer';
import { useThemeStore } from './shared/stores/themeStore';

const router = createRouter({ routeTree });

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

import { useToastStore } from './shared/stores/toastStore';

export function App() {
  const queryClient = useMemo(
    () =>
      new QueryClient({
        defaultOptions: { queries: { staleTime: 5 * 60 * 1000, retry: 1 } },
        mutationCache: new MutationCache({
          onError: (error) => {
            let message = 'An unexpected error occurred';
            if (error instanceof Error) {
              message = error.message;
            }
            if (error && typeof error === 'object' && 'response' in error) {
              const err = error as { response?: { data?: { detail?: string; message?: string } } };
              message = err.response?.data?.detail || err.response?.data?.message || message;
            }
            useToastStore.getState().addToast(message, 'error');
          },
        }),
      }),
    []
  );

  const { mode } = useThemeStore();
  const theme = useMemo(() => createAppTheme(mode), [mode]);

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Suspense fallback={<Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}><CircularProgress /></Box>}>
          <RouterProvider router={router} />
        </Suspense>
        <ToastContainer />
      </ThemeProvider>
    </QueryClientProvider>
  );
}
