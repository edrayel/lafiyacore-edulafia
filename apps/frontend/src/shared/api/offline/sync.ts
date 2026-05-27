import { getLocalDb } from './db';
import PouchDB from 'pouchdb';

export type SyncStatusType = 'idle' | 'active' | 'error' | 'paused';
let syncStatus: SyncStatusType = 'idle';
let currentSync: PouchDB.Replication.Sync<Record<string, unknown>> | null = null;

type Listener = (status: SyncStatusType) => void;
const listeners: Set<Listener> = new Set();

function updateStatus(newStatus: SyncStatusType) {
  syncStatus = newStatus;
  listeners.forEach((listener) => listener(syncStatus));
}

export function subscribeToSyncStatus(listener: Listener) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

export function getSyncStatus() {
  return syncStatus;
}

export function syncData(localName: string, remoteUrl: string, options?: Record<string, unknown>) {
  const localDb = getLocalDb(localName);
  const remoteDb = new PouchDB(remoteUrl);

  updateStatus('active');

  currentSync = localDb
    .sync(remoteDb, {
      live: true,
      retry: true,
      ...options,
    })
    .on('change', () => {
      // handle change (info omitted)
    })
    .on('paused', () => {
      // replication paused (e.g. user went offline)
      updateStatus('paused');
    })
    .on('active', () => {
      // replicate resumed (e.g. new changes replicating, user went back online)
      updateStatus('active');
    })
    .on('denied', (err) => {
      // a document failed to replicate (e.g. due to permissions)
      console.warn('Sync denied:', err);
    })
    .on('complete', () => {
      // handle complete (info omitted)
      updateStatus('idle');
    })
    .on('error', (err) => {
      updateStatus('error');
      console.warn('Sync error:', err);
    });

  return currentSync;
}

export function cancelSync() {
  if (currentSync) {
    currentSync.cancel();
    currentSync = null;
    updateStatus('idle');
  }
}
