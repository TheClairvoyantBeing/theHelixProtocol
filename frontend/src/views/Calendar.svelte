<!--
Module: frontend/src/views/Calendar.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Calendar view utilizing FullCalendar.
-->
<script>
    import { onMount } from "svelte";
    import { api } from "../lib/api.js";
    import { Calendar } from '@fullcalendar/core';
    import dayGridPlugin from '@fullcalendar/daygrid';
    import timeGridPlugin from '@fullcalendar/timegrid';

    let calendarEl = $state();
    let loading = $state(true);
    let events = $state([]);

    onMount(async () => {
        try {
            events = await api.calendar.events("", "");
        } catch (e) {
            console.error(e);
        }
        loading = false;

        if (calendarEl) {
            let calendar = new Calendar(calendarEl, {
                plugins: [dayGridPlugin, timeGridPlugin],
                initialView: 'dayGridMonth',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                // Format the events appropriately for FullCalendar if we had real dates
                events: events.map(e => ({ title: e, start: new Date() })),
                editable: true
            });
            calendar.render();
        }
    });
</script>

<div class="calendar-container p-4 h-full flex flex-col overflow-y-auto bg-white dark:bg-obsidian-900 transition-colors">
    <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-gray-100">Calendar</h2>
    {#if loading}
        <div class="animate-pulse flex space-x-4">
          <div class="flex-1 space-y-4 py-1">
            <div class="h-64 bg-gray-200 dark:bg-obsidian-800 rounded"></div>
          </div>
        </div>
    {:else}
        <!-- Ensure styling cascades into fullcalendar internal css -->
        <div class="flex-1 p-4 bg-white dark:bg-obsidian-800 rounded shadow min-h-[600px] border border-gray-200 dark:border-obsidian-700 fc-theme-standard">
            <div bind:this={calendarEl}></div>
        </div>
    {/if}
</div>

<style>
    /* Basic overrides to make FullCalendar look okay in dark mode */
    :global(.fc) {
        --fc-border-color: #374151; /* gray-700 */
        --fc-button-bg-color: #4b5563; /* gray-600 */
        --fc-button-border-color: #374151;
        --fc-button-hover-bg-color: #374151;
        --fc-button-hover-border-color: #1f2937;
        --fc-button-active-bg-color: #1f2937;
        --fc-button-active-border-color: #111827;
    }
    :global(.dark .fc-theme-standard td), :global(.dark .fc-theme-standard th) {
        border-color: #374151;
    }
    :global(.dark .fc-col-header-cell-cushion), :global(.dark .fc-daygrid-day-number) {
        color: #e5e7eb; /* gray-200 */
    }
</style>
