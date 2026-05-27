import { Box, Skeleton, Paper } from '@mui/material';

interface SkeletonPageProps {
  rows?: number;
  cardCount?: number;
}

export function SkeletonPage({ rows = 5, cardCount = 4 }: SkeletonPageProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Skeleton variant="text" width={200} height={32} />
      <Box sx={{ display: 'grid', gridTemplateColumns: `repeat(auto-fill, minmax(200px, 1fr))`, gap: 2 }}>
        {Array.from({ length: cardCount }).map((_, i) => (
          <Paper key={i} sx={{ p: 3, borderRadius: 3 }}>
            <Skeleton variant="circular" width={40} height={40} sx={{ mb: 2 }} />
            <Skeleton variant="text" width="60%" height={28} />
            <Skeleton variant="text" width="40%" height={20} />
          </Paper>
        ))}
      </Box>
      <Paper sx={{ borderRadius: 3, p: 2 }}>
        <Skeleton variant="rectangular" height={40} sx={{ mb: 2, borderRadius: 1 }} />
        {Array.from({ length: rows }).map((_, i) => (
          <Skeleton key={i} variant="rectangular" height={52} sx={{ mb: 1, borderRadius: 1 }} />
        ))}
      </Paper>
    </Box>
  );
}
