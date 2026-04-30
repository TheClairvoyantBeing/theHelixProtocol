import { writable } from 'svelte/store';

export const systemStatus = writable(null);       // from GET /status
export const ingestionProgress = writable(null);  // from WebSocket
export const activeSession = writable(null);      // current chat session ID
export const notifications = writable([]);        // system alerts
export const graphData = writable({ nodes: [], edges: [] });
export const currentView = writable('chat');
export const isSidebarOpen = writable(true);
