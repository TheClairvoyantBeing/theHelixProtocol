<!--
Module: frontend/src/views/Chat.svelte
Copyright (c) 2026 HELIX. All rights reserved.
Chat View Component with SSE streaming support.
-->
<script>
    import { api } from '../lib/api.js';
    import DOMPurify from 'dompurify';
    import { marked } from 'marked';

    let messages = $state([]);
    let inputValue = $state("");
    let isStreaming = $state(false);
    let currentSession = $state("default_session");

    async function sendMessage() {
        if (!inputValue.trim() || isStreaming) return;

        const userMsg = { role: "user", content: inputValue };
        messages = [...messages, userMsg];
        const contentToSend = inputValue;
        inputValue = "";

        isStreaming = true;

        try {
            const res = await api.chat.message(currentSession, contentToSend);

            if (!res.ok) throw new Error("Failed to connect to chat stream.");

            const reader = res.body.getReader();
            const decoder = new TextDecoder("utf-8");

            // Add placeholder for assistant response
            let assistantMsgIndex = messages.length;
            messages = [...messages, { role: "assistant", content: "" }];

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                messages[assistantMsgIndex].content += chunk;
                // Trigger reactivity by reassigning
                messages = [...messages];
            }
        } catch (error) {
            console.error("Chat streaming error:", error);
            messages = [...messages, { role: "system", content: "Error communicating with HELIX." }];
        } finally {
            isStreaming = false;
        }
    }

    // Function to safely render markdown
    function renderMarkdown(content) {
        return DOMPurify.sanitize(marked.parse(content));
    }
</script>

<div class="chat-container flex h-full">
    <div class="chat-main w-2/3 flex flex-col p-4">
        <h2 class="text-xl font-bold mb-4">Chat</h2>

        <div class="messages flex-grow overflow-y-auto mb-4">
            {#each messages as msg}
                <div class="message mb-3 p-3 rounded-lg {msg.role === 'user' ? 'bg-blue-100 ml-auto' : 'bg-gray-100'}">
                    {#if msg.role === 'assistant'}
                        {@html renderMarkdown(msg.content)}
                    {:else}
                        {msg.content}
                    {/if}
                </div>
            {/each}
        </div>

        <div class="input-area flex gap-2">
            <input
                type="text"
                class="flex-grow border p-2 rounded"
                bind:value={inputValue}
                onkeydown={e => e.key === 'Enter' && sendMessage()}
                placeholder="Ask HELIX..."
                disabled={isStreaming}
            />
            <button
                class="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
                onclick={sendMessage}
                disabled={isStreaming}
            >
                Send
            </button>
        </div>
    </div>

    <div class="chat-sidebar w-1/3 border-l p-4">
        <h3 class="font-bold">Why HELIX knows this</h3>
        <p class="text-sm text-gray-500">Memory inspector panel</p>
        <!-- Memory details will go here -->
    </div>
</div>
