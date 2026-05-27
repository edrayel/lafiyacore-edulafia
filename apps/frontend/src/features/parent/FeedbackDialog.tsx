import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import type { FeedbackPayload } from './api';

interface FeedbackDialogProps {
  open: boolean;
  onClose: () => void;
  feedbackForm: Partial<FeedbackPayload>;
  setFeedbackForm: React.Dispatch<React.SetStateAction<Partial<FeedbackPayload>>>;
  onSubmit: () => void;
  isPending: boolean;
}

export function FeedbackDialog({
  open,
  onClose,
  feedbackForm,
  setFeedbackForm,
  onSubmit,
  isPending,
}: FeedbackDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Submit Feedback</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Type</InputLabel>
          <Select
            value={feedbackForm.feedback_type ?? 'complaint'}
            label="Type"
            onChange={(e) =>
              setFeedbackForm((f) => ({
                ...f,
                feedback_type: e.target.value as FeedbackPayload['feedback_type'],
              }))
            }
          >
            <MenuItem value="complaint">Complaint</MenuItem>
            <MenuItem value="suggestion">Suggestion</MenuItem>
            <MenuItem value="praise">Praise</MenuItem>
            <MenuItem value="question">Question</MenuItem>
          </Select>
        </FormControl>

        <TextField
          label="Subject"
          value={feedbackForm.subject ?? ''}
          onChange={(e) => setFeedbackForm((f) => ({ ...f, subject: e.target.value }))}
          fullWidth
        />

        <TextField
          label="Message"
          value={feedbackForm.message ?? ''}
          onChange={(e) => setFeedbackForm((f) => ({ ...f, message: e.target.value }))}
          fullWidth
          multiline
          rows={4}
        />

        <FormControlLabel
          control={
            <Checkbox
              checked={feedbackForm.is_anonymous ?? false}
              onChange={(e) => setFeedbackForm((f) => ({ ...f, is_anonymous: e.target.checked }))}
            />
          }
          label="Submit anonymously"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={onSubmit}
          variant="contained"
          disabled={isPending || !feedbackForm.subject || !feedbackForm.message}
        >
          Submit
        </Button>
      </DialogActions>
    </Dialog>
  );
}
