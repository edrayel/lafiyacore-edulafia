import { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
} from '@mui/material';
import { Send as SendIcon, PictureAsPdf as PdfIcon } from '@mui/icons-material';
import { useQuery, useMutation } from '@tanstack/react-query';
import { getAcademicMetadata, generateReportCard, sendReportCard, type ReportCardSubjectResult } from './api';
import { getStudents } from '../students/api';
import type { Student } from '@/shared/types';
import { useToastStore } from '@/shared/stores/toastStore';

interface ReportCardPreviewProps {
  open: boolean;
  onClose: () => void;
}

export function ReportCardPreview({ open, onClose }: ReportCardPreviewProps) {
  const [studentId, setStudentId] = useState('');

  const { data: metadata } = useQuery({
    queryKey: ['academicMetadata'],
    queryFn: getAcademicMetadata,
    enabled: open,
  });

  const { data: studentsData } = useQuery({
    queryKey: ['students', metadata?.class?.id],
    queryFn: () => getStudents({ per_page: 100 }),
    enabled: open && !!metadata?.class?.id,
  });

  const termId = metadata?.term?.id;
  const { data: report, isLoading: reportLoading } = useQuery({
    queryKey: ['reportCard', studentId, termId],
    queryFn: () => generateReportCard(studentId, termId!),
    enabled: !!(studentId && termId),
  });

  const sendMutation = useMutation({
    mutationFn: (method: 'whatsapp' | 'sms') =>
      sendReportCard(studentId, termId!, method),
    onSuccess: (_data, method) => {
      useToastStore.getState().addToast(`Report card sent via ${method} successfully!`, 'success');
    },
  });

  const handlePrint = () => {
    window.print();
  };

  const studentInfo = studentsData?.items?.find((s: Student) => s.id === studentId);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          '@media print': { display: 'none' },
        }}
      >
        <Typography variant="h6">Report Card Preview</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            startIcon={<SendIcon />}
            onClick={() => sendMutation.mutate('whatsapp')}
            disabled={!report || sendMutation.isPending}
            variant="outlined"
            size="small"
            color="success"
          >
            WhatsApp
          </Button>
          <Button
            startIcon={<SendIcon />}
            onClick={() => sendMutation.mutate('sms')}
            disabled={!report || sendMutation.isPending}
            variant="outlined"
            size="small"
            color="secondary"
          >
            SMS
          </Button>
          <Button
            startIcon={<PdfIcon />}
            onClick={handlePrint}
            disabled={!report}
            variant="contained"
            size="small"
          >
            Generate PDF
          </Button>
        </Box>
      </DialogTitle>
      <DialogContent id="report-print-area">
        <Box sx={{ '@media print': { display: 'none' }, mb: 4, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Select Student</InputLabel>
            <Select
              value={studentId}
              label="Select Student"
              onChange={(e) => setStudentId(e.target.value)}
            >
              {studentsData?.items?.map((s: Student) => (
                <MenuItem key={s.id} value={s.id}>
                  {s.first_name} {s.last_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        {reportLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : report && studentInfo ? (
          <Box sx={{ p: 4, '@media print': { p: 0 } }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>
                EduLafia Academy
              </Typography>
              <Typography variant="h6" color="textSecondary">
                Termly Academic Report
              </Typography>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  Student Name
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {studentInfo.first_name} {studentInfo.last_name}
                </Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  Class
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {metadata?.class?.name}
                </Typography>
              </Box>
              <Box>
                <Typography variant="subtitle2" color="textSecondary">
                  Term
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {metadata?.term?.name}
                </Typography>
              </Box>
            </Box>

            <Divider sx={{ mb: 3 }} />

            <TableContainer
              component={Paper}
              elevation={0}
              sx={{ border: '1px solid', borderColor: 'divider', mb: 4 }}
            >
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: 'action.hover' }}>
                    <TableCell>Subject</TableCell>
                    <TableCell align="right">CA (30)</TableCell>
                    <TableCell align="right">Exam (70)</TableCell>
                    <TableCell align="right">Total</TableCell>
                    <TableCell align="center">Grade</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {report.subject_results?.map((g: ReportCardSubjectResult) => (
                    <TableRow key={g.subject_id}>
                      <TableCell component="th" scope="row">
                        {g.subject_name || g.subject_code}
                      </TableCell>
                      <TableCell align="right">{g.ca_total}</TableCell>
                      <TableCell align="right">{g.exam_score}</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                        {g.total_score}
                      </TableCell>
                      <TableCell align="center">
                        <Typography
                          fontWeight="bold"
                          color={
                            g.grade?.startsWith('A')
                              ? 'success.main'
                              : g.grade?.startsWith('F')
                                ? 'error.main'
                                : 'text.primary'
                          }
                        >
                          {g.grade}
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell colSpan={3} align="right">
                      <Typography fontWeight="bold">Overall Average:</Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography fontWeight="bold">{report.average}%</Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Typography fontWeight="bold" color="primary">
                        {report.overall_grade}
                      </Typography>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 8 }}>
              <Box sx={{ width: '40%', textAlign: 'center' }}>
                <Divider sx={{ mb: 1 }} />
                <Typography variant="caption">Form Teacher's Signature</Typography>
              </Box>
              <Box sx={{ width: '40%', textAlign: 'center' }}>
                <Divider sx={{ mb: 1 }} />
                <Typography variant="caption">Principal's Signature</Typography>
              </Box>
            </Box>
          </Box>
        ) : studentId ? (
          <Box sx={{ p: 4, textAlign: 'center', color: 'text.secondary' }}>
            No report card data found for this student.
          </Box>
        ) : (
          <Box sx={{ p: 4, textAlign: 'center', color: 'text.secondary' }}>
            Please select a student to view their report card.
          </Box>
        )}
      </DialogContent>
      <DialogActions sx={{ '@media print': { display: 'none' } }}>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>

      {/* Print styles */}
      <style>{`
        @media print {
          @page { margin: 15mm; }
          body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
          .MuiDialog-root { position: static !important; }
          .MuiDialog-paper {
            box-shadow: none !important;
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          .MuiDialogActions-root { display: none !important; }
          #report-print-area { margin: 0; padding: 0; }
          #report-print-area, #report-print-area * { visibility: visible; }
          .MuiDialog-root, .MuiDialog-container { visibility: visible; }
        }
      `}</style>
    </Dialog>
  );
}
