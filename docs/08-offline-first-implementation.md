# EduLafia Offline-First Implementation Guide

## Document Information

- **Version**: 1.0.0
- **Last Updated**: 2026-03-26
- **Status**: Draft
- **Purpose**: Specify the offline-first architecture enabling EduLafia to function reliably in low-connectivity Nigerian school environments

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Principles](#2-architecture-principles)
3. [IndexedDB Schema Design](#3-indexeddb-schema-design)
4. [PouchDB/CouchDB Sync Protocol](#4-pouchdbcouchdb-sync-protocol)
5. [Conflict Resolution Strategies](#5-conflict-resolution-strategies)
6. [Offline Queue Management](#6-offline-queue-management)
7. [Sync Status Monitoring](#7-sync-status-monitoring)
8. [Data Storage Limits and Management](#8-data-storage-limits-and-management)
9. [Network State Management](#9-network-state-management)
10. [Caching Strategies](#10-caching-strategies)
11. [Graceful Degradation](#11-graceful-degradation)
12. [Implementation Checklists](#12-implementation-checklists)

---

## 1. Overview

### 1.1 Problem Context

Many Nigerian secondary schools operate in areas with unreliable internet connectivity. Teachers, school nurses, and administrators must continue performing daily operations (marking attendance, recording grades, logging health visits) even when offline. EduLafia must store data locally on the device and synchronize with the central server when connectivity is restored, without data loss.

### 1.2 Offline-First Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| Full offline functionality | P0 | All core operations must work without internet |
| Automatic sync | P0 | Data must sync automatically when connectivity returns |
| Conflict resolution | P0 | Concurrent edits must be resolved without data loss |
| Data integrity | P0 | Local data must remain consistent and valid |
| Storage management | P1 | Local storage must not exceed device limits |
| Sync feedback | P1 | Users must see sync status for their data |
| Bandwidth efficiency | P2 | Sync must minimize data transfer |

### 1.3 Technology Stack

- **Client-Side Storage**: IndexedDB (via PouchDB abstraction)
- **Sync Protocol**: PouchDB-to-CouchDB replication
- **Server-Side**: CouchDB or PouchDB-compatible endpoint (via `pouchdb-adapter-http`)
- **State Management**: React Query + Zustand for sync-aware state
- **Service Worker**: Workbox for asset caching and background sync

---

## 2. Architecture Principles

### 2.1 Data Flow Model

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT DEVICE                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  Application │───>│  Local State │───>│   IndexedDB      │  │
│  │   (React)    │    │ (React Query)│    │ (PouchDB)        │  │
│  └──────────────┘    └──────────────┘    └────────┬─────────┘  │
│                                                   │             │
│                              ┌────────────────────┘             │
│                              ▼                                  │
│                       ┌──────────────┐                          │
│                       │ Sync Service │                          │
│                       │  (Background)│                          │
│                       └──────┬───────┘                          │
└──────────────────────────────┼──────────────────────────────────┘
                               │ Network
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                         SERVER                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  CouchDB /   │───>│  Conflict    │───>│  PostgreSQL      │   │
│  │  Sync Gateway│    │  Resolver    │    │  (Canonical DB)  │   │
│  └──────────────┘    └──────────────┘    └──────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Design Principles

1. **Local First**: All reads and writes go to IndexedDB first, then sync to server
2. **Eventual Consistency**: Data is eventually consistent across devices, not immediately consistent
3. **Optimistic UI**: UI updates immediately on local write, without waiting for server confirmation
4. **Conflict Tolerance**: System accepts that conflicts will occur and provides resolution strategies
5. **Bandwidth Awareness**: Sync is throttled and batched to work on low-bandwidth connections

---

## 3. IndexedDB Schema Design

### 3.1 Database Configuration

```
Database Name: edulafia_<school_id>
Version: 1
```

Each school gets its own IndexedDB database to isolate data by school context.

### 3.2 Object Stores

#### 3.2.1 Students Store

```
Store Name: students
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| admission_number | String | Yes (unique) | - |
| first_name | String | No | - |
| last_name | String | No | - |
| date_of_birth | Date | No | - |
| gender | String | Yes | - |
| class_id | String (UUID) | Yes | - |
| parent_id | String (UUID) | Yes | - |
| medical_flags | JSON | No | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.2 Attendance Store

```
Store Name: attendance_records
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| student_id | String (UUID) | Yes | - |
| class_id | String (UUID) | Yes | - |
| date | Date | Yes | - |
| period | String | Yes | - |
| status | String | Yes | - |
| notes | String | No | - |
| marked_by | String (UUID) | Yes | - |
| marked_at | DateTime | No | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.3 Grades Store

```
Store Name: grades
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| student_id | String (UUID) | Yes | - |
| subject_id | String (UUID) | Yes | - |
| term_id | String (UUID) | Yes | - |
| ca_score | Number | No | - |
| exam_score | Number | No | - |
| total_score | Number | No | - |
| letter_grade | String | No | - |
| remark | String | No | - |
| graded_by | String (UUID) | Yes | - |
| graded_at | DateTime | No | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.4 Health Visits Store

```
Store Name: health_visits
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| student_id | String (UUID) | Yes | - |
| visit_date | DateTime | Yes | - |
| symptoms | JSON | No | - |
| diagnosis | String | No | - |
| treatment | String | No | - |
| severity | String | Yes | - |
| sentinel_flagged | Boolean | Yes | - |
| sentinel_cluster_id | String | No | - |
| provider_id | String (UUID) | Yes | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.5 Fees & Payments Store

```
Store Name: fee_payments
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| student_id | String (UUID) | Yes | - |
| fee_structure_id | String (UUID) | Yes | - |
| amount | Number | No | - |
| payment_date | Date | Yes | - |
| payment_method | String | Yes | - |
| reference | String | No | - |
| status | String | Yes | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.6 Teachers Store

```
Store Name: teachers
Key Path: id (UUID)
```

| Field | Type | Indexed | Sync Status |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| school_id | String (UUID) | Yes | - |
| employee_id | String | Yes | - |
| first_name | String | No | - |
| last_name | String | No | - |
| email | String | Yes | - |
| phone | String | No | - |
| status | String | Yes | - |
| subjects | JSON | No | - |
| classes | JSON | No | - |
| created_at | DateTime | Yes | - |
| updated_at | DateTime | Yes | - |
| _sync_status | String | Yes | synced/pending/conflict/error |
| _last_synced_at | DateTime | No | - |
| _rev | String | No | PouchDB revision |

#### 3.2.7 Sync Queue Store

```
Store Name: sync_queue
Key Path: id (UUID)
```

| Field | Type | Indexed | Description |
|-------|------|---------|-------------|
| id | String (UUID) | Yes (PK) | - |
| store_name | String | Yes | Target object store |
| record_id | String | Yes | ID of the record |
| operation | String | Yes | create/update/delete |
| payload | JSON | No | Full record or delta |
| priority | Number | Yes | Higher = synced first |
| retry_count | Number | Yes | Number of retry attempts |
| max_retries | Number | No | Maximum retry limit |
| error_message | String | No | Last error if failed |
| created_at | DateTime | Yes | - |
| last_attempt_at | DateTime | No | - |
| status | String | Yes | pending/syncing/failed/completed |

#### 3.2.8 Sync Metadata Store

```
Store Name: sync_metadata
Key Path: key
```

| Field | Type | Description |
|-------|------|-------------|
| key | String (PK) | Metadata key |
| value | JSON | Metadata value |
| updated_at | DateTime | Last update time |

Metadata keys include:
- `last_successful_sync` - Timestamp of last successful sync
- `last_checkpoint` - CouchDB sequence number for continuous replication
- `device_id` - Unique device identifier
- `user_id` - Currently authenticated user
- `school_id` - Current school context
- `sync_enabled` - Boolean flag for sync status

### 3.3 Indexes

Create compound indexes for common query patterns:

```
// Attendance queries
attendance_records: ["school_id", "class_id", "date"]
attendance_records: ["student_id", "date"]
attendance_records: ["_sync_status", "created_at"]

// Grade queries
grades: ["student_id", "term_id", "subject_id"]
grades: ["school_id", "term_id", "subject_id"]
grades: ["_sync_status", "created_at"]

// Sync queue queries
sync_queue: ["status", "priority", "created_at"]
sync_queue: ["store_name", "status"]

// Health visit queries
health_visits: ["student_id", "visit_date"]
health_visits: ["school_id", "sentinel_flagged", "visit_date"]
```

---

## 4. PouchDB/CouchDB Sync Protocol

### 4.1 PouchDB Configuration

```javascript
// PouchDB instance configuration
const dbConfig = {
  auto_compaction: true,       // Compact database automatically
  adapter: 'indexeddb',        // Use IndexedDB adapter
  revs_limit: 100,             // Keep 100 revision history
  deterministic_revs: true,    // Deterministic revision IDs
  ddoc_validation: false,      // Skip design doc validation
};
```

### 4.2 Sync Modes

#### 4.2.1 One-Time Sync (Pull)

Used during initial app load or user login to pull latest data from server.

```
Trigger: App initialization, user login, manual refresh
Direction: Server → Client
Scope: All data for the current user/school
Behavior: Pull all changes since last checkpoint
```

#### 4.2.2 Continuous Replication (Push)

Used to continuously push local changes to the server.

```
Trigger: Any local write operation
Direction: Client → Server
Scope: Only pending records in sync queue
Behavior: Batch updates every 30 seconds when online
```

#### 4.2.3 Two-Way Replication

Used for real-time sync when connectivity is good.

```
Trigger: Online state with good connectivity
Direction: Bidirectional
Scope: Full sync
Behavior: Live replication with change feed
```

### 4.3 Sync Configuration

```javascript
const syncConfig = {
  // Timing
  retryInterval: 5000,           // 5 seconds between retries
  heartbeatInterval: 30000,      // 30 seconds heartbeat
  backOffDelay: 1000,            // Initial backoff delay
  maxBackOffDelay: 60000,        // Maximum backoff delay (1 minute)
  
  // Batching
  batchSize: 50,                 // Sync 50 documents at a time
  batchInterval: 30000,          // Batch every 30 seconds
  
  // Network
  timeout: 30000,                // 30 second timeout per request
  ajaxPoolSize: 5,               // Max 5 concurrent requests
  
  // Filters
  filter: 'sync/by_school',     // Only sync school data
  query_params: {
    school_id: currentSchoolId,
    user_id: currentUserId,
  },
};
```

### 4.4 Server-Side CouchDB Configuration

```
couchdb.ini:
  [couchdb]
  max_document_size = 67108864  ; 64MB max document
  
  [chttpd]
  max_http_request_size = 67108864
  require_valid_user = true
  
  [replicator]
  max_jobs = 20
  worker_processes = 4
  worker_batch_size = 500
  
  [couch_httpd_auth]
  require_valid_user = true
  timeout = 3600
  allow_persistent_cookies = true
```

### 4.5 Replication Filter Functions

```javascript
// Server-side filter: Only replicate school-relevant documents
function(doc, req) {
  if (doc._deleted) return true;
  if (doc.school_id && doc.school_id === req.query.school_id) {
    return true;
  }
  return false;
}
```

---

## 5. Conflict Resolution Strategies

### 5.1 Conflict Types

| Conflict Type | Description | Resolution Strategy |
|---------------|-------------|---------------------|
| Edit-Edit | Same field modified on two devices | Field-level merge or latest-wins |
| Edit-Delete | Record modified on one device, deleted on another | Recover (do not allow delete) |
| Concurrent Create | Same record created on two devices | Merge into single record |
| Cascading | Conflict in one record affects related records | Transactional rollback |

### 5.2 Resolution Hierarchy

```
1. Automatic Field-Level Merge
   ↓ (if merge fails)
2. Last-Write-Wins by Updated Timestamp
   ↓ (if timestamps equal)
3. Conflict Record Created for Manual Resolution
```

### 5.3 Field-Level Merge Strategy

For each document, identify mergeable fields and non-mergeable fields:

**Mergeable Fields** (can be merged automatically):
- `notes`, `remark`, `medical_flags` (JSON fields)
- `subjects`, `classes`, `symptoms` (array fields)

**Non-Mergeable Fields** (require last-write-wins):
- `status`, `severity`, `amount` (state fields)
- `score`, `grade`, `payment_date` (critical data)

**Merge Algorithm:**

```
function resolveConflict(localDoc, remoteDoc) {
  const merged = { ...remoteDoc };  // Start with remote as base
  
  for (const field of mergeableFields) {
    if (localDoc[field] !== remoteDoc[field]) {
      // Merge JSON/array fields
      merged[field] = deepMerge(localDoc[field], remoteDoc[field]);
    }
  }
  
  for (const field of nonMergeableFields) {
    if (localDoc[field] !== remoteDoc[field]) {
      // Use latest timestamp
      if (localDoc.updated_at > remoteDoc.updated_at) {
        merged[field] = localDoc[field];
      }
    }
  }
  
  merged._rev = generateNewRev();
  merged.updated_at = new Date();
  merged._conflict_resolution = 'auto_merged';
  
  return merged;
}
```

### 5.4 Conflict Record Storage

When automatic resolution fails, create a conflict record:

```
Conflict Record Schema:
{
  id: UUID,
  document_id: UUID,
  store_name: String,
  local_version: JSON,
  remote_version: JSON,
  conflict_type: String,
  detected_at: DateTime,
  resolved: Boolean,
  resolution: String (manual/auto_merged/server_wins/client_wins),
  resolved_by: String (UUID of user),
  resolved_at: DateTime,
  resolution_notes: String,
}
```

### 5.5 Manual Conflict Resolution UI

The conflict resolution interface presents both versions side by side and allows the user to:

1. **View differences** - Highlight changed fields between versions
2. **Choose version** - Select local or remote version
3. **Merge manually** - Pick and choose fields from both versions
4. **Add notes** - Document the resolution decision

---

## 6. Offline Queue Management

### 6.1 Queue Structure

```
┌─────────────────────────────────────────────────┐
│                 SYNC QUEUE                       │
├──────┬──────────┬──────────┬────────┬───────────┤
│ P0   │ P1       │ P2       │ P3     │ P4        │
│Health│Attendance│ Grades   │ Fees   │ Reports   │
│Visits│ Marking  │ Entry    │ Payment│ Generation│
└──────┴──────────┴──────────┴────────┴───────────┘
```

### 6.2 Priority Levels

| Priority | Level | Description | Max Retries | Retry Interval |
|----------|-------|-------------|-------------|----------------|
| 0 | Critical | Health sentinel alerts | 10 | 5 seconds |
| 1 | High | Attendance records | 5 | 15 seconds |
| 2 | Normal | Grade entries | 5 | 30 seconds |
| 3 | Low | Fee payments, reports | 3 | 60 seconds |
| 4 | Background | Bulk imports, analytics | 2 | 5 minutes |

### 6.3 Queue Operations

```javascript
// Add to queue
function enqueue(storeName, recordId, operation, payload, priority = 2) {
  const queueItem = {
    id: generateUUID(),
    store_name: storeName,
    record_id: recordId,
    operation: operation,
    payload: payload,
    priority: priority,
    retry_count: 0,
    max_retries: getRetryLimit(priority),
    created_at: new Date(),
    status: 'pending',
  };
  return db.sync_queue.put(queueItem);
}

// Process queue
async function processQueue() {
  const items = await db.sync_queue
    .where('status').equals('pending')
    .and(item => item.retry_count < item.max_retries)
    .sortBy('priority')
    .limit(batchSize);
  
  for (const item of items) {
    try {
      await processQueueItem(item);
      item.status = 'completed';
    } catch (error) {
      item.retry_count++;
      item.error_message = error.message;
      item.last_attempt_at = new Date();
      
      if (item.retry_count >= item.max_retries) {
        item.status = 'failed';
      }
    }
    await db.sync_queue.put(item);
  }
}
```

### 6.4 Queue Cleanup

```javascript
// Clean up completed items older than 7 days
async function cleanupQueue() {
  const cutoff = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
  await db.sync_queue
    .where('status').equals('completed')
    .and(item => item.created_at < cutoff)
    .delete();
}
```

---

## 7. Sync Status Monitoring

### 7.1 Sync State Machine

```
                    ┌─────────────┐
                    │  CONNECTED  │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │   IDLE      │ │  SYNCING    │ │   ERROR     │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │              │              │
            │              ▼              ▼
            │       ┌─────────────┐ ┌─────────────┐
            └──────>│  COMPLETE   │ │  RETRYING   │
                    └─────────────┘ └─────────────┘
```

### 7.2 Sync Status Indicators

| Status | Icon | Color | Description |
|--------|------|-------|-------------|
| Online & Synced | ✅ | Green | All data synced |
| Online & Syncing | 🔄 | Blue | Sync in progress |
| Online & Pending | ⏳ | Yellow | Changes waiting to sync |
| Offline & Pending | 📴 | Orange | Offline with pending changes |
| Conflict | ⚠️ | Red | Conflicts need resolution |
| Error | ❌ | Red | Sync failed, retrying |

### 7.3 Sync Dashboard Data

```javascript
syncDashboard = {
  network_status: 'online' | 'offline' | 'slow',
  last_sync_at: DateTime,
  next_sync_at: DateTime,
  
  pending_uploads: {
    total: Number,
    by_priority: {
      critical: Number,
      high: Number,
      normal: Number,
      low: Number,
    },
    by_store: {
      students: Number,
      attendance: Number,
      grades: Number,
      health_visits: Number,
      fee_payments: Number,
    },
  },
  
  recent_syncs: [{
    started_at: DateTime,
    completed_at: DateTime,
    records_uploaded: Number,
    records_downloaded: Number,
    conflicts_resolved: Number,
    errors: Number,
  }],
  
  storage_usage: {
    used_bytes: Number,
    available_bytes: Number,
    percentage_used: Number,
  },
  
  conflicts: [{
    document_id: String,
    store_name: String,
    detected_at: DateTime,
  }],
};
```

---

## 8. Data Storage Limits and Management

### 8.1 Browser Storage Limits

| Browser | Storage Limit | Notes |
|---------|---------------|-------|
| Chrome (Desktop) | ~80% of disk | Automatically managed |
| Chrome (Android) | ~80% of disk | May prompt user |
| Safari (iOS) | ~1GB | May evict without warning |
| Firefox | ~50% of disk | Automatic management |
| Samsung Internet | ~80% of disk | Similar to Chrome |

### 8.2 Storage Monitoring

```javascript
// Check available storage
async function checkStorage() {
  if (navigator.storage && navigator.storage.estimate) {
    const estimate = await navigator.storage.estimate();
    return {
      usage: estimate.usage,
      quota: estimate.quota,
      percentage: (estimate.usage / estimate.quota) * 100,
    };
  }
}

// Request persistent storage
async function requestPersistentStorage() {
  if (navigator.storage && navigator.storage.persist) {
    const persisted = await navigator.storage.persist();
    return persisted;
  }
}
```

### 8.3 Storage Cleanup Strategies

| Strategy | Trigger | Action |
|----------|---------|--------|
| Auto-compaction | DB size > 50MB | Compact PouchDB |
| Old data archival | Records > 2 years old | Archive to server, delete locally |
| Cache eviction | Storage > 80% full | Remove cached reference data |
| Manual cleanup | User action | Clear specific data sets |

---

## 9. Network State Management

### 9.1 Network Detection

```javascript
// Network state monitoring
const networkMonitor = {
  isOnline: navigator.onLine,
  connectionType: navigator.connection?.effectiveType,
  downlinkSpeed: navigator.connection?.downlink,
  rtt: navigator.connection?.rtt,
  saveData: navigator.connection?.saveData,
};
```

### 9.2 Connection Quality Tiers

| Tier | Criteria | Sync Behavior |
|------|----------|---------------|
| Excellent | RTT < 100ms, downlink > 5Mbps | Full two-way replication |
| Good | RTT < 300ms, downlink > 1Mbps | Batched two-way replication |
| Fair | RTT < 1000ms, downlink > 256Kbps | Push only, small batches |
| Poor | RTT > 1000ms, downlink < 256Kbps | Critical only (priority 0) |
| Offline | No connection | Queue all changes locally |

### 9.3 Offline Event Handling

```
Events to handle:
- navigator.onLine changes to false
- Sync request timeout
- Network error from fetch API
- WebSocket disconnection

Actions on offline:
1. Pause continuous replication
2. Start local queue processing
3. Update UI to show offline indicator
4. Enable offline-specific shortcuts
5. Reduce background processing
```

---

## 10. Caching Strategies

### 10.1 Service Worker Caching

```javascript
// Workbox configuration
workbox.routing.registerRoute(
  ({request}) => request.destination === 'document',
  new workbox.strategies.NetworkFirst({
    cacheName: 'pages-cache',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({request}) => request.destination === 'script' || request.destination === 'style',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'static-assets-cache',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({request}) => request.destination === 'image',
  new workbox.strategies.CacheFirst({
    cacheName: 'images-cache',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 200,
        maxAgeSeconds: 90 * 24 * 60 * 60, // 90 days
      }),
    ],
  })
);
```

### 10.2 Reference Data Caching

Cache frequently accessed reference data locally:

| Data Type | Cache Duration | Sync Frequency |
|-----------|---------------|----------------|
| School settings | 7 days | Daily |
| Class lists | 7 days | Daily |
| Subject lists | 7 days | Daily |
| Fee structures | 30 days | Weekly |
| Grading scales | 30 days | Weekly |
| Health protocols | 7 days | Daily |

---

## 11. Graceful Degradation

### 11.1 Feature Availability Matrix

| Feature | Online | Offline | Degraded |
|---------|--------|---------|----------|
| Mark attendance | ✅ Full | ✅ Full | ✅ Full |
| Record grades | ✅ Full | ✅ Full | ✅ Full |
| Log health visit | ✅ Full | ✅ Full | ✅ Full |
| Process payment | ✅ Full | ❌ N/A | ⚠️ Queue only |
| Generate report | ✅ Full | ⚠️ Cached | ❌ N/A |
| View analytics | ✅ Full | ⚠️ Cached | ❌ N/A |
| WhatsApp notifications | ✅ Full | ❌ N/A | ❌ N/A |
| User authentication | ✅ Full | ⚠️ Cached | ❌ N/A |

### 11.2 Offline Mode UI Adjustments

```
When offline:
- Show persistent offline banner at top
- Disable real-time collaboration features
- Show cached data with "last updated" timestamp
- Queue payment transactions instead of processing
- Use local notifications instead of push notifications
- Simplify forms to reduce data entry
```

---

## 12. Implementation Checklists

### 12.1 IndexedDB Setup Checklist

- [ ] Create PouchDB instance with IndexedDB adapter
- [ ] Define all object stores with proper indexes
- [ ] Implement store initialization on app start
- [ ] Set up compound indexes for query optimization
- [ ] Implement database versioning and migration
- [ ] Add storage monitoring and cleanup routines
- [ ] Test storage limits across browsers
- [ ] Implement data encryption at rest

### 12.2 Sync Protocol Checklist

- [ ] Implement one-time pull sync on login
- [ ] Implement continuous push replication
- [ ] Configure two-way replication for online mode
- [ ] Set up server-side CouchDB/Sync Gateway
- [ ] Implement replication filter functions
- [ ] Configure batch sizes and timing
- [ ] Add retry logic with exponential backoff
- [ ] Test sync with various network conditions

### 12.3 Conflict Resolution Checklist

- [ ] Implement field-level merge algorithm
- [ ] Create conflict detection logic
- [ ] Build conflict record storage
- [ ] Design conflict resolution UI
- [ ] Implement last-write-wins fallback
- [ ] Add conflict resolution audit logging
- [ ] Test with concurrent edit scenarios
- [ ] Document conflict resolution policies

### 12.4 Offline Queue Checklist

- [ ] Implement queue data structure
- [ ] Add priority-based queue processing
- [ ] Implement queue persistence
- [ ] Add retry logic per priority level
- [ ] Build queue monitoring dashboard
- [ ] Implement queue cleanup routines
- [ ] Test queue behavior during extended offline
- [ ] Add queue size limits and warnings

### 12.5 Network Management Checklist

- [ ] Implement network state detection
- [ ] Add connection quality assessment
- [ ] Implement adaptive sync based on quality
- [ ] Add offline event handlers
- [ ] Implement bandwidth-aware batching
- [ ] Test on various Nigerian network conditions
- [ ] Add slow connection detection and warnings
- [ ] Implement data saver mode

### 12.6 Caching and Storage Checklist

- [ ] Configure Service Worker with Workbox
- [ ] Implement page caching strategy
- [ ] Cache static assets appropriately
- [ ] Implement reference data caching
- [ ] Add cache invalidation logic
- [ ] Test storage eviction behavior
- [ ] Implement persistent storage requests
- [ ] Add storage usage monitoring UI

---

**End of Offline-First Implementation Guide**
