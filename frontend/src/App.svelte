<!-- Copyright (c) 2026 HELIX. All rights reserved. -->
<script>
  import { onMount } from 'svelte';

  import { currentView } from './stores/helix.js';

  import Ribbon from './components/Ribbon.svelte';
  import Sidebar from './components/Sidebar.svelte';

  import Chat from './views/Chat.svelte';
  import Settings from './views/Settings.svelte';
  import Calendar from './views/Calendar.svelte';
  import Today from './views/Today.svelte';
  import Wiki from './views/Wiki.svelte';
  import Graph from './views/Graph.svelte';
  import Files from './views/Files.svelte';

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

</script>

<div class="h-screen w-full flex bg-obsidian-50 dark:bg-obsidian-900 transition-colors overflow-hidden">

  <!-- Left Ribbon (icon rail - 44px wide) -->
  <Ribbon />

  <!-- Left Sidebar (collapsible 280px) -->
  <Sidebar />

  <!-- Main Content Area -->
  <main class="flex-1 overflow-hidden relative flex flex-col bg-white dark:bg-obsidian-900 transition-colors shadow-inner z-0">
    {#if $currentView === 'chat'}
      <Chat />
    {:else if $currentView === 'settings'}
      <Settings />
    {:else if $currentView === 'calendar'}
      <Calendar />
    {:else if $currentView === 'today'}
      <Today />
    {:else if $currentView === 'wiki'}
      <Wiki />
    {:else if $currentView === 'graph'}
      <Graph />
    {:else if $currentView === 'files'}
      <Files />
    {:else}
      <!-- Fallback or mock views for 'search', 'memory', 'ingest' -->
      <div class="h-full flex items-center justify-center text-gray-500">
         View: {$currentView} (Not yet fully implemented)
      </div>
    {/if}
  </main>
</div>
