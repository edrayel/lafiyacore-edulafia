import { useMemo, useState } from 'react';
import {
  Box,
  Typography,
  IconButton,
  Button,
  Tooltip,
  Chip,
  Popover,
  List,
  ListItemButton,
  ListItemText,
} from '@mui/material';
import { ChevronLeft, ChevronRight, Today } from '@mui/icons-material';
import { SkeletonPage } from '@/shared/components/SkeletonPage';
import type { CalendarEvent } from './api';

interface CalendarViewProps {
  events: CalendarEvent[];
  isLoading: boolean;
  currentDate: Date;
  onDateChange: (date: Date) => void;
  onAddEvent: (date?: Date) => void;
  onEditEvent: (event: CalendarEvent) => void;
}

function getDaysInMonth(date: Date): Date[] {
  const year = date.getFullYear();
  const month = date.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startPad = firstDay.getDay();

  const days: Date[] = [];

  for (let i = startPad - 1; i >= 0; i--) {
    days.push(new Date(year, month - 1, new Date(year, month, 0).getDate() - i));
  }

  for (let d = 1; d <= lastDay.getDate(); d++) {
    days.push(new Date(year, month, d));
  }

  const totalCells = Math.ceil(days.length / 7) * 7;
  for (let i = days.length; i < totalCells; i++) {
    days.push(new Date(year, month + 1, i - days.length + 1));
  }

  return days;
}

const colorMap: Record<string, string> = {
  exam: 'error.main',
  holiday: 'success.main',
  meeting: 'warning.main',
  sports: 'info.main',
  general: 'grey.400',
};

function DayCell({
  day,
  events,
  isCurrentMonth,
  isToday,
  onEditEvent,
  onAddEvent,
}: {
  day: Date;
  events: CalendarEvent[];
  isCurrentMonth: boolean;
  isToday: boolean;
  onEditEvent: (event: CalendarEvent) => void;
  onAddEvent: (date?: Date) => void;
}) {
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const open = Boolean(anchorEl);

  const handleClick = (e: React.MouseEvent<HTMLElement>) => {
    if (events.length === 1) {
      onEditEvent(events[0]);
    } else if (events.length > 1) {
      setAnchorEl(e.currentTarget);
    } else {
      onAddEvent(day);
    }
  };

  const eventTitles = events.map(ev => ev.title).join('\n');

  return (
    <>
      <Tooltip title={events.length > 0 ? eventTitles : ''} disableHoverListener={events.length === 0}>
        <Box
          onClick={handleClick}
          sx={{
            minHeight: 90,
            p: 0.5,
            borderRight: '1px solid',
            borderBottom: '1px solid',
            borderColor: 'divider',
            bgcolor: isCurrentMonth ? 'background.paper' : 'grey.50',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            outline: isToday ? '2px solid' : 'none',
            outlineColor: 'primary.main',
            outlineOffset: -2,
            opacity: isCurrentMonth ? 1 : 0.45,
            '&:hover': { bgcolor: 'action.hover' },
          }}
        >
          <Typography
            variant="caption"
            sx={{
              fontWeight: isToday ? 700 : 400,
              color: isToday ? 'primary.main' : 'text.primary',
              lineHeight: 1.2,
            }}
          >
            {day.getDate()}
          </Typography>
          <Box sx={{ display: 'flex', gap: 0.3, flexWrap: 'wrap', alignItems: 'center', mt: 0.5 }}>
            {events.slice(0, 3).map(ev => (
              <Box
                key={ev.id}
                sx={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  bgcolor: colorMap[ev.event_type] || 'grey.400',
                }}
              />
            ))}
            {events.length > 3 && (
              <Chip
                label={`+${events.length - 3} more`}
                size="small"
                variant="outlined"
                sx={{ height: 16, fontSize: 9, '& .MuiChip-label': { px: 0.5 } }}
              />
            )}
          </Box>
        </Box>
      </Tooltip>
      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={() => setAnchorEl(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'left' }}
      >
        <List dense sx={{ minWidth: 180 }}>
          {events.map(ev => (
            <ListItemButton
              key={ev.id}
              onClick={() => {
                setAnchorEl(null);
                onEditEvent(ev);
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    bgcolor: colorMap[ev.event_type] || 'grey.400',
                    flexShrink: 0,
                  }}
                />
                <ListItemText
                  primary={ev.title}
                  primaryTypographyProps={{ variant: 'body2' }}
                  secondary={
                    ev.start_date
                      ? new Date(ev.start_date).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })
                      : undefined
                  }
                />
              </Box>
            </ListItemButton>
          ))}
        </List>
      </Popover>
    </>
  );
}

export function CalendarView({
  events,
  isLoading,
  currentDate,
  onDateChange,
  onAddEvent,
  onEditEvent,
}: CalendarViewProps) {
  const days = useMemo(() => getDaysInMonth(currentDate), [currentDate]);

  const eventsByDay = useMemo(() => {
    const map = new Map<string, CalendarEvent[]>();
    events.forEach(ev => {
      const key = new Date(ev.start_date).toDateString();
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(ev);
    });
    return map;
  }, [events]);

  const monthLabel = currentDate.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
  });
  const todayStr = new Date().toDateString();

  if (isLoading) {
    return <SkeletonPage rows={3} cardCount={0} />;
  }

  const handlePrev = () => {
    onDateChange(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const handleNext = () => {
    onDateChange(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const handleToday = () => {
    onDateChange(new Date());
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
          <IconButton onClick={handlePrev} size="small">
            <ChevronLeft />
          </IconButton>
          <Typography variant="h6" sx={{ fontWeight: 600, minWidth: 180, textAlign: 'center' }}>
            {monthLabel}
          </Typography>
          <IconButton onClick={handleNext} size="small">
            <ChevronRight />
          </IconButton>
        </Box>
        <Button variant="outlined" size="small" startIcon={<Today />} onClick={handleToday}>
          Today
        </Button>
      </Box>

      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: 'repeat(7, 1fr)',
          borderTop: '1px solid',
          borderLeft: '1px solid',
          borderColor: 'divider',
        }}
      >
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
          <Box
            key={d}
            sx={{
              textAlign: 'center',
              py: 0.75,
              fontWeight: 600,
              color: 'text.secondary',
              fontSize: 12,
              borderRight: '1px solid',
              borderBottom: '1px solid',
              borderColor: 'divider',
              bgcolor: 'grey.50',
            }}
          >
            {d}
          </Box>
        ))}
        {days.map((day, i) => {
          const dayKey = day.toDateString();
          const dayEvents = eventsByDay.get(dayKey) || [];
          const isCurrent = day.getMonth() === currentDate.getMonth();
          const isToday = dayKey === todayStr;
          return (
            <DayCell
              key={i}
              day={day}
              events={dayEvents}
              isCurrentMonth={isCurrent}
              isToday={isToday}
              onEditEvent={onEditEvent}
              onAddEvent={onAddEvent}
            />
          );
        })}
      </Box>
    </Box>
  );
}
