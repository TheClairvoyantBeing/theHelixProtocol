<!--
Module: frontend/src/views/Today.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Today dashboard displaying active tasks and recent files.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";

    // State variables using Svelte 5 runes
    let activeTasks = $state([]);
    let recentFiles = $state([]);
    let loading = $state(true);
    let error = $state(null);

    // Fetch initial data when the component mounts
    onMount(async () => {
        try {
            // Concurrently fetch tasks and recent files
            const [tasksRes, filesRes] = await Promise.all([
                api.tasks.list({ status: "todo" }),
                api.files.list({ limit: 5 })
            ]);
            activeTasks = tasksRes;
            recentFiles = filesRes;
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    });
</script>

<div class="today-container p-4 flex flex-col gap-6">
    <h2 class="text-2xl font-bold">Today</h2>

    {#if loading}
        <p>Loading dashboard...</p>
    {:else if error}
        <p class="text-red-600">Error: {error}</p>
    {:else}
        <div class="grid grid-cols-2 gap-4">
            <!-- Active Tasks Panel -->
            <div class="tasks border p-4 rounded shadow bg-white">
                <h3 class="text-lg font-semibold mb-2">Active Tasks</h3>
                {#if activeTasks.length === 0}
                    <p class="text-gray-500">No active tasks.</p>
                {:else}
                    <ul class="list-disc pl-5">
                        {#each activeTasks as task}
                            <li>{task.title} (Due: {task.deadline || "None"})</li>
                        {/each}
                    </ul>
                {/if}
            </div>

            <!-- Recent Files Panel -->
            <div class="files border p-4 rounded shadow bg-white">
                <h3 class="text-lg font-semibold mb-2">Recent Files</h3>
                {#if recentFiles.length === 0}
                    <p class="text-gray-500">No recent files.</p>
                {:else}
                    <ul class="list-disc pl-5">
                        {#each recentFiles as file}
                            <li>{file.file_name}</li>
                        {/each}
                    </ul>
                {/if}
            </div>
        </div>
    {/if}
</div>
