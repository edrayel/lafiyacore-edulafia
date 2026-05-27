import { describe, it, expect, vi, beforeEach } from 'vitest';
import { syncData, getSyncStatus } from './sync';
import { getLocalDb } from './db';

vi.mock('./db', () => ({
  getLocalDb: vi.fn().mockReturnValue({
    sync: vi.fn().mockReturnValue({
      on: vi.fn().mockReturnThis(),
      cancel: vi.fn(),
    }),
  }),
}));

describe('Offline Sync Manager', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('starts replication to remote CouchDB and updates sync status', () => {
    const remoteUrl = 'http://localhost:5984/edulafia-remote';
    const syncHandler = syncData('edulafia-local', remoteUrl);

    expect(getLocalDb).toHaveBeenCalledWith('edulafia-local');
    expect(syncHandler).toBeDefined();

    const status = getSyncStatus();
    expect(status).toBe('active');
  });
});
