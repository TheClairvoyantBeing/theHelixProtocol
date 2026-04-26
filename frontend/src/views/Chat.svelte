<script>
    let messages = [];
    let inputValue = "";

    function sendMessage() {
        if (!inputValue.trim()) return;
        messages = [...messages, { role: "user", content: inputValue }];
        inputValue = "";
        // TODO: Call API via api.js
    }
</script>

<div class="chat-container">
    <h2>Chat</h2>
    <div class="messages">
        {#each messages as msg}
            <div class="message {msg.role}">
                {msg.content}
            </div>
        {/each}
    </div>
    <div class="input-area">
        <input type="text" bind:value={inputValue} on:keydown={e => e.key === 'Enter' && sendMessage()} />
        <button on:click={sendMessage}>Send</button>
    </div>
</div>
