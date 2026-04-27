<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    import { IconMoon, IconSun } from '@tabler/icons-svelte';

    let hardware = $state(null);
    let loading = $state(true);
    let isDark = $state(true);

    onMount(async () => {
        // Init theme state
        isDark = document.documentElement.classList.contains('dark');

        try {
            hardware = await api.system.hardware();
        } catch (e) {
            console.error(e);
        }
        loading = false;
    });

    function toggleTheme() {
        isDark = !isDark;
        if (isDark) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }
</script>

<div class="h-full overflow-y-auto p-8 max-w-4xl mx-auto w-full">
    <h2 class="text-3xl font-bold mb-8 text-gray-900 dark:text-gray-100">Settings</h2>

    <div class="bg-obsidian-100 dark:bg-obsidian-800 rounded-xl p-6 mb-8 border border-gray-200 dark:border-obsidian-700 shadow-sm">
        <h3 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200 flex items-center gap-2">
            Appearance
        </h3>
        <div class="flex items-center justify-between p-4 bg-white dark:bg-obsidian-900 rounded-lg border border-gray-200 dark:border-obsidian-700">
            <div>
                <p class="font-medium text-gray-900 dark:text-gray-100">Theme Preference</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">Switch between light and dark mode</p>
            </div>
            <button
                class="flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors bg-gray-100 dark:bg-obsidian-700 hover:bg-gray-200 dark:hover:bg-obsidian-600 text-gray-800 dark:text-gray-200"
                onclick={toggleTheme}
            >
                {#if isDark}
                    <IconSun size={18} /> Light Mode
                {:else}
                    <IconMoon size={18} /> Dark Mode
                {/if}
            </button>
        </div>
    </div>

    <div class="bg-obsidian-100 dark:bg-obsidian-800 rounded-xl p-6 mb-8 border border-gray-200 dark:border-obsidian-700 shadow-sm">
        <h3 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Hardware Profile</h3>
        {#if loading}
            <div class="animate-pulse flex space-x-4">
              <div class="flex-1 space-y-4 py-1">
                <div class="h-4 bg-gray-300 dark:bg-obsidian-600 rounded w-3/4"></div>
                <div class="h-4 bg-gray-300 dark:bg-obsidian-600 rounded"></div>
              </div>
            </div>
        {:else if hardware && hardware.data}
            <div class="bg-white dark:bg-obsidian-900 p-4 rounded-lg border border-gray-200 dark:border-obsidian-700 overflow-auto">
                <pre class="text-sm text-gray-700 dark:text-gray-300 font-mono">{JSON.stringify(hardware.data, null, 2)}</pre>
            </div>
        {:else}
            <p class="text-gray-500 dark:text-gray-400 italic">No hardware information available in stub.</p>
        {/if}
    </div>
</div>
