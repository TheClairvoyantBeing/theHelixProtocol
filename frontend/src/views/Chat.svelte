<script>
    import { api } from "../lib/api.js";
    import { marked } from "marked";
    import DOMPurify from "dompurify";
    import { IconSend, IconBrain, IconX } from '@tabler/icons-svelte';
    import { activeSession } from '../stores/helix.js';
    import { onMount } from "svelte";

    let inputMessage = $state("");
    let messages = $state([]);
    let sessionId = $state("session_123");
    let isStreaming = $state(false);
    let showMemoryPanel = $state(false);
    let chatContainer = $state(null);
    
    // Memory data
    let semanticFacts = $state([]);
    let recentSessions = $state([]);
    let loadingMemory = $state(false);

    // Load initial context or session if needed
    onMount(() => {
        if ($activeSession) {
            sessionId = $activeSession;
        } else {
            activeSession.set(sessionId);
        }
    });

    // Auto-scroll to bottom when messages update
    $effect(() => {
        if (messages.length && chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });

    async function fetchMemoryData() {
        loadingMemory = true;
        try {
            const [facts, sessions] = await Promise.all([
                api.memory.facts ? api.memory.facts() : Promise.resolve([]),
                api.chat.sessions ? api.chat.sessions() : Promise.resolve([])
            ]);
            semanticFacts = facts || [];
            recentSessions = (sessions || []).filter(s => s !== sessionId).slice(0, 5);
        } catch (e) {
            console.error("Failed to fetch memory data:", e);
        } finally {
            loadingMemory = false;
        }
    }

    $effect(() => {
        if (showMemoryPanel) {
            fetchMemoryData();
        }
    });

    async function sendMessage() {
        if (!inputMessage.trim() || isStreaming) return;

        const userMsg = inputMessage;
        messages = [...messages, { role: "user", content: userMsg }];
        inputMessage = "";
        isStreaming = true;

        let assistantMsg = { role: "assistant", content: "" };
        messages = [...messages, assistantMsg];

        try {
            const response = await api.chat.message(sessionId, userMsg);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                // Assuming chunk contains raw text or SSE format `data: ...`
                assistantMsg.content += chunk.replace(/^data:\s*/gm, "");
                messages[messages.length - 1] = assistantMsg;
            }
        } catch (e) {
            console.error(e);
            assistantMsg.content += "\n\n**Error:** Failed to get response.";
            messages[messages.length - 1] = assistantMsg;
        } finally {
            isStreaming = false;
        }
    }

    function handleKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }
</script>

<div class="h-full flex relative overflow-hidden bg-white dark:bg-obsidian-900 transition-colors">
    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col relative transition-all duration-300 {showMemoryPanel ? 'mr-80' : ''}">

        <!-- Header -->
        <header class="h-14 border-b border-gray-200 dark:border-obsidian-700 flex items-center justify-between px-6 bg-obsidian-50 dark:bg-obsidian-900/80 backdrop-blur-sm z-10 absolute top-0 w-full transition-colors">
            <h2 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Chat with HELIX</h2>
            <button
                class="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-obsidian-700 text-gray-500 dark:text-gray-400 transition-colors"
                onclick={() => showMemoryPanel = !showMemoryPanel}
                title="Toggle Memory Inspector"
            >
                <IconBrain size={20} />
            </button>
        </header>

        <!-- Messages List -->
        <div bind:this={chatContainer} class="flex-1 overflow-y-auto px-4 pt-20 pb-32">
            <div class="max-w-3xl mx-auto space-y-6">
                {#if messages.length === 0}
                    <div class="flex flex-col items-center justify-center h-64 text-gray-400 dark:text-gray-500">
                        <div class="w-16 h-16 rounded-full bg-obsidian-100 dark:bg-obsidian-800 flex items-center justify-center mb-4">
                            <IconBrain size={32} />
                        </div>
                        <p class="text-lg">How can I help you today?</p>
                    </div>
                {/if}

                {#each messages as msg}
                    <div class={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {#if msg.role === 'assistant'}
                            <div class="w-8 h-8 rounded-full bg-claude-accent flex-shrink-0 flex items-center justify-center mr-4 mt-1 text-white font-bold text-xs">
                                H
                            </div>
                        {/if}

                        <div class={`max-w-[85%] rounded-2xl px-5 py-3 ${
                            msg.role === 'user'
                            ? 'bg-claude-bubble text-gray-900 dark:bg-claude-darkBubble dark:text-gray-100'
                            : 'bg-transparent text-gray-800 dark:text-gray-200'
                        }`}>
                            {#if msg.role === 'assistant'}
                                <div class="markdown-body prose dark:prose-invert max-w-none text-[15px] leading-relaxed">
                                    {@html DOMPurify.sanitize(marked(msg.content || ' '))}
                                </div>
                            {:else}
                                <p class="text-[15px] whitespace-pre-wrap">{msg.content}</p>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Input Area (Bottom Anchored) -->
        <div class="absolute bottom-0 w-full bg-gradient-to-t from-white dark:from-obsidian-900 pt-6 pb-6 px-4">
            <div class="max-w-3xl mx-auto relative">
                <form class="relative flex items-end shadow-lg rounded-2xl bg-white dark:bg-obsidian-800 border border-gray-200 dark:border-obsidian-700 transition-colors focus-within:ring-2 focus-within:ring-claude-accent/50" onsubmit={(e) => { e.preventDefault(); sendMessage(); }}>
                    <textarea
                        bind:value={inputMessage}
                        onkeydown={handleKeydown}
                        placeholder="Message HELIX..."
                        class="w-full max-h-48 min-h-[56px] resize-none bg-transparent border-none rounded-2xl pl-4 pr-14 py-4 focus:ring-0 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                        disabled={isStreaming}
                        rows="1"
                    ></textarea>
                    <button
                        type="submit"
                        class="absolute right-2 bottom-2 p-2 rounded-xl bg-claude-accent hover:bg-orange-500 text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={isStreaming || !inputMessage.trim()}
                    >
                        <IconSend size={20} />
                    </button>
                </form>
                <p class="text-center text-xs text-gray-400 dark:text-gray-500 mt-3">HELIX runs locally. Your data stays on your machine.</p>
            </div>
        </div>
    </div>

    <!-- Memory Inspector Sidebar (Right) -->
    <aside class={`absolute right-0 top-0 h-full w-80 bg-obsidian-50 dark:bg-obsidian-800 border-l border-gray-200 dark:border-obsidian-700 transition-transform duration-300 transform ${showMemoryPanel ? 'translate-x-0' : 'translate-x-full'} shadow-2xl z-20`}>
        <div class="p-4 border-b border-gray-200 dark:border-obsidian-700 flex justify-between items-center bg-white dark:bg-obsidian-900/50">
            <h3 class="font-semibold text-gray-800 dark:text-gray-200 flex items-center gap-2">
                <IconBrain size={18} class="text-claude-accent"/> Why HELIX knows this
            </h3>
            <button onclick={() => showMemoryPanel = false} class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                <IconX size={18} />
            </button>
        </div>
        <div class="p-4 overflow-y-auto h-[calc(100%-60px)] space-y-6">

            <div>
                <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Semantic Memory</h4>
                <div class="space-y-2">
                    {#if loadingMemory}
                        <div class="animate-pulse space-y-2">
                            <div class="h-10 bg-gray-200 dark:bg-obsidian-700 rounded"></div>
                            <div class="h-10 bg-gray-200 dark:bg-obsidian-700 rounded"></div>
                        </div>
                    {:else if semanticFacts.length === 0}
                        <p class="text-xs text-gray-500 italic text-center py-2">No facts stored yet.</p>
                    {:else}
                        {#each semanticFacts as fact}
                            <div class="p-3 bg-white dark:bg-obsidian-900 border border-gray-200 dark:border-obsidian-700 rounded text-sm text-gray-700 dark:text-gray-300 shadow-sm">
                                {fact.fact}
                            </div>
                        {/each}
                    {/if}
                </div>
            </div>

            <div>
                <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Episodic Context (Recent)</h4>
                <div class="space-y-3">
                    {#if loadingMemory}
                        <div class="animate-pulse space-y-2">
                            <div class="h-16 bg-gray-200 dark:bg-obsidian-700 rounded"></div>
                        </div>
                    {:else if recentSessions.length === 0}
                        <p class="text-xs text-gray-500 italic text-center py-2">No recent sessions.</p>
                    {:else}
                        {#each recentSessions as sess}
                            <div class="p-3 bg-white dark:bg-obsidian-900 border border-gray-200 dark:border-obsidian-700 rounded shadow-sm cursor-pointer hover:border-claude-accent transition-colors" onclick={() => { sessionId = sess; activeSession.set(sess); showMemoryPanel = false; }}>
                                <p class="text-xs text-gray-400 mb-1">Session</p>
                                <p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">{sess}</p>
                            </div>
                        {/each}
                    {/if}
                </div>
            </div>

        </div>
    </aside>
</div>

<style>
    /* Premium markdown styles for chat bubbles */
    :global(.prose p) { margin-top: 0.5em; margin-bottom: 0.5em; }
    :global(.prose pre) {
        background-color: #1a1a1a !important;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        overflow-x: auto;
    }
    :global(.prose code) {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.875em;
        padding: 0.2em 0.4em;
        background-color: rgba(128, 128, 128, 0.15);
        border-radius: 0.25rem;
    }
    :global(.prose pre code) {
        background-color: transparent;
        padding: 0;
        color: #e5e7eb;
    }
    :global(.prose ul) { list-style-type: disc; padding-left: 1.5em; margin: 0.5em 0; }
    :global(.prose ol) { list-style-type: decimal; padding-left: 1.5em; margin: 0.5em 0; }
</style>
