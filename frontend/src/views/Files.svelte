<!--
Module: frontend/src/views/Files.svelte
Copyright (c) 2026 HELIX. All rights reserved.
File browser view (Obsidian file-tree inspired).
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    import { IconFile, IconFolder, IconRefresh, IconSearch, IconChevronRight, IconChevronDown } from '@tabler/icons-svelte';

    let loading = $state(true);
    let files = $state([]);
    let searchQuery = $state("");
    let expandedCategories = $state({});

    onMount(async () => {
        await loadFiles();
    });

    async function loadFiles() {
        loading = true;
        try {
            files = await api.files.list();
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    }

    function toggleCategory(category) {
        expandedCategories[category] = !expandedCategories[category];
    }

    // Group files by category (stub logic, assuming simple flat categories or grouping)
    // A robust file system needs nested groups, but for now we'll do simple categories
    let groupedFiles = $derived(() => {
        const groups = {};
        const filtered = files.filter(f => f.file_name.toLowerCase().includes(searchQuery.toLowerCase()) || (f.category && f.category.toLowerCase().includes(searchQuery.toLowerCase())));

        for (const file of filtered) {
            const cat = file.category || "Uncategorized";
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(file);
        }
        return groups;
    });

</script>

<div class="h-full flex flex-col bg-white dark:bg-obsidian-900 transition-colors">
    <header class="p-4 border-b border-gray-200 dark:border-obsidian-700 flex items-center justify-between">
        <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
            <IconFolder size={24} class="text-claude-accent"/> Vault Files
        </h2>
        <div class="flex items-center gap-2">
            <div class="relative">
                <IconSearch size={16} class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                <input
                    type="text"
                    bind:value={searchQuery}
                    placeholder="Search files..."
                    class="pl-9 pr-4 py-1.5 bg-obsidian-50 dark:bg-obsidian-800 border border-gray-200 dark:border-obsidian-700 rounded-md text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:border-claude-accent transition-colors"
                />
            </div>
            <button class="p-1.5 rounded bg-gray-100 dark:bg-obsidian-800 hover:bg-gray-200 dark:hover:bg-obsidian-700 transition-colors text-gray-600 dark:text-gray-400" onclick={loadFiles} title="Refresh">
                <IconRefresh size={18} />
            </button>
        </div>
    </header>

    <div class="flex-1 overflow-y-auto p-4">
        {#if loading}
            <div class="animate-pulse space-y-4">
                {#each Array(5) as _}
                    <div class="h-6 bg-gray-200 dark:bg-obsidian-800 rounded w-1/3"></div>
                {/each}
            </div>
        {:else if files.length === 0}
            <div class="flex flex-col items-center justify-center h-full text-gray-400 dark:text-gray-500">
                <IconFiles size={48} class="mb-4 opacity-50" />
                <p>No files indexed yet in your Vault.</p>
            </div>
        {:else}
            <div class="space-y-1 w-full max-w-2xl">
                {#each Object.entries(groupedFiles()) as [category, catFiles]}
                    <div class="mb-2">
                        <button
                            class="w-full flex items-center gap-2 px-2 py-1.5 hover:bg-gray-100 dark:hover:bg-obsidian-800 rounded text-left transition-colors"
                            onclick={() => toggleCategory(category)}
                        >
                            {#if expandedCategories[category] !== false}
                                <IconChevronDown size={16} class="text-gray-500" />
                            {:else}
                                <IconChevronRight size={16} class="text-gray-500" />
                            {/if}
                            <IconFolder size={18} class="text-claude-accent" />
                            <span class="font-medium text-gray-800 dark:text-gray-200">{category}</span>
                            <span class="text-xs text-gray-400 dark:text-gray-500 ml-auto">{catFiles.length} files</span>
                        </button>

                        {#if expandedCategories[category] !== false}
                            <ul class="ml-6 border-l border-gray-200 dark:border-obsidian-700 pl-2 mt-1 space-y-1">
                                {#each catFiles as file}
                                    <li>
                                        <button class="w-full flex items-center gap-2 px-2 py-1 hover:bg-gray-100 dark:hover:bg-obsidian-800 rounded text-left transition-colors group">
                                            <IconFile size={16} class="text-gray-400 group-hover:text-claude-accent transition-colors" />
                                            <span class="text-sm text-gray-700 dark:text-gray-300 truncate">{file.file_name || 'Unnamed File'}</span>
                                        </button>
                                    </li>
                                {/each}
                            </ul>
                        {/if}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
