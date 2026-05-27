import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
} from '@mui/material';
import type { Screening } from './api';

interface ScreeningsDialogProps {
  open: boolean;
  onClose: () => void;
  screeningForm: Partial<Screening>;
  setScreeningForm: React.Dispatch<React.SetStateAction<Partial<Screening>>>;
  onSubmit: () => void;
  isPending: boolean;
}

export function ScreeningsDialog({
  open,
  onClose,
  screeningForm,
  setScreeningForm,
  onSubmit,
  isPending,
}: ScreeningsDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Log Health Screening</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Student ID"
          value={screeningForm.student_id ?? ''}
          onChange={(e) => setScreeningForm((f) => ({ ...f, student_id: e.target.value }))}
          fullWidth
        />
        <TextField
          label="Screening Type"
          value={screeningForm.screening_type ?? ''}
          onChange={(e) => setScreeningForm((f) => ({ ...f, screening_type: e.target.value }))}
          fullWidth
        />
        <TextField
          label="Date Conducted"
          type="date"
          value={screeningForm.screening_date ?? ''}
          onChange={(e) => setScreeningForm((f) => ({ ...f, screening_date: e.target.value }))}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            label="Height (cm)"
            type="number"
            value={screeningForm.height ?? ''}
            onChange={(e) => setScreeningForm((f) => ({ ...f, height: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Weight (kg)"
            type="number"
            value={screeningForm.weight ?? ''}
            onChange={(e) => setScreeningForm((f) => ({ ...f, weight: +e.target.value }))}
            fullWidth
          />
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            label="Vision Left"
            type="number"
            value={screeningForm.vision_left ?? ''}
            onChange={(e) => setScreeningForm((f) => ({ ...f, vision_left: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Hearing Left"
            value={screeningForm.hearing_left ?? ''}
            onChange={(e) => setScreeningForm((f) => ({ ...f, hearing_left: e.target.value }))}
            fullWidth
          />
        </Box>
        <TextField
          label="Dental"
          value={screeningForm.dental_notes ?? ''}
          onChange={(e) => setScreeningForm((f) => ({ ...f, dental_notes: e.target.value }))}
          fullWidth
        />
        <TextField
          label="General Notes"
          value={screeningForm.follow_up_notes ?? ''}
          onChange={(e) => setScreeningForm((f) => ({ ...f, follow_up_notes: e.target.value }))}
          fullWidth
          multiline
          rows={3}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onSubmit} variant="contained" disabled={isPending}>
          Save Screening
        </Button>
      </DialogActions>
    </Dialog>
  );
}
