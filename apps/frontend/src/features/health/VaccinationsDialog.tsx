import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
} from '@mui/material';
import type { CreateVaccinationPayload } from './api';

interface VaccinationsDialogProps {
  open: boolean;
  onClose: () => void;
  vaccForm: Partial<CreateVaccinationPayload>;
  setVaccForm: React.Dispatch<React.SetStateAction<Partial<CreateVaccinationPayload>>>;
  onSubmit: () => void;
  isPending: boolean;
}

export function VaccinationsDialog({
  open,
  onClose,
  vaccForm,
  setVaccForm,
  onSubmit,
  isPending,
}: VaccinationsDialogProps) {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add Vaccination Record</DialogTitle>
      <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Student ID"
          value={vaccForm.student_id ?? ''}
          onChange={(e) => setVaccForm((f) => ({ ...f, student_id: e.target.value }))}
          fullWidth
        />
        <TextField
          label="Vaccine Name"
          value={vaccForm.vaccine_name ?? ''}
          onChange={(e) => setVaccForm((f) => ({ ...f, vaccine_name: e.target.value }))}
          fullWidth
        />
        <TextField
          label="Vaccine Code"
          value={vaccForm.vaccine_code ?? ''}
          onChange={(e) => setVaccForm((f) => ({ ...f, vaccine_code: e.target.value }))}
          fullWidth
        />
        <TextField
          label="Administration Date"
          type="date"
          value={vaccForm.administration_date ?? ''}
          onChange={(e) => setVaccForm((f) => ({ ...f, administration_date: e.target.value }))}
          fullWidth
          InputLabelProps={{ shrink: true }}
        />
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField
            label="Dose Number"
            type="number"
            value={vaccForm.dose_number ?? ''}
            onChange={(e) => setVaccForm((f) => ({ ...f, dose_number: +e.target.value }))}
            fullWidth
          />
          <TextField
            label="Facility"
            value={vaccForm.administering_facility ?? ''}
            onChange={(e) =>
              setVaccForm((f) => ({ ...f, administering_facility: e.target.value }))
            }
            fullWidth
          />
        </Box>
        <TextField
          label="Lot Number"
          value={vaccForm.lot_number ?? ''}
          onChange={(e) => setVaccForm((f) => ({ ...f, lot_number: e.target.value }))}
          fullWidth
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onSubmit} variant="contained" disabled={isPending}>
          Save Record
        </Button>
      </DialogActions>
    </Dialog>
  );
}
