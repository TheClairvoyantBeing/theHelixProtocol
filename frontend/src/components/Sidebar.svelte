<script>
  import { currentView, isSidebarOpen } from '../stores/helix.js';
  import { IconChevronLeft, IconChevronRight, IconFolder, IconMessage2, IconHash } from '@tabler/icons-svelte';

  function toggleSidebar() {
      isSidebarOpen.update(v => !v);
  }
</script>

{#if $isSidebarOpen}
<aside class="w-[280px] h-full flex flex-col bg-obsidian-50 dark:bg-obsidian-900 border-r border-gray-200 dark:border-obsidian-700 flex-shrink-0 transition-all z-10 relative">
  <div class="p-4 flex items-center justify-between border-b border-gray-200 dark:border-obsidian-700 h-14">
    <h2 class="text-sm font-semibold text-gray-800 dark:text-gray-200 uppercase tracking-wider">
      {#if $currentView === 'chat'}
          Chat Sessions
      {:else if $currentView === 'files'}
          Vault Explorer
      {:else}
          Navigator
      {/if}
    </h2>
    <button onclick={toggleSidebar} class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1">
        <IconChevronLeft size={18} />
    </button>
  </div>

  <div class="flex-1 overflow-y-auto p-2">
      <!-- Sidebar content changes based on currentView -->
      {#if $currentView === 'chat'}
          <div class="space-y-1">
              <div class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 dark:hover:bg-obsidian-800 cursor-pointer text-sm text-gray-700 dark:text-gray-300">
                  <IconMessage2 size={16} /> New Session
              </div>
              <div class="mt-4 px-2 text-xs font-semibold text-gray-500 uppercase">Recent</div>
              <div class="flex items-center gap-2 p-2 rounded bg-gray-200 dark:bg-obsidian-800 cursor-pointer text-sm text-gray-900 dark:text-gray-100">
                  <IconHash size={16} class="text-gray-400" /> System Architecture
              </div>
          </div>
      {:else if $currentView === 'files'}
          <div class="space-y-1">
              <div class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 dark:hover:bg-obsidian-800 cursor-pointer text-sm text-gray-700 dark:text-gray-300">
                  <IconFolder size={16} class="text-blue-500" /> Documents
              </div>
              <div class="flex items-center gap-2 p-2 rounded hover:bg-gray-200 dark:hover:bg-obsidian-800 cursor-pointer text-sm text-gray-700 dark:text-gray-300">
                  <IconFolder size={16} class="text-blue-500" /> Projects
              </div>
          </div>
      {:else}
          <div class="p-4 text-sm text-gray-500 dark:text-gray-400 text-center italic">
              Context for {$currentView}
          </div>
      {/if}
  </div>
</aside>
{:else}
  <!-- Collapsed state toggle button -->
  <div class="absolute left-11 top-4 z-30">
      <button onclick={toggleSidebar} class="bg-white dark:bg-obsidian-800 border border-gray-200 dark:border-obsidian-700 rounded-r-md p-1.5 text-gray-500 hover:text-gray-900 dark:hover:text-gray-200 shadow-sm">
          <IconChevronRight size={16} />
      </button>
  </div>
{/if}
