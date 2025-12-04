window.addEventListener("DOMContentLoaded", function () {

  const apiURL = "http://127.0.0.1:8000/ask";

  const btn = document.getElementById("askBtn");
  const qInput = document.getElementById("question");
  const ans = document.getElementById("answer");
  const src = document.getElementById("sources");

  if (!btn) return;

  btn.addEventListener("click", async () => {
    ans.innerText = "Thinking...";
    src.innerText = "";

    const q = qInput.value;

    try {
      const res = await fetch(`${apiURL}?q=${encodeURIComponent(q)}`);
      const data = await res.json();

      ans.innerText = data.answer;
      src.innerText = data.sources.join("\n");
    } catch (err) {
      ans.innerText = "Error: " + err;
    }
  });
});
