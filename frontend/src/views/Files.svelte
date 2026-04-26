<script>
    let files = [];
</script>

<div class="files-container">
    <h2>Files & Tasks</h2>
    <ul>
        {#each files as file}
            <li>{file.name}</li>
        {/each}
    </ul>
</div>
