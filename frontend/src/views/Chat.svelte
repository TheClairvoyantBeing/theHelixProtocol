<script>
    import { api } from "../lib/api.js";
    import { marked } from "marked";
    import DOMPurify from "dompurify";

    let inputMessage = $state("");
    let messages = $state([]);
    let sessionId = $state("session_123");
    let isStreaming = $state(false);

    async function sendMessage() {
        if (!inputMessage.trim()) return;

        const userMsg = inputMessage;
        messages = [...messages, { role: "user", content: userMsg }];
        inputMessage = "";
        isStreaming = true;

        // Create a placeholder for the assistant's streaming response
        let assistantMsg = { role: "assistant", content: "" };
        messages = [...messages, assistantMsg];

        try {
            const response = await api.chat.message(sessionId, userMsg);

            // Handle Server-Sent Events from the streaming response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                // Assuming chunk contains raw text or SSE format, typically SSE is structured `data: ...`
                // We'll append it directly for this basic stream handling
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
</script>

<div class="chat-container h-full flex flex-col">
    <div class="flex-1 overflow-y-auto p-4 space-y-4">
        {#each messages as msg}
            <div class={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div class={`max-w-[75%] rounded p-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-200'}`}>
                    {#if msg.role === 'assistant'}
                        <!-- Safe markdown rendering -->
                        <div class="markdown-body">
                            {@html DOMPurify.sanitize(marked(msg.content))}
                        </div>
                    {:else}
                        {msg.content}
                    {/if}
                </div>
            </div>
        {/each}
    </div>

    <div class="p-4 bg-gray-800 border-t border-gray-700">
        <form class="flex gap-2" onsubmit={(e) => { e.preventDefault(); sendMessage(); }}>
            <input
                type="text"
                bind:value={inputMessage}
                placeholder="Ask HELIX..."
                class="flex-1 bg-gray-900 border border-gray-600 rounded px-4 py-2 focus:outline-none focus:border-blue-500"
                disabled={isStreaming}
            />
            <button
                type="submit"
                class="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded font-semibold disabled:opacity-50"
                disabled={isStreaming || !inputMessage.trim()}
            >
                Send
            </button>
        </form>
    </div>
</div>

<style>
    /* Basic markdown body styles */
    .markdown-body :global(p) { margin-bottom: 0.5em; }
    .markdown-body :global(pre) { background: #1a202c; padding: 1em; border-radius: 0.25rem; overflow-x: auto; }
    .markdown-body :global(code) { font-family: monospace; }
</style>
