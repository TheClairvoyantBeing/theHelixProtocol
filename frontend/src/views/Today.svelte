<script>
    let activeTasks = [];
    let recentFiles = [];
</script>

<div class="today-container">
    <h2>Today</h2>
    <div class="tasks">
        <h3>Tasks</h3>
        {#if activeTasks.length === 0}
            <p>No active tasks.</p>
        {/if}
    </div>
    <div class="files">
        <h3>Recent Files</h3>
        {#if recentFiles.length === 0}
            <p>No recent files.</p>
        {/if}
    </div>
</div>
