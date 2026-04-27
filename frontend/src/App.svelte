<!-- Copyright (c) 2026 HELIX. All rights reserved. -->
<script>
  import Chat from './views/Chat.svelte';
  import Settings from './views/Settings.svelte';
  import Calendar from './views/Calendar.svelte';
  import Today from './views/Today.svelte';
  import Wiki from './views/Wiki.svelte';
  import Graph from './views/Graph.svelte';
  import Files from './views/Files.svelte';

  let currentView = $state('chat');
</script>

<main class="h-screen w-full flex flex-col">
  <header class="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center">
    <h1 class="text-xl font-bold tracking-wider">HELIX OS</h1>
    <div class="flex gap-4 text-sm text-gray-400">
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'today'}>Today</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'chat'}>Chat</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'wiki'}>Wiki</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'graph'}>Graph</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'calendar'}>Calendar</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'files'}>Files</button>
      <button class="hover:text-white transition-colors" onclick={() => currentView = 'settings'}>Settings</button>
    </div>
  </header>

  <div class="flex-1 overflow-hidden relative">
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
  </div>
</main>
