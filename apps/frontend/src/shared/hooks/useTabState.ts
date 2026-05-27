import { useCallback } from 'react';

export function useTabState(key = 'tab') {
  const searchParams = new URLSearchParams(window.location.search);
  const tab = parseInt(searchParams.get(key) || '0', 10);

  const setTab = useCallback(
    (value: number) => {
      const params = new URLSearchParams(window.location.search);
      if (value === 0) {
        params.delete(key);
      } else {
        params.set(key, String(value));
      }
      const newUrl = params.toString()
        ? `${window.location.pathname}?${params.toString()}`
        : window.location.pathname;
      window.history.replaceState(null, '', newUrl);
    },
    [key]
  );

  return [tab, setTab] as const;
}
