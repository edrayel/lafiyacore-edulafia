import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider,
} from '@mui/material';
import { Print as PrintIcon } from '@mui/icons-material';
import type { Payment } from './api';

interface ReceiptViewProps {
  open: boolean;
  onClose: () => void;
  payment: Payment | null;
}

export function ReceiptView({ open, onClose, payment }: ReceiptViewProps) {
  const handlePrint = () => {
    window.print();
  };

  if (!payment) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          '@media print': { display: 'none' },
        }}
      >
        <Typography variant="h6">Receipt</Typography>
        <Button startIcon={<PrintIcon />} onClick={handlePrint} variant="outlined" size="small">
          Print
        </Button>
      </DialogTitle>

      {/* Printable Area */}
      <DialogContent id="receipt-print-area">
        <Box sx={{ p: 4, '@media print': { p: 0 } }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Typography variant="h4" sx={{ fontWeight: 800, color: 'primary.main', mb: 1 }}>
              EduLafia
            </Typography>
            <Typography variant="body1" color="textSecondary">
              Official Payment Receipt
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Box>
              <Typography variant="caption" color="textSecondary" display="block">
                Receipt No.
              </Typography>
              <Typography variant="body1" fontWeight="bold">
                {payment.receipt_number}
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'right' }}>
              <Typography variant="caption" color="textSecondary" display="block">
                Date
              </Typography>
              <Typography variant="body1">
                {new Date(payment.payment_date).toLocaleDateString()}
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ mb: 3 }}>
            <GridRow label="Student Name" value={payment.student_name} />
            <GridRow label="Payment Method" value={payment.payment_method.toUpperCase()} />
            <GridRow label="Status" value={payment.status.toUpperCase()} />
          </Box>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body1" color="textSecondary">
              Fee Type
            </Typography>
            <Typography variant="body1" fontWeight="bold">
              {payment.fee_type}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6">Total Paid</Typography>
            <Typography variant="h6" fontWeight="bold">
              ₦{payment.amount_paid.toLocaleString()}
            </Typography>
          </Box>

          <Box sx={{ textAlign: 'center', mt: 6 }}>
            <Typography variant="caption" color="textSecondary">
              Thank you for your payment. Keep this receipt for your records.
            </Typography>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ '@media print': { display: 'none' } }}>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>

      {/* Global styles specifically for printing this dialog */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #receipt-print-area, #receipt-print-area * {
            visibility: visible;
          }
          #receipt-print-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
          }
        }
      `}</style>
    </Dialog>
  );
}

function GridRow({ label, value }: { label: string; value: string }) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
      <Typography variant="body2" color="textSecondary">
        {label}
      </Typography>
      <Typography variant="body2" fontWeight="medium">
        {value}
      </Typography>
    </Box>
  );
}
