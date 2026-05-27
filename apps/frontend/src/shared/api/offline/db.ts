import PouchDB from 'pouchdb';

// Cache database instances so we don't recreate them
const dbCache: Record<string, PouchDB.Database> = {};

export function getLocalDb(
  name: string,
  options?: PouchDB.Configuration.DatabaseConfiguration
): PouchDB.Database {
  if (!dbCache[name]) {
    dbCache[name] = new PouchDB(name, options);
  }
  return dbCache[name];
}

export async function clearDb(
  name: string,
  options?: PouchDB.Configuration.DatabaseConfiguration
): Promise<void> {
  if (dbCache[name]) {
    await dbCache[name].destroy();
    delete dbCache[name];
  } else {
    const db = new PouchDB(name, options);
    await db.destroy();
  }
}

export async function saveRecord(
  name: string,
  record: Record<string, unknown> & { _id?: string },
  options?: PouchDB.Configuration.DatabaseConfiguration
): Promise<PouchDB.Core.Response> {
  const db = getLocalDb(name, options);

  if (!record._id) {
    throw new Error('Record must have an _id');
  }

  try {
    // If the document already exists, we need its latest _rev
    const existing = await db.get(record._id);
    return await db.put({ ...record, _rev: existing._rev });
  } catch (error: unknown) {
    // If document doesn't exist (status 404), just put it
    if (error && typeof error === 'object' && 'status' in error && error.status === 404) {
      return await db.put(record);
    }
    throw error;
  }
}

export async function getRecord(
  name: string,
  id: string,
  options?: PouchDB.Configuration.DatabaseConfiguration
): Promise<unknown> {
  const db = getLocalDb(name, options);
  return await db.get(id);
}

export function resolveConflict(
  localDoc: Record<string, unknown> & { updated_at?: string; _rev?: string },
  remoteDoc: Record<string, unknown> & { updated_at?: string; _rev?: string }
): Record<string, unknown> {
  // Simple timestamp-based resolution (latest wins)
  const localTime = new Date(localDoc.updated_at || 0).getTime();
  const remoteTime = new Date(remoteDoc.updated_at || 0).getTime();

  if (remoteTime > localTime) {
    return { ...remoteDoc, _rev: localDoc._rev || remoteDoc._rev };
  }

  return { ...localDoc, _rev: localDoc._rev || remoteDoc._rev };
}
