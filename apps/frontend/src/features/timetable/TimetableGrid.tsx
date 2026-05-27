import { useMemo } from 'react';
import { Box, Paper, Typography } from '@mui/material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import type { TimetableEntry } from '@/features/staff/api';

interface TimetableGridProps {
  entries: TimetableEntry[];
  timetableId: string;
  isLoading: boolean;
  onAddEntry: (day?: number, period?: number) => void;
  onEditEntry: (entry: TimetableEntry) => void;
}

const DAY_LABELS = ['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const CELL_COLORS = [
  '#1976d2', '#388e3c', '#d32f2f', '#f57c00', '#7b1fa2',
  '#0097a7', '#c2185b', '#689f38', '#e64a19', '#512da8',
];

function getSubjectColor(subject: string): string {
  let hash = 0;
  for (let i = 0; i < subject.length; i++) {
    hash = subject.charCodeAt(i) + ((hash << 5) - hash);
  }
  return CELL_COLORS[Math.abs(hash) % CELL_COLORS.length];
}

export function TimetableGrid({ entries, isLoading, onAddEntry, onEditEntry }: TimetableGridProps) {
  const timeSlots = useMemo(() => {
    const slots = new Map<string, { start_time: string; end_time: string }>();
    entries.forEach(e => {
      const key = `${e.start_time}-${e.end_time}`;
      if (!slots.has(key)) {
        slots.set(key, { start_time: e.start_time, end_time: e.end_time });
      }
    });
    return Array.from(slots.values()).sort((a, b) => a.start_time.localeCompare(b.start_time));
  }, [entries]);

  const gridMap = useMemo(() => {
    const map = new Map<number, Map<string, TimetableEntry>>();
    entries.forEach(e => {
      const key = `${e.start_time}-${e.end_time}`;
      if (!map.has(e.day_of_week)) map.set(e.day_of_week, new Map());
      map.get(e.day_of_week)!.set(key, e);
    });
    return map;
  }, [entries]);

  if (isLoading) {
    return <SkeletonPage rows={5} cardCount={0} />;
  }

  if (entries.length === 0) {
    return <DataEmptyState title="No entries" message="Click a cell to add a class" />;
  }

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: `100px repeat(5, 1fr)`,
        gap: 0.5,
        overflowX: 'auto',
      }}
    >
      <Box sx={{ p: 1, fontWeight: 600 }}>Time</Box>
      {[1, 2, 3, 4, 5].map(day => (
        <Box key={day} sx={{ p: 1, fontWeight: 600, textAlign: 'center' }}>
          {DAY_LABELS[day]}
        </Box>
      ))}
      {timeSlots.map((slot, slotIndex) => (
        <Box
          key={`${slot.start_time}-${slot.end_time}`}
          sx={{ display: 'contents' }}
        >
          <Box
            sx={{
              p: 1,
              display: 'flex',
              alignItems: 'center',
              fontSize: '0.8rem',
              color: 'text.secondary',
              fontWeight: 500,
            }}
          >
            {slot.start_time} - {slot.end_time}
          </Box>
          {[1, 2, 3, 4, 5].map(day => {
            const entry = gridMap.get(day)?.get(`${slot.start_time}-${slot.end_time}`);
            return (
              <Paper
                key={`${day}-${slot.start_time}`}
                variant="outlined"
                sx={{
                  minHeight: 80,
                  p: 1,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  transition: 'box-shadow 0.15s, border-color 0.15s',
                  '&:hover': {
                    boxShadow: 1,
                    borderColor: 'primary.main',
                  },
                  ...(entry
                    ? {
                        borderLeft: 4,
                        borderLeftColor: getSubjectColor(entry.subject_name ?? entry.subject_id),
                      }
                    : {
                        borderStyle: 'dashed',
                        borderColor: 'divider',
                        color: 'text.disabled',
                        '&:hover .add-label': { opacity: 1 },
                      }),
                }}
                onClick={() => {
                  if (entry) onEditEntry(entry);
                  else onAddEntry(day, slotIndex);
                }}
              >
                {entry ? (
                  <>
                    <Typography
                      variant="body2"
                      sx={{ fontWeight: 700, fontSize: '0.8rem', lineHeight: 1.2 }}
                      noWrap
                    >
                      {entry.subject_name || entry.subject_id}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{ fontSize: '0.7rem', lineHeight: 1.2, color: 'text.secondary' }}
                      noWrap
                    >
                      {entry.staff_name || entry.staff_id}
                    </Typography>
                    {entry.room && (
                      <Typography
                        variant="caption"
                        sx={{ fontSize: '0.65rem', lineHeight: 1.2, color: 'text.disabled' }}
                        noWrap
                      >
                        {entry.room}
                      </Typography>
                    )}
                  </>
                ) : (
                  <Typography
                    className="add-label"
                    variant="caption"
                    sx={{
                      textAlign: 'center',
                      opacity: 0,
                      transition: 'opacity 0.15s',
                      fontSize: '0.75rem',
                    }}
                  >
                    +
                  </Typography>
                )}
              </Paper>
            );
          })}
        </Box>
      ))}
    </Box>
  );
}
