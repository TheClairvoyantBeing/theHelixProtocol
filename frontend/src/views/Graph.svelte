<!--
Module: frontend/src/views/Graph.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Knowledge Graph view using D3.
-->
<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { api } from "../lib/api.js";

    let container;
    let loading = $state(true);
    let error = $state(null);

    onMount(async () => {
        try {
            const data = await api.graph.data();
            renderGraph(data.nodes, data.edges);
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    });

    function renderGraph(nodes, edges) {
        if (!container) return;

        const width = container.clientWidth || 800;
        const height = container.clientHeight || 600;

        // Setup force simulation
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(edges).id(d => d.id).distance(80))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide(20));

        const svg = d3.select(container).append("svg")
            .attr("width", width)
            .attr("height", height);

        // Zoom capability
        const g = svg.append("g");
        svg.call(d3.zoom().on("zoom", (event) => {
            g.attr("transform", event.transform);
        }));

        const link = g.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(edges)
            .join("line")
            .attr("stroke-width", d => Math.sqrt(d.weight || 1));

        const node = g.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("r", 8)
            .attr("fill", getColor)
            .call(drag(simulation));

        node.append("title").text(d => d.label);

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

    function getColor(d) {
        if (d.node_type === "wiki_page") return "teal";
        if (d.node_type === "person") return "yellow";
        if (d.node_type === "project") return "red";
        return "blue"; // default file
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

<div class="graph-container flex flex-col h-full p-4">
    <h2 class="text-xl font-bold mb-4">Knowledge Graph</h2>

    {#if loading}
        <p>Loading graph...</p>
    {:else if error}
        <p class="text-red-600">Error loading graph: {error}</p>
    {:else}
        <div bind:this={container} class="d3-container flex-grow border rounded bg-gray-50"></div>
    {/if}
</div>
