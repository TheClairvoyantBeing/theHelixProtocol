<!--
Module: frontend/src/views/Files.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Files browsing and management view.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";

    // State variables using Svelte 5 runes
    let files = $state([]);
    let loading = $state(true);

    // Fetch initial files data when the component mounts
    onMount(async () => {
        try {
            files = await api.files.list();
        } catch (err) {
            console.error("Failed to load files:", err);
        } finally {
            loading = false;
        }
    });
</script>

<div class="files-container p-4">
    <h2 class="text-xl font-bold mb-4">Files & Documents</h2>
    {#if loading}
        <p>Loading files...</p>
    {:else if files.length === 0}
        <p class="text-gray-500">No files indexed yet.</p>
    {:else}
        <!-- Render the list of files -->
        <ul class="divide-y border rounded bg-white">
            {#each files as file}
                <li class="p-3 hover:bg-gray-50 cursor-pointer">
                    {file.file_name}
                    <span class="text-xs text-gray-400 ml-2">{file.category}</span>
                </li>
            {/each}
        </ul>
    {/if}
</div>
