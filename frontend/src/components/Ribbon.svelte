<script>
  import {
    IconSearch,
    IconFolder,
    IconMessage,
    IconBrain,
    IconTopologyStar3,
    IconChecklist,
    IconCalendarEvent,
    IconDownload,
    IconSettings
  } from '@tabler/icons-svelte';
  import { currentView } from '../stores/helix.js';

  const menuItems = [
    { id: 'files', icon: IconFolder, label: 'Vault Explorer' },
    { id: 'chat', icon: IconMessage, label: 'HELIX Chat' },
    { id: 'graph', icon: IconTopologyStar3, label: 'Graph View' },
    { id: 'today', icon: IconChecklist, label: 'Tasks' },
    { id: 'calendar', icon: IconCalendarEvent, label: 'Calendar' },
    { id: 'settings', icon: IconSettings, label: 'Settings' }
  ];

  function setView(id) {
    currentView.set(id);
  }
</script>

<nav class="w-[44px] h-full flex flex-col items-center py-4 bg-obsidian-100 dark:bg-obsidian-800 border-r border-gray-200 dark:border-obsidian-700 flex-shrink-0 transition-colors z-20">
  <div class="mb-4">
    <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-accentHelix to-orange-400 flex items-center justify-center shadow-lg">
      <span class="text-white font-bold text-sm leading-none">H</span>
    </div>
  </div>

  <div class="flex-1 flex flex-col items-center gap-4 mt-2">
    {#each menuItems as item}
      <button
        class={`p-2 rounded-lg transition-colors flex items-center justify-center text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-200 dark:hover:bg-obsidian-700 ${$currentView === item.id ? 'text-accentHelix dark:text-accentHelix' : ''}`}
        onclick={() => setView(item.id)}
        title={item.label}
      >
        <item.icon size={22} stroke={1.5} />
      </button>
    {/each}
  </div>
</nav>

<style>
  /* Tooltip logic if needed, simple title attribute used for now */
</style>
