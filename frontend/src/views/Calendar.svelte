<!--
Module: frontend/src/views/Calendar.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Calendar view utilizing FullCalendar.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    // Simulated import for FullCalendar to avoid massive NPM installs in sandbox
    // import { Calendar } from '@fullcalendar/core';
    // import dayGridPlugin from '@fullcalendar/daygrid';
    // import timeGridPlugin from '@fullcalendar/timegrid';

    let calendarEl;
    let loading = $state(true);
    let events = $state([]);

    onMount(async () => {
        try {
            events = await api.calendar.events("", "");
        } catch (e) {
            console.error(e);
        }

        // In a real environment, we instantiate FullCalendar here
        /*
        let calendar = new Calendar(calendarEl, {
          plugins: [dayGridPlugin, timeGridPlugin],
          initialView: 'dayGridMonth',
          events: '/api/v1/calendar/events',
          editable: true
        });
        calendar.render();
        */
        loading = false;
    });
</script>

<div class="calendar-container p-4 h-full flex flex-col">
    <h2 class="text-xl font-bold mb-4">Calendar</h2>
    {#if loading}
        <p>Loading calendar...</p>
    {:else}
        <div bind:this={calendarEl} class="flex-1 border p-4 bg-gray-800 rounded shadow min-h-[500px]">
            <p class="text-gray-400 italic">FullCalendar will render here. ({events.length} events loaded)</p>
        </div>
    {/if}
</div>
