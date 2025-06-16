<script>
  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const userMessage = input.value.trim();
      if (!userMessage) return;

      // Show user's message
      appendMessage("You", userMessage);
      input.value = "";

      // Call backend
      try {
        const response = await fetch("https://alanna-chatbot.onrender.com/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();
        appendMessage("Bot", data.reply || "No response.");
      } catch (error) {
        console.error("Error:", error);
        appendMessage("Bot", "Sorry, something went wrong.");
      }
    });

    function appendMessage(sender, text) {
      const message = document.createElement("div");
      message.classList.add("message");
      message.innerHTML = `<strong>${sender}:</strong> ${text}`;
      chatBox.appendChild(message);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
</script>