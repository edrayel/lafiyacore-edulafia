import { useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import { DataEmptyState } from '@/shared/components/DataEmptyState';
import { Add as AddIcon, MenuBook as BookIcon } from '@mui/icons-material';
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getBooks,
  createBook,
  lendBook,
  type Book,
  type CreateBookPayload,
  type LendBookPayload,
} from './api';

export function LibraryPage() {
  const [bookOpen, setBookOpen] = useState(false);
  const [lendOpen, setLendOpen] = useState(false);
  const [bookForm, setBookForm] = useState<Partial<CreateBookPayload>>({});
  const [lendForm, setLendForm] = useState<Partial<LendBookPayload>>({});
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ['books'], queryFn: () => getBooks() });

  const create = useMutation({
    mutationFn: (p: CreateBookPayload) => createBook(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['books'] });
      setBookOpen(false);
      setBookForm({});
    },
  });
  const lend = useMutation({
    mutationFn: (p: LendBookPayload) => lendBook(p),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['books'] });
      setLendOpen(false);
      setLendForm({});
    },
  });

  const columns: GridColDef<Book>[] = [
    { field: 'title', headerName: 'Title', width: 250 },
    { field: 'author', headerName: 'Author', width: 180 },
    { field: 'category', headerName: 'Category', width: 140 },
    { field: 'available_copies', headerName: 'Available', width: 100 },
    { field: 'total_copies', headerName: 'Total', width: 80 },
    {
      field: 'availability',
      headerName: 'Status',
      width: 120,
      renderCell: (p) => (
        <Chip
          label={p.row.available_copies > 0 ? 'Available' : 'Out of Stock'}
          size="small"
          color={p.row.available_copies > 0 ? 'success' : 'error'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: '',
      width: 100,
      sortable: false,
      renderCell: (p) => (
        <Button
          aria-label="Lend"
          size="small"
          disabled={p.row.available_copies <= 0}
          onClick={() => {
            setLendForm({ book_id: p.row.id });
            setLendOpen(true);
          }}
        >
          <BookIcon fontSize="small" />
        </Button>
      ),
    },
  ];

  return (
    <>
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 800, color: 'text.primary', letterSpacing: '-0.5px' }}
        >
          Library
        </Typography>
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
        <Toolbar>
          <Box sx={{ flexGrow: 1 }} />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{
              borderRadius: 2,
              px: 3,
              py: 1,
              fontWeight: 600,
              boxShadow: '0 4px 14px 0 rgba(56, 189, 248, 0.39)',
              '&:hover': { boxShadow: '0 6px 20px rgba(56, 189, 248, 0.23)' },
            }}
            onClick={() => setBookOpen(true)}
          >
            Add Book
          </Button>
        </Toolbar>
      </Paper>
      <Paper
        elevation={0}
        sx={{
          height: 500,
          width: '100%',
          border: '1px solid',
          borderColor: 'divider',
          bgcolor: 'background.paper',
          overflow: 'hidden',
        }}
      >
        <DataGrid
          rows={data ?? []}
          columns={columns}
          loading={isLoading}
          getRowId={(r) => r.id}
          initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
          pageSizeOptions={[10, 25, 50]}
          slots={{ noRowsOverlay: () => <DataEmptyState title="No books found" message="There are no books to display at this time." /> }}
        />
      </Paper>
      <Dialog open={bookOpen} onClose={() => setBookOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Book</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Title"
            value={bookForm.title ?? ''}
            onChange={(e) => setBookForm((f) => ({ ...f, title: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Author"
            value={bookForm.author ?? ''}
            onChange={(e) => setBookForm((f) => ({ ...f, author: e.target.value }))}
            fullWidth
          />
          <FormControl fullWidth>
            <InputLabel>Category</InputLabel>
            <Select
              value={bookForm.category ?? ''}
              label="Category"
              onChange={(e) => setBookForm((f) => ({ ...f, category: e.target.value }))}
            >
              <MenuItem value="textbook">Textbook</MenuItem>
              <MenuItem value="fiction">Fiction</MenuItem>
              <MenuItem value="reference">Reference</MenuItem>
              <MenuItem value="science">Science</MenuItem>
              <MenuItem value="other">Other</MenuItem>
            </Select>
          </FormControl>
          <TextField
            label="ISBN"
            value={bookForm.isbn ?? ''}
            onChange={(e) => setBookForm((f) => ({ ...f, isbn: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Total Copies"
            type="number"
            value={bookForm.total_copies ?? ''}
            onChange={(e) => setBookForm((f) => ({ ...f, total_copies: +e.target.value }))}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBookOpen(false)}>Cancel</Button>
          <Button
            onClick={() => create.mutate(bookForm as CreateBookPayload)}
            variant="contained"
            disabled={create.isPending}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={lendOpen} onClose={() => setLendOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Lend Book</DialogTitle>
        <DialogContent sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Student ID"
            value={lendForm.student_id ?? ''}
            onChange={(e) => setLendForm((f) => ({ ...f, student_id: e.target.value }))}
            fullWidth
          />
          <TextField
            label="Due Date"
            type="date"
            value={lendForm.due_date ?? ''}
            onChange={(e) => setLendForm((f) => ({ ...f, due_date: e.target.value }))}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setLendOpen(false)}>Cancel</Button>
          <Button
            onClick={() => lend.mutate(lendForm as LendBookPayload)}
            variant="contained"
            disabled={lend.isPending}
          >
            Lend
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
