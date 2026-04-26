<script>
    import { onMount } from "svelte";

    let calendarEl;

    onMount(() => {
        // TODO: Initialize FullCalendar here
    });
</script>

<div class="calendar-container">
    <h2>Calendar</h2>
    <div bind:this={calendarEl}></div>
</div>
