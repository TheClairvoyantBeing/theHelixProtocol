<!--
Module: frontend/src/views/Today.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Today dashboard view.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    import { IconClock, IconChecklist, IconSun } from '@tabler/icons-svelte';

    let loading = $state(true);
    let tasks = $state([]);
    let overdue = $state([]);
    let dateStr = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });

    onMount(async () => {
        try {
            tasks = await api.tasks.list({ status: "todo" });
            overdue = await api.tasks.overdue();
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="h-full flex flex-col bg-white dark:bg-obsidian-900 transition-colors overflow-y-auto">
    <header class="p-8 pb-4">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-gray-100 flex items-center gap-3">
            <IconSun size={32} class="text-claude-accent" /> Good Morning
        </h2>
        <p class="text-gray-500 dark:text-gray-400 mt-2">{dateStr}</p>
    </header>

    <div class="p-8 pt-4 grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-5xl">

        <!-- Overdue Tasks -->
        <div class="bg-obsidian-50 dark:bg-obsidian-800 rounded-xl p-6 border border-red-200 dark:border-red-900/30 shadow-sm relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1 h-full bg-red-500"></div>
            <h3 class="text-lg font-semibold text-red-600 dark:text-red-400 mb-4 flex items-center gap-2">
                <IconClock size={20} /> Overdue
            </h3>

            {#if loading}
                <div class="animate-pulse space-y-3">
                    <div class="h-4 bg-gray-200 dark:bg-obsidian-700 rounded w-3/4"></div>
                    <div class="h-4 bg-gray-200 dark:bg-obsidian-700 rounded w-1/2"></div>
                </div>
            {:else if overdue.length === 0}
                <p class="text-gray-500 dark:text-gray-400 text-sm">You're all caught up on old tasks.</p>
            {:else}
                <ul class="space-y-3">
                    {#each overdue as task}
                        <li class="flex items-start gap-3 p-3 bg-white dark:bg-obsidian-900 rounded-lg border border-gray-100 dark:border-obsidian-700">
                            <input type="checkbox" class="mt-1 rounded text-claude-accent focus:ring-claude-accent bg-gray-100 border-gray-300 dark:bg-obsidian-800 dark:border-obsidian-600">
                            <div>
                                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">{task.title}</p>
                                {#if task.deadline}
                                    <p class="text-xs text-red-500 mt-1">Due: {new Date(task.deadline).toLocaleDateString()}</p>
                                {/if}
                            </div>
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>

        <!-- Today's Tasks -->
        <div class="bg-obsidian-50 dark:bg-obsidian-800 rounded-xl p-6 border border-gray-200 dark:border-obsidian-700 shadow-sm relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1 h-full bg-claude-accent"></div>
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4 flex items-center gap-2">
                <IconChecklist size={20} class="text-claude-accent" /> Up Next
            </h3>

            {#if loading}
                <div class="animate-pulse space-y-3">
                    <div class="h-4 bg-gray-200 dark:bg-obsidian-700 rounded w-full"></div>
                    <div class="h-4 bg-gray-200 dark:bg-obsidian-700 rounded w-5/6"></div>
                </div>
            {:else if tasks.length === 0}
                <p class="text-gray-500 dark:text-gray-400 text-sm">Nothing on the docket for today.</p>
            {:else}
                <ul class="space-y-3">
                    {#each tasks as task}
                        <li class="flex items-start gap-3 p-3 bg-white dark:bg-obsidian-900 rounded-lg border border-gray-100 dark:border-obsidian-700 hover:border-gray-300 dark:hover:border-obsidian-500 transition-colors">
                            <input type="checkbox" class="mt-1 rounded text-claude-accent focus:ring-claude-accent bg-gray-100 border-gray-300 dark:bg-obsidian-800 dark:border-obsidian-600">
                            <p class="text-sm font-medium text-gray-800 dark:text-gray-200">{task.title}</p>
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>

    </div>
</div>
