<!-- Copyright (c) 2026 HELIX. All rights reserved. -->
<script>
  import Chat from './views/Chat.svelte';
  // Import other views as they are built...
</script>

<main class="h-screen w-full flex flex-col">
  <header class="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center">
    <h1 class="text-xl font-bold tracking-wider">HELIX OS</h1>
    <div class="flex gap-4 text-sm text-gray-400">
      <button class="hover:text-white transition-colors">Chat</button>
      <button class="hover:text-white transition-colors">Graph</button>
      <button class="hover:text-white transition-colors">Calendar</button>
      <button class="hover:text-white transition-colors">Settings</button>
    </div>
  </header>

  <div class="flex-1 overflow-hidden relative">
    <Chat />
  </div>
</main>
