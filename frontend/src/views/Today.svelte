<!--
Module: frontend/src/views/Today.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Today dashboard view.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";

    let loading = $state(true);
    let tasks = $state([]);
    let overdue = $state([]);

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

<div class="today-container p-4 h-full flex flex-col">
    <h2 class="text-xl font-bold mb-4">Today</h2>

    {#if loading}
        <p>Loading dashboard...</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="border p-4 bg-gray-800 rounded shadow">
                <h3 class="text-lg font-semibold text-red-400 mb-2">Overdue Tasks</h3>
                {#if overdue.length === 0}
                    <p class="text-gray-400 italic">No overdue tasks.</p>
                {:else}
                    <ul class="list-disc pl-5">
                        {#each overdue as task}
                            <li>{task.title}</li>
                        {/each}
                    </ul>
                {/if}
            </div>

            <div class="border p-4 bg-gray-800 rounded shadow">
                <h3 class="text-lg font-semibold mb-2">Tasks to Do</h3>
                {#if tasks.length === 0}
                    <p class="text-gray-400 italic">No pending tasks.</p>
                {:else}
                    <ul class="list-disc pl-5">
                        {#each tasks as task}
                            <li>{task.title}</li>
                        {/each}
                    </ul>
                {/if}
            </div>
        </div>
    {/if}
</div>
