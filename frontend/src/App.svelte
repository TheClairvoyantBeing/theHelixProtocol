<!-- Copyright (c) 2026 HELIX. All rights reserved. -->
<script>
  import { onMount } from 'svelte';
  import {
    IconMessage, IconCalendarEvent, IconLayoutDashboard,
    IconBook, IconTopologyStar3, IconFiles, IconSettings
  } from '@tabler/icons-svelte';

  import Chat from './views/Chat.svelte';
  import Settings from './views/Settings.svelte';
  import Calendar from './views/Calendar.svelte';
  import Today from './views/Today.svelte';
  import Wiki from './views/Wiki.svelte';
  import Graph from './views/Graph.svelte';
  import Files from './views/Files.svelte';

  let currentView = $state('chat');

  // Handle theme persistence
  onMount(() => {
      const isDark = localStorage.getItem('theme') === 'dark' ||
          (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      if (isDark) {
          document.documentElement.classList.add('dark');
      } else {
          document.documentElement.classList.remove('dark');
      }
  });

  const menuItems = [
    { id: 'chat', label: 'Chat', icon: IconMessage },
    { id: 'today', label: 'Today', icon: IconLayoutDashboard },
    { id: 'wiki', label: 'Wiki', icon: IconBook },
    { id: 'graph', label: 'Graph', icon: IconTopologyStar3 },
    { id: 'files', label: 'Files', icon: IconFiles },
    { id: 'calendar', label: 'Calendar', icon: IconCalendarEvent },
    { id: 'settings', label: 'Settings', icon: IconSettings },
  ];
</script>

<div class="h-screen w-full flex bg-obsidian-50 dark:bg-obsidian-900 transition-colors">

  <!-- Premium Left Sidebar -->
  <aside class="w-64 border-r border-gray-200 dark:border-obsidian-700 bg-obsidian-100 dark:bg-obsidian-800 flex flex-col transition-colors">
    <div class="p-6 flex items-center gap-3 border-b border-gray-200 dark:border-obsidian-700">
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-claude-accent to-orange-400 flex items-center justify-center shadow-lg">
        <span class="text-white font-bold text-lg leading-none">H</span>
      </div>
      <h1 class="text-xl font-bold tracking-wide text-gray-900 dark:text-gray-100">HELIX</h1>
    </div>

    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      {#each menuItems as item}
        <button
          class={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-sm font-medium
            ${currentView === item.id
              ? 'bg-white dark:bg-obsidian-600 text-claude-accent shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-obsidian-700 hover:text-gray-900 dark:hover:text-gray-200'}`}
          onclick={() => currentView = item.id}
        >
          <item.icon size={20} stroke={2} />
          {item.label}
        </button>
      {/each}
    </nav>
  </aside>

  <!-- Main Content Area -->
  <main class="flex-1 overflow-hidden relative flex flex-col bg-white dark:bg-obsidian-900 transition-colors shadow-inner">
    {#if currentView === 'chat'}
      <Chat />
    {:else if currentView === 'settings'}
      <Settings />
    {:else if currentView === 'calendar'}
      <Calendar />
    {:else if currentView === 'today'}
      <Today />
    {:else if currentView === 'wiki'}
      <Wiki />
    {:else if currentView === 'graph'}
      <Graph />
    {:else if currentView === 'files'}
      <Files />
    {/if}
  </main>
</div>
