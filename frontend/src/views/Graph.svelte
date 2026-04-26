<script>
    import { onMount } from "svelte";

    let container;

    onMount(() => {
        // TODO: Initialize D3 graph here
    });
</script>

<div class="graph-container">
    <h2>Knowledge Graph</h2>
    <div bind:this={container} class="d3-container"></div>
</div>
