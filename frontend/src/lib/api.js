// frontend/src/lib/api.js

const BASE = 'http://localhost:7331/api/v1';

async function request(method, path, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(BASE + path, opts);
  const data = await res.json();
  if (!data.success) throw new Error(data.error?.message || 'API error');
  return data.data;
}

export const api = {
  files: {
    list: (params = {}) => request('GET', '/files?' + new URLSearchParams(params)),
    get: (id) => request('GET', `/files/${id}`),
    reindex: (ids) => request('POST', '/files/reindex', { ids }),
    stats: () => request('GET', '/files/stats'),
  },
  search: {
    query: (q, mode = 'hybrid', limit = 10) =>
      request('POST', '/search', { query: q, mode, limit }),
  },
  chat: {
    // Note: message() returns a Response for SSE streaming — handled specially
    message: (session_id, content) =>
      fetch(BASE + '/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id, content }),
      }),
    sessions: () => request('GET', '/chat/sessions'),
  },
  tasks: {
    list: (params = {}) => request('GET', '/tasks?' + new URLSearchParams(params)),
    create: (task) => request('POST', '/tasks', task),
    update: (id, data) => request('PUT', `/tasks/${id}`, data),
    complete: (id) => request('POST', `/tasks/${id}/complete`),
    overdue: () => request('GET', '/tasks/overdue'),
  },
  calendar: {
    events: (start, end) => request('GET', `/calendar/events?start=${start}&end=${end}`),
    ical: () => BASE + '/calendar/export.ical',  // direct URL for download
  },
  graph: {
    data: () => request('GET', '/graph'),
    neighbours: (id) => request('GET', `/graph/neighbours/${id}`),
  },
  system: {
    status: () => request('GET', '/status'),
    hardware: () => request('GET', '/status/hardware'),
  },
  export: {
    start: (file_ids, mode, passphrase) =>
      request('POST', '/export/start', { file_ids, mode, passphrase }),
    status: (job_id) => request('GET', `/export/status/${job_id}`),
    downloadUrl: (job_id) => BASE + `/export/download/${job_id}`,
  },
};
