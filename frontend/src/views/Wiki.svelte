<!--
Module: frontend/src/views/Wiki.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Wiki viewer for semantic memories.
-->
<script>
    // State variables representing the currently available semantic pages
    let pages = $state([
        { id: "1", title: "User Profile" },
        { id: "2", title: "Active Projects" }
    ]);
</script>

<div class="wiki-container p-4 flex">
    <!-- Sidebar navigation for Wiki pages -->
    <div class="sidebar w-1/4 border-r pr-4">
        <h2 class="text-xl font-bold mb-4">Wiki</h2>
        <ul class="space-y-2">
            {#each pages as page}
                <li class="cursor-pointer text-blue-600 hover:underline">{page.title}</li>
            {/each}
        </ul>
    </div>

    <!-- Main content area for viewing the selected Wiki page -->
    <div class="content w-3/4 pl-4">
        <p class="text-gray-500 mt-10 text-center">Select a page to view.</p>
    </div>
</div>
