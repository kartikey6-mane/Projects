(function () {
  const API_BASE = "http://127.0.0.1:8000"; // <-- CHANGE IN PRODUCTION

  const bubble = document.createElement("div");
  bubble.textContent = "💬";
  Object.assign(bubble.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "56px",
    height: "56px",
    background: "#0ea5e9",
    color: "white",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "26px",
    cursor: "pointer",
    boxShadow: "0 6px 16px rgba(0,0,0,.25)",
    zIndex: 9999,
  });

  const panel = document.createElement("div");
  Object.assign(panel.style, {
    position: "fixed",
    bottom: "88px",
    right: "20px",
    width: "340px",
    height: "480px",
    background: "white",
    borderRadius: "14px",
    border: "1px solid #e5e7eb",
    display: "none",
    flexDirection: "column",
    overflow: "hidden",
    boxShadow: "0 12px 28px rgba(0,0,0,.25)",
    zIndex: 9999,
  });

  const header = document.createElement("div");
  header.textContent = "Indala Chatbot";
  Object.assign(header.style, {
    padding: "12px 14px",
    fontWeight: "600",
    background: "#f8fafc",
    borderBottom: "1px solid #e5e7eb",
  });

  const log = document.createElement("div");
  Object.assign(log.style, {
    flex: "1",
    padding: "12px",
    overflowY: "auto",
    fontSize: "14px",
    lineHeight: "1.4",
  });

  const footer = document.createElement("div");
  Object.assign(footer.style, {
    display: "flex",
    borderTop: "1px solid #e5e7eb",
  });

  const input = document.createElement("input");
  input.type = "text";
  input.placeholder = "Type here… (e.g., 'fees for BE')";
  Object.assign(input.style, {
    flex: "1",
    padding: "10px 12px",
    border: "none",
    outline: "none",
  });

  const send = document.createElement("button");
  send.textContent = "Send";
  Object.assign(send.style, {
    padding: "10px 12px",
    border: "none",
    background: "#0ea5e9",
    color: "white",
    cursor: "pointer",
  });

  function addMsg(text, who) {
    const row = document.createElement("div");
    row.textContent = text;
    row.style.margin = "6px 0";
    row.style.whiteSpace = "pre-wrap";
    if (who === "you") {
      row.style.textAlign = "right";
      row.style.opacity = "0.9";
    }
    log.appendChild(row);
    log.scrollTop = log.scrollHeight;
  }

  async function sendMsg() {
    const text = input.value.trim();
    if (!text) return;
    addMsg(text, "you");
    input.value = "";
    try {
      const res = await fetch(API_BASE + "/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      addMsg(data.reply || "No reply.", "bot");
    } catch (e) {
      addMsg("Network error. Please try again.", "bot");
    }
  }

  const footerElem = footer;
  footerElem.appendChild(input);
  footerElem.appendChild(send);
  panel.appendChild(header);
  panel.appendChild(log);
  panel.appendChild(footerElem);

  bubble.addEventListener("click", () => {
    panel.style.display = panel.style.display === "none" ? "flex" : "none";
  });
  send.addEventListener("click", sendMsg);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMsg();
  });

  document.body.appendChild(bubble);
  document.body.appendChild(panel);
})();