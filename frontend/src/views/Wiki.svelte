<!--
Module: frontend/src/views/Wiki.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Wiki browsing view.
-->
<script>
    import { onMount } from "svelte";
    import { IconBook, IconFileText } from '@tabler/icons-svelte';

    let loading = $state(false);
    // Future: implement wiki api calls
    let pages = $state([]);

</script>

<div class="h-full flex flex-col bg-white dark:bg-obsidian-900 transition-colors">
    <header class="p-4 border-b border-gray-200 dark:border-obsidian-700 flex items-center justify-between">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <IconBook size={24} class="text-claude-accent"/> Knowledge Wiki
        </h2>
    </header>

    <div class="flex-1 overflow-y-auto p-8">
        {#if loading}
            <p class="text-gray-500">Loading wiki...</p>
        {:else if pages.length === 0}
            <div class="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-500 max-w-md mx-auto text-center">
                <IconFileText size={48} class="mb-4 opacity-50" />
                <h3 class="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">Your Wiki is Empty</h3>
                <p class="text-sm">As HELIX processes your files and conversations, it will automatically generate and curate Markdown knowledge pages here.</p>
            </div>
        {:else}
            <!-- Render wiki index -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {#each pages as page}
                    <div class="p-4 bg-obsidian-50 dark:bg-obsidian-800 border border-gray-200 dark:border-obsidian-700 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer">
                        <h3 class="font-medium text-gray-900 dark:text-gray-100">{page.title}</h3>
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
