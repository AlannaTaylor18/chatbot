document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const userInput = document.getElementById("user-input").value.trim();
  if (!userInput) return;

  const chatBox = document.getElementById("chat-box");

  const userMessage = document.createElement("div");
  userMessage.className = "user-message";
  userMessage.textContent = "You: " + userInput;
  chatBox.appendChild(userMessage);

  document.getElementById("user-input").value = "";

  const loadingMessage = document.createElement("div");
  loadingMessage.className = "bot-message";
  loadingMessage.textContent = "Bot: Thinking...";
  chatBox.appendChild(loadingMessage);

  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("https://alanna-chatbot.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    loadingMessage.textContent = "Bot: " + (data.reply || "No response received.");
  } catch (error) {
    loadingMessage.textContent = "Bot: Error – " + error.message;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
});