/* ===================================================
   SkillMatch AI – Frontend Logic
   =================================================== */

// ── Tab Switching ───────────────────────────────────
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + tab).classList.add('active');
  });
});

document.querySelectorAll('.result-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    const rtab = btn.dataset.rtab;
    document.querySelectorAll('.result-tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.result-tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('rtab-' + rtab).classList.add('active');
  });
});

// ── File Upload ─────────────────────────────────────
let uploadedFileText = '';

const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');

if (fileInput) {
  fileInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (file) readFile(file);
  });
}

if (uploadZone) {
  uploadZone.addEventListener('dragover', e => {
    e.preventDefault();
    uploadZone.style.borderColor = '#6366f1';
    uploadZone.style.background = '#f5f3ff';
  });
  uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = '';
    uploadZone.style.background = '';
  });
  uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.style.borderColor = '';
    uploadZone.style.background = '';
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.txt')) readFile(file);
    else alert('Please upload a .txt file.');
  });
}

function readFile(file) {
  const reader = new FileReader();
  reader.onload = e => {
    uploadedFileText = e.target.result;
    document.getElementById('uploadPreview').style.display = 'flex';
    document.getElementById('uploadZone').style.display = 'none';
    document.getElementById('fileName').textContent = file.name;
  };
  reader.readAsText(file);
}

function clearFile() {
  uploadedFileText = '';
  document.getElementById('uploadPreview').style.display = 'none';
  document.getElementById('uploadZone').style.display = '';
  document.getElementById('fileInput').value = '';
}

// ── Analyze Function ────────────────────────────────
async function analyzeResume() {
  const activeTab = document.querySelector('.tab.active')?.dataset.tab;
  const resumeText = activeTab === 'upload'
    ? uploadedFileText
    : document.getElementById('resumeText').value.trim();
  const jobDesc    = document.getElementById('jobDesc').value.trim();
  const jobRole    = document.getElementById('jobRole').value;
  const expLevel   = document.getElementById('expLevel').value;

  if (!resumeText) { alert('Please paste or upload your resume.'); return; }
  if (!jobDesc)    { alert('Please paste the job description.'); return; }

  // Show loader
  document.getElementById('btnText').style.display = 'none';
  document.getElementById('btnLoader').style.display = 'flex';
  document.getElementById('analyzeBtn').disabled = true;

  try {
    const res = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resume: resumeText, job_desc: jobDesc, role: jobRole, exp_level: expLevel })
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.error(err);
    alert('Analysis failed: ' + err.message);
  } finally {
    document.getElementById('btnText').style.display = 'flex';
    document.getElementById('btnLoader').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = false;
  }
}

// ── Render Results ──────────────────────────────────
function renderResults(data) {
  document.getElementById('resultsPlaceholder').style.display = 'none';
  const rc = document.getElementById('resultsContent');
  rc.style.display = 'block';
  rc.classList.add('fade-in');

  // Score ring
  const score    = data.match_score || 0;
  const circumf  = 314;
  const offset   = circumf - (score / 100) * circumf;
  const ringFill = document.getElementById('ringFill');
  ringFill.style.strokeDashoffset = circumf; // reset first
  setTimeout(() => { ringFill.style.strokeDashoffset = offset; }, 50);

  // Ring color by score
  if      (score >= 75) ringFill.style.stroke = '#10b981';
  else if (score >= 50) ringFill.style.stroke = '#f59e0b';
  else                  ringFill.style.stroke = '#ef4444';

  document.getElementById('scoreNumber').textContent = score + '%';

  // Title + description
  let title, desc;
  if      (score >= 75) { title = '🎉 Strong Match!';      desc = 'You meet most requirements. Focus on a few gaps to stand out.'; }
  else if (score >= 50) { title = '👍 Good Potential';      desc = 'A solid foundation — close the highlighted skill gaps to be competitive.'; }
  else if (score >= 30) { title = '🚀 Room to Grow';        desc = 'Notable skill gaps exist. Follow the roadmap to get job-ready.'; }
  else                  { title = '📚 Start Your Journey'; desc = 'Many skills needed. Use the learning roadmap to build them step by step.'; }

  document.getElementById('scoreTitle').textContent = title;
  document.getElementById('scoreDesc').textContent  = desc;

  // Chips
  const badges = document.getElementById('scoreBadges');
  badges.innerHTML = '';
  [
    { label: `${data.matched_skills?.length || 0} Matched`,  cls: 'chip-green' },
    { label: `${data.missing_skills?.length || 0} Missing`,  cls: 'chip-red'   },
    { label: `${data.extra_skills?.length   || 0} Bonus`,    cls: 'chip-blue'  },
  ].forEach(({ label, cls }) => {
    const s = document.createElement('span');
    s.className = `score-chip ${cls}`;
    s.textContent = label;
    badges.appendChild(s);
  });

  // Reset to first result tab
  document.querySelectorAll('.result-tab').forEach((b, i) => b.classList.toggle('active', i === 0));
  document.querySelectorAll('.result-tab-content').forEach((c, i) => c.classList.toggle('active', i === 0));

  renderSkills(data);
  renderGaps(data);
  renderRoadmap(data);
}

// ── Render Skills Tab ───────────────────────────────
function renderSkills(data) {
  const matchedEl = document.getElementById('matchedSkills');
  const missingEl = document.getElementById('missingSkills');
  const extraEl   = document.getElementById('extraSkills');

  matchedEl.innerHTML = '';
  missingEl.innerHTML = '';
  extraEl.innerHTML   = '';

  (data.matched_skills || []).forEach(s => {
    matchedEl.appendChild(skillTag(s.name || s, 'matched', s.score));
  });
  (data.missing_skills || []).forEach(s => {
    missingEl.appendChild(skillTag(s.name || s, 'missing', s.importance));
  });
  (data.extra_skills || []).forEach(s => {
    extraEl.appendChild(skillTag(s.name || s, 'extra'));
  });
}

function skillTag(name, type, score) {
  const span = document.createElement('span');
  span.className = `skill-tag skill-${type}`;
  let icon = type === 'matched' ? '✓' : type === 'missing' ? '✗' : '＋';
  span.innerHTML = `${icon} ${name}` + (score != null ? `<span class="skill-percent">${Math.round(score)}%</span>` : '');
  return span;
}

// ── Render Gaps Tab ──────────────────────────────────
function renderGaps(data) {
  const el = document.getElementById('gapsList');
  el.innerHTML = '';
  const gaps = data.skill_gaps || [];
  if (!gaps.length) {
    el.innerHTML = '<p style="color:#57606a;text-align:center;padding:40px 0">No significant skill gaps detected — great job!</p>';
    return;
  }
  gaps.forEach(g => {
    const priority = g.priority || 'medium';
    const pctGap   = g.gap_percent || 70;
    el.innerHTML += `
      <div class="gap-item fade-in">
        <div class="gap-header">
          <span class="gap-name">${g.skill}</span>
          <span class="priority-chip priority-${priority}">${priority.toUpperCase()} PRIORITY</span>
        </div>
        <div class="gap-bar"><div class="gap-fill" style="width:${pctGap}%"></div></div>
        <p class="gap-desc">${g.description || 'This skill is required for the role. See roadmap for learning resources.'}</p>
      </div>`;
  });
}

// ── Render Roadmap Tab ───────────────────────────────
function renderRoadmap(data) {
  const el = document.getElementById('roadmapList');
  el.innerHTML = '';
  const roadmap = data.roadmap || [];
  if (!roadmap.length) {
    el.innerHTML = '<p style="color:#57606a;text-align:center;padding:40px 0">No roadmap generated — you already match the job well!</p>';
    return;
  }
  roadmap.forEach((step, i) => {
    const links = (step.resources || []).map(r =>
      `<a href="${r.url}" target="_blank" rel="noopener" class="resource-link">${r.name}</a>`
    ).join('');
    el.innerHTML += `
      <div class="roadmap-item fade-in">
        <div class="roadmap-left">
          <div class="roadmap-dot">${i + 1}</div>
          <div class="roadmap-line"></div>
        </div>
        <div class="roadmap-content">
          <div class="roadmap-week">${step.timeline || 'Week ' + (i * 2 + 1) + '-' + (i * 2 + 2)}</div>
          <h4>${step.skill}</h4>
          <p>${step.description || ''}</p>
          <div class="resource-links">${links}</div>
        </div>
      </div>`;
  });
}
