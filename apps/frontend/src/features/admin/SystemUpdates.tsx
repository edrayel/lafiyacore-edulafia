import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
  Grid,
  CircularProgress,
} from '@mui/material';
import { useToastStore } from '@/shared/stores/toastStore';
import {
  Update as UpdateIcon,
  Backup as BackupIcon,
  Restore as RestoreIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  listSystemUpdates,
  deploySystemUpdate,
  listBackups,
  createBackup,
  restoreBackup,
} from './api';

export function SystemUpdates() {
  const queryClient = useQueryClient();
  const [deployingId, setDeployingId] = useState<string | null>(null);
  const [restoringId, setRestoringId] = useState<string | null>(null);

  const { data: updates, isLoading: updatesLoading } = useQuery({
    queryKey: ['system-updates'],
    queryFn: listSystemUpdates,
  });

  const { data: backups, isLoading: backupsLoading } = useQuery({
    queryKey: ['system-backups'],
    queryFn: listBackups,
  });

  const deployMutation = useMutation({
    mutationFn: deploySystemUpdate,
    onMutate: (id) => setDeployingId(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-updates'] });
      setDeployingId(null);
      useToastStore.getState().addToast('Update deployed successfully.', 'success');
    },
    onError: () => setDeployingId(null),
  });

  const backupMutation = useMutation({
    mutationFn: createBackup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-backups'] });
      useToastStore.getState().addToast('Backup initiated successfully.', 'success');
    },
  });

  const restoreMutation = useMutation({
    mutationFn: restoreBackup,
    onMutate: (id) => setRestoringId(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-backups'] });
      setRestoringId(null);
      useToastStore.getState().addToast('Restore process initiated.', 'success');
    },
    onError: () => setRestoringId(null),
  });

  return (
    <Box sx={{ p: 2 }}>
      <Grid container spacing={4}>
        <Grid size={{ xs: 12, md: 6 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              System Updates
            </Typography>
            <Button variant="contained" startIcon={<UpdateIcon />} onClick={() => useToastStore.getState().addToast('System update checking requires GitHub/GitLab integration. Set CI/CD webhook URLs to enable this feature.', 'info')}>
              Check for Updates
            </Button>
          </Box>

          <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider', minHeight: 300 }}>
            {updatesLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : updates && updates.length > 0 ? (
              <List>
                {updates.map((u, i) => (
                  <ListItem key={u.id} divider={i !== updates.length - 1}>
                    <ListItemText
                      primary={
                        <strong>
                          {u.version} - {u.release_type}
                        </strong>
                      }
                      secondary={`Released: ${new Date(u.release_date).toLocaleDateString()}`}
                    />
                    <ListItemSecondaryAction>
                      <Chip
                        label={u.status}
                        color={u.status === 'deployed' ? 'success' : 'warning'}
                        size="small"
                      />
                      {u.status === 'pending' && (
                        <Button
                          size="small"
                          variant="outlined"
                          sx={{ ml: 2 }}
                          disabled={deployingId === u.id}
                          onClick={() => deployMutation.mutate(u.id)}
                        >
                          {deployingId === u.id ? 'Deploying...' : 'Install'}
                        </Button>
                      )}
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="textSecondary" sx={{ p: 4, textAlign: 'center' }}>
                No updates available.
              </Typography>
            )}
          </Paper>
        </Grid>

        <Grid size={{ xs: 12, md: 6 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              System Backups
            </Typography>
            <Button
              variant="contained"
              startIcon={<BackupIcon />}
              onClick={() => backupMutation.mutate('full')}
              disabled={backupMutation.isPending}
            >
              {backupMutation.isPending ? 'Backing up...' : 'Create Backup'}
            </Button>
          </Box>

          <Paper elevation={0} sx={{ border: '1px solid', borderColor: 'divider', minHeight: 300 }}>
            {backupsLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : backups && backups.length > 0 ? (
              <List>
                {backups.map((b, i) => (
                  <ListItem key={b.backup_id} divider={i !== backups.length - 1}>
                    <ListItemText
                      primary={<strong>{b.type.toUpperCase()} Backup</strong>}
                      secondary={`${new Date(b.timestamp).toLocaleString()} • ${b.size_mb} MB`}
                    />
                    <ListItemSecondaryAction>
                      <Chip
                        label={b.status}
                        color={b.status === 'completed' ? 'success' : 'default'}
                        size="small"
                      />
                      {b.status === 'completed' && (
                        <Button
                          size="small"
                          variant="outlined"
                          color="error"
                          startIcon={<RestoreIcon />}
                          sx={{ ml: 2 }}
                          disabled={restoringId === b.backup_id}
                          onClick={() => {
                            if (
                              window.confirm(
                                'Are you sure you want to restore from this backup? Current data will be overwritten.'
                              )
                            ) {
                              restoreMutation.mutate(b.backup_id);
                            }
                          }}
                        >
                          {restoringId === b.backup_id ? 'Restoring...' : 'Restore'}
                        </Button>
                      )}
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography color="textSecondary" sx={{ p: 4, textAlign: 'center' }}>
                No backups found.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}
