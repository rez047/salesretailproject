function send() {
  fetch("/chat/send", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      receiver_id: 2,
      message: document.getElementById("msg").value
    })
  }).then(() => loadChat());
}

function loadChat() {
  fetch("/chat/2")
    .then(res => res.json())
    .then(data => {
      let box = document.getElementById("chatBox");
      box.innerHTML = "";

      data.forEach(m => {
        let div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `<b>${m.from}</b>: ${m.msg}`;
        box.appendChild(div);
      });
    });
}

loadChat();