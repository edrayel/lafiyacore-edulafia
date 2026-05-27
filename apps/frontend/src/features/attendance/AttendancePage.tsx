import { useState, useCallback, useEffect, useMemo } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Toolbar,
  Tooltip,
  OutlinedInput,
  Checkbox,
  ListItemText,
  Typography,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DEFAULT_CLASS_OPTIONS } from '@/shared/config/constants';
import {
  Save as SaveIcon,
  CheckCircle,
  Cancel,
  Schedule,
  EventBusy,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format, subMonths } from 'date-fns';
import { getAttendance, markAttendance, getAttendanceStats, exportEMISAttendance } from './api';
import { getStudents } from '../students/api';
import type { AttendanceRecord } from '@/shared/types';
import type { Student } from '@/shared/types';

type AttendanceStatus = 'present' | 'absent' | 'late' | 'excused' | '';

interface StudentAttendanceRow {
  studentId: string;
  name: string;
  admissionNumber: string;
  status: AttendanceStatus;
  reasonCode: string;
  symptomCodes: string[];
  notes: string;
}

const statusConfig: Record<
  Exclude<AttendanceStatus, ''>,
  { label: string; color: 'success' | 'error' | 'warning' | 'info'; icon: typeof CheckCircle }
> = {
  present: { label: 'Present', color: 'success', icon: CheckCircle },
  absent: { label: 'Absent', color: 'error', icon: Cancel },
  late: { label: 'Late', color: 'warning', icon: Schedule },
  excused: { label: 'Excused', color: 'info', icon: EventBusy },
};

const SYMPTOMS = [
  { code: 'fever', label: 'Fever' },
  { code: 'cough', label: 'Cough' },
  { code: 'fatigue', label: 'Fatigue' },
  { code: 'headache', label: 'Headache' },
  { code: 'vomiting', label: 'Vomiting' },
  { code: 'diarrhea', label: 'Diarrhea' },
  { code: 'rash', label: 'Rash' },
];

export function AttendancePage() {
  const queryClient = useQueryClient();
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [bulkStatus, setBulkStatus] = useState<AttendanceStatus>('');

  const dateStr = selectedDate ? format(selectedDate, 'yyyy-MM-dd') : '';

  // Fetch students for selected class
  const { data: studentsData } = useQuery({
    queryKey: ['students-by-class', selectedClass],
    queryFn: () => getStudents({ class_id: selectedClass, per_page: 100 }),
    enabled: !!selectedClass,
  });

  const { data: attendanceRecords } = useQuery({
    queryKey: ['attendance', selectedClass, dateStr],
    queryFn: () =>
      getAttendance({ classId: selectedClass || undefined, date: dateStr || undefined }),
    enabled: !!selectedClass && !!dateStr,
  });

  // Store only user edits locally
  const [edits, setEdits] = useState<Record<string, Partial<StudentAttendanceRow>>>({});

  // Reset edits when class or date changes
  useEffect(() => {
    setEdits({});
    setBulkStatus('');
  }, [selectedClass, dateStr]);

  const students = useMemo(() => studentsData?.items ?? [], [studentsData?.items]);

  const rows = useMemo(() => {
    return students.map((s: Student) => {
      // 1. Get server record if exists
      const serverRecord = attendanceRecords?.find((r: AttendanceRecord) => r.student_id === s.id);

      // 2. Base row from server data or default
      const baseRow: StudentAttendanceRow = {
        studentId: s.id,
        name: `${s.first_name} ${s.last_name}`,
        admissionNumber: s.admission_number,
        status: serverRecord ? (serverRecord.status as AttendanceStatus) : '',
        reasonCode: serverRecord?.reason_code || '',
        symptomCodes: serverRecord?.symptom_codes || [],
        notes: serverRecord?.notes || '',
      };

      // 3. Apply any local edits
      return { ...baseRow, ...(edits[s.id] || {}) };
    });
  }, [students, attendanceRecords, edits]);

  const { data: stats } = useQuery({
    queryKey: ['attendance-stats', selectedClass, dateStr],
    queryFn: () => getAttendanceStats(selectedClass, dateStr),
    enabled: !!selectedClass && !!dateStr,
  });

  const markMutation = useMutation({
    mutationFn: (
      records: {
        student_id: string;
        class_id: string;
        date: string;
        status: string;
        reason_code?: string;
        symptom_codes?: string[];
        notes?: string;
      }[]
    ) => markAttendance(selectedClass, dateStr, records),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attendance'] });
      queryClient.invalidateQueries({ queryKey: ['attendance-stats'] });
    },
  });

  const updateRowStatus = useCallback(
    (studentId: string, status: AttendanceStatus) => {
      setEdits((prev) => {
        const current = prev[studentId] || {};
        const baseRow = rows.find((r) => r.studentId === studentId);
        const currentReason =
          current.reasonCode !== undefined ? current.reasonCode : baseRow?.reasonCode;
        const currentSymptoms =
          current.symptomCodes !== undefined ? current.symptomCodes : baseRow?.symptomCodes;

        return {
          ...prev,
          [studentId]: {
            ...current,
            status,
            reasonCode: status === 'absent' ? currentReason : '',
            symptomCodes: status === 'absent' && currentReason === 'sick' ? currentSymptoms : [],
          },
        };
      });
    },
    [rows]
  );

  const updateRowReason = useCallback(
    (studentId: string, reasonCode: string) => {
      setEdits((prev) => {
        const current = prev[studentId] || {};
        const baseRow = rows.find((r) => r.studentId === studentId);
        const currentSymptoms =
          current.symptomCodes !== undefined ? current.symptomCodes : baseRow?.symptomCodes;

        return {
          ...prev,
          [studentId]: {
            ...current,
            reasonCode,
            symptomCodes: reasonCode === 'sick' ? currentSymptoms : [],
          },
        };
      });
    },
    [rows]
  );

  const updateRowSymptoms = useCallback((studentId: string, symptomCodes: string[]) => {
    setEdits((prev) => ({ ...prev, [studentId]: { ...(prev[studentId] || {}), symptomCodes } }));
  }, []);

  const handleBulkMark = useCallback(() => {
    if (bulkStatus) {
      const newEdits: Record<string, Partial<StudentAttendanceRow>> = {};
      students.forEach((s: Student) => {
        newEdits[s.id] = { status: bulkStatus, reasonCode: '', symptomCodes: [] };
      });
      setEdits((prev) => ({ ...prev, ...newEdits }));
    }
  }, [bulkStatus, students]);

  const handleSave = useCallback(() => {
    if (!selectedClass || !dateStr) return;
    const records = rows
      .filter((r) => r.status !== '')
      .map((r) => ({
        student_id: r.studentId,
        class_id: selectedClass,
        date: dateStr,
        status: r.status,
        reason_code: r.status === 'absent' ? r.reasonCode || undefined : undefined,
        symptom_codes:
          r.status === 'absent' && r.reasonCode === 'sick' ? r.symptomCodes : undefined,
        notes: r.notes || undefined,
      }));
    if (records.length > 0) {
      markMutation.mutate(records);
    }
  }, [rows, selectedClass, dateStr, markMutation]);

  const exportMutation = useMutation({
    mutationFn: () => {
      const endDate = new Date();
      const startDate = subMonths(endDate, 3); // 3 months for a term
      return exportEMISAttendance(
        format(startDate, 'yyyy-MM-dd'),
        format(endDate, 'yyyy-MM-dd'),
        selectedClass || undefined
      );
    },
    onSuccess: (data) => {
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `emis_attendance_export_${format(new Date(), 'yyyyMMdd')}.json`;
      a.click();
      URL.revokeObjectURL(url);
    },
  });

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography
            variant="h4"
            sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
          >
            Attendance
          </Typography>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={() => exportMutation.mutate()}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? 'Exporting...' : 'Export EMIS Report'}
          </Button>
        </Box>

        <Paper
          elevation={0}
          sx={{
            p: 2,
            mb: 3,
            border: '1px solid',
            borderColor: 'divider',
            bgcolor: 'background.paper',
          }}
        >
          <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
            <FormControl size="small" sx={{ minWidth: 180 }}>
              <InputLabel>Class</InputLabel>
              <Select
                value={selectedClass}
                label="Class"
                onChange={(e) => setSelectedClass(e.target.value)}
              >
                {DEFAULT_CLASS_OPTIONS.map((cls) => (
                  <MenuItem key={cls.value} value={cls.value}>{cls.label}</MenuItem>
                ))}
              </Select>
            </FormControl>

            <DatePicker
              label="Date"
              value={selectedDate}
              onChange={(date) => setSelectedDate(date)}
              slotProps={{ textField: { size: 'small', sx: { minWidth: 180 } } }}
            />

            <Box sx={{ flexGrow: 1 }} />

            {selectedClass && (
              <>
                <FormControl size="small" sx={{ minWidth: 140 }}>
                  <InputLabel>Bulk Mark</InputLabel>
                  <Select
                    value={bulkStatus}
                    label="Bulk Mark"
                    onChange={(e) => setBulkStatus(e.target.value as AttendanceStatus)}
                  >
                    <MenuItem value="">Select...</MenuItem>
                    <MenuItem value="present">All Present</MenuItem>
                    <MenuItem value="absent">All Absent</MenuItem>
                  </Select>
                </FormControl>
                <Button variant="outlined" onClick={handleBulkMark} disabled={!bulkStatus}>
                  Apply
                </Button>
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  onClick={handleSave}
                  disabled={markMutation.isPending}
                >
                  Save Attendance
                </Button>
              </>
            )}
          </Toolbar>
        </Paper>

        {stats && (
          <Grid container spacing={2} sx={{ mb: 2 }}>
            {Object.entries(statusConfig).map(([key, config]) => {
              const Icon = config.icon;
              const count = stats[key as keyof typeof stats] ?? 0;
              return (
                <Grid size={{ xs: 6, sm: 3 }} key={key}>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Icon color={config.color} />
                      <Box>
                        <Typography variant="caption" color="textSecondary">
                          {config.label}
                        </Typography>
                        <Typography variant="h5">{count}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        )}

        {selectedClass && (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Admission #</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell align="center">Status</TableCell>
                  <TableCell>Absence Details</TableCell>
                  <TableCell>Notes</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow key={row.studentId}>
                    <TableCell>{row.admissionNumber}</TableCell>
                    <TableCell>{row.name}</TableCell>
                    <TableCell align="center">
                      <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center' }}>
                        {(
                          Object.entries(statusConfig) as [
                            Exclude<AttendanceStatus, ''>,
                            (typeof statusConfig)[Exclude<AttendanceStatus, ''>],
                          ][]
                        ).map(([key, config]) => {
                          const Icon = config.icon;
                          const isSelected = row.status === key;
                          return (
                            <Tooltip key={key} title={config.label}>
                              <Button
                                aria-label={config.label}
                                size="small"
                                variant={isSelected ? 'contained' : 'outlined'}
                                color={config.color}
                                onClick={() => updateRowStatus(row.studentId, key)}
                                sx={{ minWidth: 32, p: 0.5 }}
                              >
                                <Icon fontSize="small" />
                              </Button>
                            </Tooltip>
                          );
                        })}
                      </Box>
                    </TableCell>
                    <TableCell sx={{ minWidth: 200 }}>
                      {row.status === 'absent' && (
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          <FormControl size="small" fullWidth>
                            <InputLabel>Reason</InputLabel>
                            <Select
                              value={row.reasonCode}
                              label="Reason"
                              onChange={(e) => updateRowReason(row.studentId, e.target.value)}
                            >
                              <MenuItem value="sick">Sick</MenuItem>
                              <MenuItem value="family">Family Emergency</MenuItem>
                              <MenuItem value="excused">Excused</MenuItem>
                              <MenuItem value="suspended">Suspended</MenuItem>
                              <MenuItem value="unknown">Unknown</MenuItem>
                            </Select>
                          </FormControl>
                          {row.reasonCode === 'sick' && (
                            <FormControl size="small" fullWidth>
                              <InputLabel>Symptoms</InputLabel>
                              <Select
                                multiple
                                value={row.symptomCodes}
                                onChange={(e) => {
                                  const value = e.target.value;
                                  updateRowSymptoms(
                                    row.studentId,
                                    typeof value === 'string' ? value.split(',') : value
                                  );
                                }}
                                input={<OutlinedInput label="Symptoms" />}
                                renderValue={(selected) =>
                                  selected
                                    .map((s) => SYMPTOMS.find((sym) => sym.code === s)?.label)
                                    .join(', ')
                                }
                              >
                                {SYMPTOMS.map((symptom) => (
                                  <MenuItem key={symptom.code} value={symptom.code}>
                                    <Checkbox
                                      checked={row.symptomCodes.indexOf(symptom.code) > -1}
                                    />
                                    <ListItemText primary={symptom.label} />
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          )}
                        </Box>
                      )}
                    </TableCell>
                    <TableCell>
                      <OutlinedInput
                        size="small"
                        placeholder="Add note..."
                        value={row.notes}
                        onChange={(e) =>
                          setEdits((prev) => ({
                            ...prev,
                            [row.studentId]: {
                              ...(prev[row.studentId] || {}),
                              notes: e.target.value,
                            },
                          }))
                        }
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {!selectedClass && (
          <Paper sx={{ p: 4, textAlign: 'center' }}>
            <Typography color="textSecondary">
              Select a class and date to take attendance
            </Typography>
          </Paper>
        )}
      </>
    </LocalizationProvider>
  );
}
