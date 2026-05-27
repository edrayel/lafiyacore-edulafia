import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getLocalDb, saveRecord, getRecord, resolveConflict } from './db';
import PouchDB from 'pouchdb';

vi.mock('pouchdb', () => {
  const MockPouchDB = vi.fn().mockImplementation(function (name: string) {
    return {
      name,
      put: vi.fn().mockResolvedValue({ ok: true, id: 'mock-id', rev: '1-mock' }),
      get: vi.fn().mockImplementation((id) => {
        if (id === 'attendance-record-1') {
          return Promise.resolve({
            _id: 'mock-id',
            _rev: '1-mock',
            type: 'mock',
            data: { status: 'present' },
          });
        }
        return Promise.reject({ status: 404 });
      }),
      destroy: vi.fn().mockResolvedValue({ ok: true }),
    };
  });
  return { default: MockPouchDB };
});

describe('Offline Database (PouchDB)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('initializes a local PouchDB instance', () => {
    const db = getLocalDb('edulafia-local-test');
    expect(PouchDB).toHaveBeenCalledWith('edulafia-local-test', undefined);
    expect(db.name).toBe('edulafia-local-test');
  });

  it('saves and retrieves a record locally', async () => {
    const testRecord = {
      _id: 'attendance-record-1',
      type: 'attendance',
      status: 'pending_sync',
      data: { student_id: '123', status: 'present' },
    };

    const saved = await saveRecord('edulafia-local-test', testRecord);
    expect(saved.ok).toBe(true);

    const retrieved = await getRecord('edulafia-local-test', 'attendance-record-1');
    expect((retrieved as any)._id).toBe('mock-id');
    expect((retrieved as any).data.status).toBe('present');
  });

  it('handles conflict resolution with timestamps (latest wins)', async () => {
    const localDoc = {
      _id: 'doc1',
      _rev: '1-local',
      updated_at: '2025-01-01T10:00:00Z',
      status: 'present',
    };

    const remoteDoc = {
      _id: 'doc1',
      _rev: '1-remote',
      updated_at: '2025-01-01T10:05:00Z', // remote is newer
      status: 'absent',
    };

    const resolved = resolveConflict(localDoc, remoteDoc);
    expect(resolved.status).toBe('absent'); // Remote won
    expect(resolved._rev).toBe('1-local'); // Must keep local revision for PouchDB to accept update

    const localNewer = { ...localDoc, updated_at: '2025-01-01T10:10:00Z' };
    const resolvedLocal = resolveConflict(localNewer, remoteDoc);
    expect(resolvedLocal.status).toBe('present'); // Local won
  });
});
