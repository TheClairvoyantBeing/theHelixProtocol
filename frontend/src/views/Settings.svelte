<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";

    let hardware = $state(null);
    let loading = $state(true);
    let theme = $state("dark"); // We'll store basic UI state locally

    onMount(async () => {
        try {
            hardware = await api.system.hardware();
        } catch (e) {
            console.error(e);
        }
        loading = false;
    });

    function toggleTheme() {
        theme = theme === "dark" ? "light" : "dark";
        document.body.className = theme === "dark" ? "bg-gray-900 text-white min-h-screen" : "bg-white text-gray-900 min-h-screen";
    }
</script>

<div class="settings-container p-4">
    <h2 class="text-xl font-bold mb-4">Settings</h2>

    <div class="mb-8">
        <h3 class="text-lg font-semibold border-b border-gray-700 pb-2 mb-4">Appearance</h3>
        <button class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded" onclick={toggleTheme}>
            Toggle Theme (Current: {theme})
        </button>
    </div>

    <div class="mb-8">
        <h3 class="text-lg font-semibold border-b border-gray-700 pb-2 mb-4">Hardware Info</h3>
        {#if loading}
            <p>Loading hardware details...</p>
        {:else if hardware}
            <pre class="bg-gray-800 p-4 rounded text-sm text-gray-300 overflow-auto">{JSON.stringify(hardware, null, 2)}</pre>
        {:else}
            <p class="text-red-400">Failed to load hardware profile.</p>
        {/if}
    </div>
</div>
