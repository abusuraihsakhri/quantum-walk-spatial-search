/** Exact closed-system CTQW search on the complete graph K_N (hbar = 1). */
export function simulateCompleteGraph(nodeCount = 16, markedVertex = 0, gamma = null, maxTime = null, samples = 401) {
  if (!Number.isInteger(nodeCount) || nodeCount < 2 || nodeCount > 100000) {
    throw new RangeError('Number of vertices must be an integer from 2 to 100,000.');
  }
  if (!Number.isInteger(markedVertex) || markedVertex < 0 || markedVertex >= nodeCount) {
    throw new RangeError('Marked vertex must be an integer from 0 to N − 1.');
  }
  if (!Number.isInteger(samples) || samples < 2 || samples > 2001) {
    throw new RangeError('Samples must be an integer from 2 to 2,001.');
  }
  gamma = gamma === null ? 1 / nodeCount : gamma;
  maxTime = maxTime === null ? Math.PI * Math.sqrt(nodeCount) / 2 : maxTime;
  if (!Number.isFinite(gamma) || gamma <= 0) {
    throw new RangeError('Hopping rate γ must be positive and finite.');
  }
  if (!Number.isFinite(maxTime) || maxTime <= 0 || maxTime > 100000) {
    throw new RangeError('Maximum time must be in (0, 100,000].');
  }
  // Hamiltonian in the basis {|marked>, uniform(|unmarked>)}.
  const delta = (-1 + gamma * (nodeCount - 2)) / 2;
  const offdiag = -gamma * Math.sqrt(nodeCount - 1);
  const omega = Math.hypot(delta, offdiag);
  const initialMarked = 1 / Math.sqrt(nodeCount);
  const initialUnmarked = Math.sqrt((nodeCount - 1) / nodeCount);
  const transfer = (delta * initialMarked + offdiag * initialUnmarked) / omega;
  const series = [];
  for (let i = 0; i < samples; i += 1) {
    const time = maxTime * i / (samples - 1);
    const phase = omega * time;
    const probability = Math.min(1, Math.max(0,
      (initialMarked * Math.cos(phase)) ** 2 + (transfer * Math.sin(phase)) ** 2));
    series.push({ time, success_probability: probability });
  }
  const best = series.reduce((a, b) => b.success_probability > a.success_probability ? b : a);
  return {
    node_count: nodeCount, marked_vertex: markedVertex, gamma, max_time: maxTime,
    initial_probability: 1 / nodeCount, peak_time: best.time,
    peak_success_probability: best.success_probability, series
  };
}

export function resultsCsv(result) {
  return 'time,success_probability\n' +
    result.series.map(point => point.time + ',' + point.success_probability).join('\n') + '\n';
}

function drawPlot(svg, result) {
  const ns = 'http://www.w3.org/2000/svg';
  const node = (tag, attrs, text) => {
    const el = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([name, value]) => el.setAttribute(name, String(value)));
    if (text !== undefined) el.textContent = text;
    return el;
  };
  const width = 760, height = 320, left = 60, right = 20, top = 20, bottom = 48;
  const plotWidth = width - left - right, plotHeight = height - top - bottom;
  const x = time => left + plotWidth * time / result.max_time;
  const y = probability => top + plotHeight * (1 - probability);
  svg.replaceChildren(node('title', {}, 'Marked-vertex probability over time'),
    node('desc', {}, 'Exact ideal quantum-walk search probability; dashed line shows 1/N classical uniform-sampling baseline.'));
  for (let i = 0; i <= 4; i += 1) {
    const p = i / 4;
    const yp = y(p);
    svg.append(node('line', {x1:left,y1:yp,x2:width-right,y2:yp,stroke:'#dce5f0','stroke-width':1}));
    svg.append(node('text', {x:left-12,y:yp+4,'text-anchor':'end',fill:'#536477','font-size':12}, p.toFixed(2)));
  }
  for (let i = 0; i <= 4; i += 1) {
    const t = result.max_time * i / 4;
    svg.append(node('text', {x:x(t),y:height-23,'text-anchor':'middle',fill:'#536477','font-size':12}, t.toFixed(2)));
  }
  svg.append(node('line', {x1:left,y1:y(result.initial_probability),x2:width-right,y2:y(result.initial_probability),stroke:'#f59e0b','stroke-dasharray':'6 5','stroke-width':2}));
  const path = result.series.map((point, index) => (index === 0 ? 'M' : 'L') + x(point.time).toFixed(3) + ' ' + y(point.success_probability).toFixed(3)).join(' ');
  svg.append(node('path', {d:path,fill:'none',stroke:'#2563eb','stroke-width':3,'stroke-linecap':'round','stroke-linejoin':'round'}));
  svg.append(node('circle', {cx:x(result.peak_time),cy:y(result.peak_success_probability),r:5,fill:'#2563eb',stroke:'#fff','stroke-width':2}));
  svg.append(node('text', {x:width/2,y:height-3,'text-anchor':'middle',fill:'#536477','font-size':13}, 'Time (ℏ = 1)'));
  svg.append(node('text', {x:16,y:height/2,transform:'rotate(-90 16 '+height/2+')','text-anchor':'middle',fill:'#536477','font-size':13}, 'Success probability'));
}

function initialize() {
  const form = document.getElementById('search-form');
  const nodes = document.getElementById('nodes');
  const marked = document.getElementById('marked');
  const gamma = document.getElementById('gamma');
  const autoGamma = document.getElementById('auto-gamma');
  const maxTime = document.getElementById('max-time');
  const autoTime = document.getElementById('auto-time');
  const status = document.getElementById('status');
  const download = document.getElementById('download');
  const plot = document.getElementById('plot');
  let latest = null;

  function refreshDefaults() {
    const n = Number(nodes.value);
    if (Number.isInteger(n) && n >= 2 && n <= 100000) {
      marked.max = String(n - 1);
      if (autoGamma.checked) gamma.value = String(1 / n);
      if (autoTime.checked) maxTime.value = String(Math.PI * Math.sqrt(n) / 2);
    }
    gamma.disabled = autoGamma.checked;
    maxTime.disabled = autoTime.checked;
  }
  [nodes, autoGamma, autoTime].forEach(field => field.addEventListener('change', refreshDefaults));

  form.addEventListener('submit', event => {
    event.preventDefault();
    try {
      const n = Number(nodes.value);
      const m = Number(marked.value);
      const g = Number(gamma.value);
      const t = Number(maxTime.value);
      const result = simulateCompleteGraph(n, m, g, t);
      latest = result;
      drawPlot(plot, result);
      document.getElementById('peak-probability').textContent = (100 * result.peak_success_probability).toFixed(2) + '%';
      document.getElementById('peak-time').textContent = result.peak_time.toFixed(4);
      document.getElementById('baseline').textContent = (100 * result.initial_probability).toFixed(3) + '%';
      document.getElementById('details').textContent = 'K' + n + ' · marked vertex ' + m + ' · γ = ' + g.toPrecision(6) + ' · ' + result.series.length + ' samples';
      status.textContent = 'Simulation complete. Results remain in your browser.';
      status.className = 'status success';
      download.disabled = false;
    } catch (error) {
      latest = null;
      download.disabled = true;
      status.textContent = error.message;
      status.className = 'status error';
    }
  });

  download.addEventListener('click', () => {
    if (!latest) return;
    const url = URL.createObjectURL(new Blob([resultsCsv(latest)], {type:'text/csv;charset=utf-8'}));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'quantum-walk-complete-graph.csv';
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  });
  refreshDefaults();
  form.requestSubmit();
}

if (typeof document !== 'undefined') initialize();
