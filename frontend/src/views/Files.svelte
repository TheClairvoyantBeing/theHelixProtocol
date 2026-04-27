<!--
Module: frontend/src/views/Files.svelte
Copyright (c) 2026 HELIX. All rights reserved.
File browser view.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";

    let loading = $state(true);
    let files = $state([]);

    onMount(async () => {
        try {
            files = await api.files.list();
        } catch (e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });
</script>

<div class="files-container p-4 h-full flex flex-col">
    <h2 class="text-xl font-bold mb-4">Files</h2>

    {#if loading}
        <p>Loading files...</p>
    {:else}
        <div class="flex-1 border p-4 bg-gray-800 rounded shadow min-h-[500px]">
            {#if files.length === 0}
                <p class="text-gray-400 italic">No files indexed yet.</p>
            {:else}
                <ul class="list-disc pl-5">
                    {#each files as file}
                        <li>{file.file_name}</li>
                    {/each}
                </ul>
            {/if}
        </div>
    {/if}
</div>
