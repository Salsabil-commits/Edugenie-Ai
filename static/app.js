const tasks = {
  qa: { title: "Ask a question", label: "What would you like to understand?", placeholder: "Example: Why is the Pacific Ocean the largest ocean?", hint: "Be specific for a more useful answer.", button: "Ask EduGenie", endpoint: "/qa", field: "question" },
  explain: { title: "Explain a concept", label: "What should we make clearer?", placeholder: "Example: Explain photosynthesis to a 12-year-old.", hint: "Name the topic and your current level.", button: "Explain it", endpoint: "/explain", field: "text" },
  quiz: { title: "Generate a quiz", label: "Paste a topic or passage to turn into practice.", placeholder: "Example: The water cycle includes evaporation, condensation, precipitation...", hint: "You will get three multiple-choice questions.", button: "Build my quiz", endpoint: "/quiz", field: "text" },
  summarize: { title: "Summarize text", label: "What should we condense?", placeholder: "Paste an article, lesson, or paragraph here...", hint: "Keep the important context in your passage.", button: "Summarize", endpoint: "/summarize", field: "text" },
  learn: { title: "Build a learning path", label: "What do you want to learn?", placeholder: "Example: SQL for data analysis", hint: "Set your pace below for a more realistic plan.", button: "Map my path", endpoint: "/learn/recommendations", field: "topic" }
};
let currentTask = "qa";
const $ = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
const markdownLite = (value) => escapeHtml(value).replace(/^### (.*)$/gm, "<h3>$1</h3>").replace(/^## (.*)$/gm, "<h2>$1</h2>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>").replace(/\n\n/g, "</p><p>").replace(/\n/g, "<br>");

function selectTask(name) {
  currentTask = name;
  const task = tasks[name];
  document.querySelectorAll(".task").forEach((button) => {
    const active = button.dataset.task === name;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", active);
  });
  $("task-title").textContent = task.title;
  $("prompt-label").textContent = task.label;
  $("prompt").placeholder = task.placeholder;
  $("input-hint").textContent = task.hint;
  $("submit-label").textContent = task.button;
  $("learning-options").classList.toggle("hidden", name !== "learn");
  const index = Object.keys(tasks).indexOf(name) + 1;
  document.querySelector(".step").innerHTML = `0${index} <i>/</i> 05`;
  $("prompt").focus();
}

function renderQuiz(questions) {
  return questions.map((item, index) => `<article class="quiz-card"><h3>${index + 1}. ${escapeHtml(item.question)}</h3>${item.options.map((option) => `<button class="quiz-option" data-answer="${escapeHtml(item.answer)}">${escapeHtml(option)}</button>`).join("")}<p class="quiz-explanation hidden">${escapeHtml(item.explanation)}</p></article>`).join("");
}

document.querySelectorAll(".task").forEach((button) => button.addEventListener("click", () => selectTask(button.dataset.task)));
$("assistant-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const task = tasks[currentTask];
  const prompt = $("prompt");
  if (!prompt.value.trim()) return;
  const payload = currentTask === "learn" ? { topic: prompt.value.trim(), level: $("level").value, weekly_hours: Number($("weekly-hours").value) } : { [task.field]: prompt.value.trim() };
  const submit = document.querySelector(".submit-button");
  submit.disabled = true;
  $("submit-label").textContent = "Thinking...";
  $("result-empty").classList.add("hidden");
  $("result").classList.remove("hidden");
  $("result-content").innerHTML = '<p class="hint">Working through that now...</p>';
  try {
    const response = await fetch(task.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail?.[0]?.msg || data.detail || "The request could not be completed.");
    $("source-badge").textContent = data.source === "gemini" ? "Gemini powered" : "Offline preview";
    $("result-content").innerHTML = currentTask === "quiz" ? renderQuiz(data.questions) : `<p>${markdownLite(data.result)}</p>`;
    if (currentTask === "quiz") bindQuiz();
  } catch (error) {
    $("source-badge").textContent = "Notice";
    $("result-content").innerHTML = `<p>${escapeHtml(error.message)}</p>`;
  } finally {
    submit.disabled = false;
    $("submit-label").textContent = task.button;
  }
});

function bindQuiz() {
  document.querySelectorAll(".quiz-option").forEach((option) => option.addEventListener("click", () => {
    const card = option.closest(".quiz-card");
    const correct = option.textContent === option.dataset.answer;
    option.classList.add(correct ? "correct" : "wrong");
    card.querySelector(".quiz-explanation").classList.remove("hidden");
  }));
}