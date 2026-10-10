document.addEventListener("DOMContentLoaded", () => {
  const resumeInput = document.getElementById("resume");
  const fileName = document.getElementById("file-name");
  const uploadArea = document.getElementById("upload-area");
  const form = document.getElementById("analysis-form");

  if (resumeInput && fileName) {
    resumeInput.addEventListener("change", () => {
      const file = resumeInput.files && resumeInput.files[0];
      if (!file) {
        fileName.textContent = "No file selected";
        return;
      }
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        resumeInput.value = "";
        fileName.textContent = "Please choose a PDF file.";
        return;
      }
      if (file.size > 8 * 1024 * 1024) {
        resumeInput.value = "";
        fileName.textContent = "File is larger than 8 MB.";
        return;
      }
      fileName.textContent = file.name;
    });
  }

  if (uploadArea && resumeInput) {
    ["dragenter", "dragover"].forEach(eventName => {
      uploadArea.addEventListener(eventName, event => {
        event.preventDefault();
        uploadArea.classList.add("is-dragging");
      });
    });
    ["dragleave", "drop"].forEach(eventName => {
      uploadArea.addEventListener(eventName, event => {
        event.preventDefault();
        uploadArea.classList.remove("is-dragging");
      });
    });
    uploadArea.addEventListener("drop", event => {
      const files = event.dataTransfer && event.dataTransfer.files;
      if (files && files.length) {
        try {
          resumeInput.files = files;
          resumeInput.dispatchEvent(new Event("change", { bubbles: true }));
        } catch (_) {
          fileName.textContent = "Use “Choose PDF” to select your file.";
        }
      }
    });
  }

  if (form) {
    form.addEventListener("submit", event => {
      const checked = form.querySelectorAll('input[name="skills"]:checked').length;
      const extra = document.getElementById("extra_skills");
      const hasExtra = extra && extra.value.trim().length > 0;
      const hasResume = resumeInput && resumeInput.files && resumeInput.files.length > 0;
      if (!checked && !hasExtra && !hasResume) {
        event.preventDefault();
        let message = form.querySelector(".client-validation");
        if (!message) {
          message = document.createElement("p");
          message.className = "client-validation";
          message.setAttribute("role", "alert");
          message.style.cssText = "color:#a44332;font-size:12px;margin:14px 0 0;";
          form.prepend(message);
        }
        message.textContent = "Select at least one skill, enter skill keywords, or upload a PDF resume.";
        document.getElementById("analyzer").scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  const chartData = window.skillReadyChartData;
  const chartCanvas = document.getElementById("roleChart");
  if (chartData && chartCanvas && window.Chart) {
    new Chart(chartCanvas, {
      type: "bar",
      data: {
        labels: chartData.labels,
        datasets: [{
          label: "Skill match",
          data: chartData.scores,
          backgroundColor: chartData.scores.map((_, i) => i === 0 ? "#167c73" : "#a8d5c0"),
          borderRadius: 6,
          borderSkipped: false,
          barThickness: 17
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: context => ` ${context.raw}% skill match` } }
        },
        scales: {
          x: { beginAtZero: true, max: 100, grid: { color: "#edf1ed" }, ticks: { callback: value => `${value}%`, font: { size: 10 }, color: "#7e8b84" }, border: { display: false } },
          y: { grid: { display: false }, ticks: { font: { size: 10 }, color: "#465a52" }, border: { display: false } }
        }
      }
    });
    const resultSection = document.getElementById("results");
    if (resultSection) {
      setTimeout(() => resultSection.scrollIntoView({ behavior: "smooth", block: "start" }), 120);
    }
  }
});
