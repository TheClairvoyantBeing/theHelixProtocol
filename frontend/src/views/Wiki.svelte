<script>
    let pages = [];
</script>

<div class="wiki-container">
    <h2>Wiki</h2>
    <ul>
        {#each pages as page}
            <li>{page.title}</li>
        {/each}
    </ul>
</div>
