<!--
Module: frontend/src/views/Settings.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Settings dashboard for OS configuration.
-->
<script>
    // Component state using Svelte 5 runes
    let vaultPath = $state("~/Documents");
    let aiModel = $state("llama3:8b");

    /**
     * Handles saving settings.
     * Prevents default form submission and alerts the user.
     */
    function saveSettings(e) {
        e.preventDefault();
        alert("Settings saved locally.");
    }
</script>

<div class="settings-container p-4 max-w-lg">
    <h2 class="text-xl font-bold mb-4">Settings</h2>

    <!-- Settings form -->
    <form onsubmit={saveSettings} class="space-y-4 border p-6 rounded bg-white">
        <!-- Vault Directory Configuration -->
        <div>
            <label class="block font-semibold mb-1" for="vaultPath">Vault Directory</label>
            <input id="vaultPath" type="text" bind:value={vaultPath} class="w-full border p-2 rounded" />
        </div>

        <!-- AI Model Configuration -->
        <div>
            <label class="block font-semibold mb-1" for="aiModel">Preferred Model</label>
            <select id="aiModel" bind:value={aiModel} class="w-full border p-2 rounded">
                <option value="llama3:70b">Llama 3 70B (High Tier)</option>
                <option value="llama3:8b">Llama 3 8B (Mid Tier)</option>
                <option value="gemma:2b">Gemma 2B (Low Tier / CPU)</option>
            </select>
        </div>

        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Save</button>
    </form>
</div>
