import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './App';
import './shared/styles/animations.css';
import { GlobalErrorBoundary } from './shared/components/GlobalErrorBoundary';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <GlobalErrorBoundary>
      <App />
    </GlobalErrorBoundary>
  </StrictMode>
);
