document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault(); // Stop form from refreshing the page

  const userInput = document.getElementById("user-input").value;
  const chatBox = document.getElementById("chat-box");

  // Show user message
  const userMessage = document.createElement("div");
  userMessage.textContent = "You: " + userInput;
  chatBox.appendChild(userMessage);

  // Scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;

  // Clear input field
  document.getElementById("user-input").value = "";

  // Show loading message
  const loadingMessage = document.createElement("div");
  loadingMessage.textContent = "Bot: Thinking...";
  chatBox.appendChild(loadingMessage);

  try {
    const response = await fetch("https://alanna-chatbot.onrender.com/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: userInput })
    });

    const data = await response.json();
    loadingMessage.textContent = "Bot: " + (data.answer || "No response received.");
  } catch (error) {
    loadingMessage.textContent = "Bot: Error – " + error.message;
  }

  // Scroll again
  chatBox.scrollTop = chatBox.scrollHeight;
});