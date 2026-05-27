import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
} from '@mui/material';
import type { ExcusalPayload } from './api';

interface ExcusalDialogProps {
  open: boolean;
  onClose: () => void;
  excusalForm: Partial<ExcusalPayload>;
  setExcusalForm: React.Dispatch<React.SetStateAction<Partial<ExcusalPayload>>>;
  onSubmit: () => void;
  isPending: boolean;
}

export function ExcusalDialog({
  open,
  onClose,
  excusalForm,
  setExcusalForm,
  onSubmit,
  isPending,
}: ExcusalDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Submit Excusal</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Date"
          type="date"
          value={excusalForm.absence_date ?? ''}
          onChange={(e) => setExcusalForm((f) => ({ ...f, absence_date: e.target.value }))}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <TextField
          label="Details"
          value={excusalForm.details ?? ''}
          onChange={(e) => setExcusalForm((f) => ({ ...f, details: e.target.value }))}
          fullWidth
          multiline
          rows={3}
        />
        <TextField
          label="Reason"
          value={excusalForm.reason ?? ''}
          onChange={(e) => setExcusalForm((f) => ({ ...f, reason: e.target.value }))}
          fullWidth
          multiline
          rows={3}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={onSubmit}
          variant="contained"
          disabled={isPending || !excusalForm.absence_date || !excusalForm.reason}
        >
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
}
