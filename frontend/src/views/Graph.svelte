<!--
Module: frontend/src/views/Graph.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Graph view for rendering knowledge nodes.
-->
<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { api } from "../lib/api.js";

    let container = $state();
    let loading = $state(true);
    let error = $state(null);
    let nodes = $state([]);
    let edges = $state([]);

    onMount(async () => {
        try {
            const data = await api.graph.data();
            nodes = data.nodes || [];
            edges = data.edges || [];

            if (nodes.length > 0 && container) {
                renderGraph();
            }
        } catch (e) {
            console.error(e);
            error = e.message;
        } finally {
            loading = false;
        }
    });

    function renderGraph() {
        if (!container) return;

        const width = container.clientWidth;
        const height = container.clientHeight || 500;

        // Clear existing svg
        d3.select(container).selectAll("*").remove();

        const svg = d3.select(container)
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", [0, 0, width, height]);

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(edges).id(d => d.id).distance(80))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide(20));

        const link = svg.append("g")
            .attr("stroke", "#4b5563")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(edges)
            .join("line")
            .attr("stroke-width", d => Math.sqrt(d.weight || 1));

        const node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("r", 8)
            .attr("fill", d => {
                switch(d.node_type) {
                    case "file": return "#10b981"; // green
                    case "wiki_page": return "#14b8a6"; // teal
                    case "person": return "#f59e0b"; // yellow
                    case "concept": return "#6b7280"; // grey
                    case "project": return "#ef4444"; // red
                    default: return "#3b82f6"; // blue
                }
            })
            .call(drag(simulation));

        node.append("title")
            .text(d => d.label);

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        });
    }

    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }
</script>

<div class="graph-container p-4 h-full flex flex-col">
    <h2 class="text-xl font-bold mb-4">Knowledge Graph</h2>

    {#if loading}
        <p>Loading graph data...</p>
    {:else if error}
        <p class="text-red-500">Error: {error}</p>
    {:else}
        <div bind:this={container} class="flex-1 border p-4 bg-gray-800 rounded shadow min-h-[500px] overflow-hidden">
            {#if nodes.length === 0}
                <p class="text-gray-400 italic">Graph is empty.</p>
            {/if}
        </div>
    {/if}
</div>
