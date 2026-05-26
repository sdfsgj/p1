const sampleJd = `Senior AI engineer / applied researcher

We are building an AI-native talent intelligence system for sourcing, ranking, and outreach.

Requirements:
- 8+ years of experience in Python backend or ML infrastructure
- Strong LLM, RAG, semantic search, and PostgreSQL experience
- Comfortable with research signals such as papers, citations, Semantic Scholar, or OpenAlex
- Able to lead ambiguous projects and mentor other engineers
- English required; US or remote preferred`;

const jdInput = document.querySelector("#jd");
const analyzeBtn = document.querySelector("#analyzeBtn");
const sampleBtn = document.querySelector("#sampleBtn");
const health = document.querySelector("#health");
const pipelineEl = document.querySelector("#pipeline");
const profileEl = document.querySelector("#profile");
const candidateListEl = document.querySelector("#candidateList");
const candidateDetailEl = document.querySelector("#candidateDetail");

let currentCandidates = [];
let activeCandidateId = null;

jdInput.value = sampleJd;

sampleBtn.addEventListener("click", () => {
  jdInput.value = sampleJd;
  jdInput.focus();
});

analyzeBtn.addEventListener("click", () => {
  runAnalysis();
});

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    if (!response.ok) throw new Error("health check failed");
    health.textContent = "Online";
    health.classList.add("ok");
  } catch {
    health.textContent = "Offline";
    health.classList.remove("ok");
  }
}

async function runAnalysis() {
  const job_description = jdInput.value.trim();
  if (!job_description) {
    candidateDetailEl.className = "candidate-detail empty-state";
    candidateDetailEl.textContent = "Paste a job description to run the pipeline.";
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.querySelector("span").textContent = "Running";

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description, limit: 6 }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "analysis failed");

    renderProfile(result.profile);
    renderPipeline(result.pipeline);
    currentCandidates = result.candidates;
    activeCandidateId = currentCandidates[0]?.id;
    renderCandidates();
    renderCandidateDetail(currentCandidates[0]);
  } catch (error) {
    candidateDetailEl.className = "candidate-detail empty-state";
    candidateDetailEl.textContent = error.message;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.querySelector("span").textContent = "Analyze";
  }
}

function renderProfile(profile) {
  const items = [
    ["Skills", profile.skills],
    ["Role Hints", profile.role_hints],
    ["Languages", profile.languages],
    ["Locations", profile.locations],
    ["Minimum Years", profile.minimum_years ? [`${profile.minimum_years}+`] : []],
    ["Flags", [
      profile.wants_research ? "Research" : null,
      profile.wants_leadership ? "Leadership" : null,
    ].filter(Boolean)],
  ];

  profileEl.innerHTML = items
    .map(([label, values]) => `
      <div class="profile-item">
        <strong>${label}</strong>
        <span>${values.length ? values.join(", ") : "Not specified"}</span>
      </div>
    `)
    .join("");
}

function renderPipeline(phases) {
  pipelineEl.innerHTML = phases
    .map((phase) => `
      <div class="phase">
        <b>${phase.phase}</b>
        <span>${phase.name}</span>
        <small>${phase.status}</small>
      </div>
    `)
    .join("");
}

function renderCandidates() {
  candidateListEl.innerHTML = currentCandidates
    .map((candidate) => `
      <button class="candidate-card ${candidate.id === activeCandidateId ? "active" : ""}" data-id="${candidate.id}">
        <div class="score">${candidate.score}</div>
        <div>
          <h3>${candidate.name}</h3>
          <p>${candidate.title} · ${candidate.location}</p>
          <div class="chips">
            ${candidate.matched_skills.slice(0, 4).map((skill) => `<span class="chip">${skill}</span>`).join("")}
          </div>
        </div>
      </button>
    `)
    .join("");

  document.querySelectorAll(".candidate-card").forEach((button) => {
    button.addEventListener("click", () => {
      activeCandidateId = button.dataset.id;
      renderCandidates();
      renderCandidateDetail(currentCandidates.find((candidate) => candidate.id === activeCandidateId));
    });
  });
}

function renderCandidateDetail(candidate) {
  if (!candidate) {
    candidateDetailEl.className = "candidate-detail empty-state";
    candidateDetailEl.textContent = "No candidate selected.";
    return;
  }

  candidateDetailEl.className = "candidate-detail";
  candidateDetailEl.innerHTML = `
    <div class="detail-head">
      <div>
        <h3>${candidate.name}</h3>
        <div class="meta">${candidate.title} · ${candidate.location}</div>
      </div>
      <div class="score">${candidate.score}</div>
    </div>

    <div class="chips">
      ${candidate.skills.map((skill) => `<span class="chip">${skill}</span>`).join("")}
    </div>

    <div class="metric-grid">
      <div class="metric"><strong>${candidate.years_experience}</strong><span>Years</span></div>
      <div class="metric"><strong>${candidate.h_index}</strong><span>h-index</span></div>
      <div class="metric"><strong>${candidate.citations}</strong><span>Citations</span></div>
      <div class="metric"><strong>${candidate.github_stars}</strong><span>GitHub stars</span></div>
    </div>

    <div class="score-bars">
      ${Object.entries(candidate.scores).map(([label, value]) => `
        <div class="bar-row">
          <span>${titleCase(label)}</span>
          <div class="bar-track"><div class="bar-fill" style="width: ${value}%"></div></div>
          <strong>${value}</strong>
        </div>
      `).join("")}
    </div>

    <div class="section-heading">Why This Match</div>
    <ul class="reason-list">
      ${candidate.reasons.map((reason) => `<li>${reason}</li>`).join("")}
    </ul>

    <div class="section-heading">Outreach Draft</div>
    <div class="outreach">${candidate.outreach}</div>
  `;
}

function titleCase(value) {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

checkHealth();
runAnalysis();
