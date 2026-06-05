document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy-target]");
  if (!button) return;
  const target = document.getElementById(button.dataset.copyTarget);
  if (!target) return;
  await navigator.clipboard.writeText(target.value || target.textContent || "");
  button.textContent = "Copiado";
  window.setTimeout(() => {
    button.textContent = "Copiar";
  }, 1200);
});

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-select-all]");
  if (!button) return;
  const checkboxes = [...document.querySelectorAll(button.dataset.selectAll)];
  const shouldSelect = checkboxes.some((checkbox) => !checkbox.checked);
  checkboxes.forEach((checkbox) => {
    checkbox.checked = shouldSelect;
  });
  button.textContent = shouldSelect ? "Limpar selecao" : "Selecionar todos";
});

function drawGraph() {
  const source = document.getElementById("graph-data");
  const canvas = document.getElementById("graphCanvas");
  const details = document.getElementById("graphDetails");
  if (!source || !canvas || !details) return;

  const graph = JSON.parse(source.textContent || '{"nodes":[],"edges":[]}');
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const nodes = (graph.nodes || []).map((node) => ({ ...node }));
  const edges = (graph.edges || []).map((edge) => ({ ...edge }));
  const centerX = width / 2;
  const centerY = height / 2;
  let selected = null;

  if (!nodes.length) {
    ctx.clearRect(0, 0, width, height);
    details.textContent = "{}";
    return;
  }

  const byId = new Map(nodes.map((node) => [node.id, node]));
  const degree = new Map(nodes.map((node) => [node.id, 0]));
  edges.forEach((edge) => {
    degree.set(edge.source, (degree.get(edge.source) || 0) + 1);
    degree.set(edge.target, (degree.get(edge.target) || 0) + 1);
  });

  nodes.forEach((node, index) => {
    const angle = (Math.PI * 2 * index) / Math.max(nodes.length, 1);
    const ring = Math.min(width, height) * (0.18 + (index % 4) * 0.055);
    node._x = centerX + Math.cos(angle) * ring;
    node._y = centerY + Math.sin(angle) * ring;
    node._vx = 0;
    node._vy = 0;
    node._radius = Math.min(34, 16 + Math.sqrt(degree.get(node.id) || 1) * 5);
  });

  simulateLayout(nodes, edges, byId, width, height);

  const edgeGroups = new Map();
  edges.forEach((edge) => {
    const key = [edge.source, edge.target].sort().join("__");
    const group = edgeGroups.get(key) || [];
    group.push(edge);
    edgeGroups.set(key, group);
  });
  edgeGroups.forEach((group) => {
    group.forEach((edge, index) => {
      edge._offset = (index - (group.length - 1) / 2) * 28;
    });
  });

  function render() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#f8fafc";
    ctx.fillRect(0, 0, width, height);

    edges.forEach((edge) => {
      const sourceNode = byId.get(edge.source);
      const targetNode = byId.get(edge.target);
      if (!sourceNode || !targetNode) return;
      drawEdge(ctx, edge, sourceNode, targetNode, selected === edge);
    });

    nodes.forEach((node) => {
      const selectedNode = selected === node;
      ctx.fillStyle = selectedNode ? "#176b87" : "#fff7d6";
      ctx.strokeStyle = selectedNode ? "#104f66" : "#d8a700";
      ctx.lineWidth = selectedNode ? 3 : 1.4;
      ctx.beginPath();
      ctx.arc(node._x, node._y, node._radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = "#20242c";
      ctx.font = "12px system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(shortLabel(node.label || node.url), node._x, node._y + node._radius + 14);
    });
  }

  canvas.addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * canvas.width;
    const y = ((event.clientY - rect.top) / rect.height) * canvas.height;
    const node = nodes.find((item) => Math.hypot(item._x - x, item._y - y) <= item._radius + 4);
    if (node) {
      selected = node;
      render();
      details.textContent = JSON.stringify(publicNode(node), null, 2);
      return;
    }
    const edge = edges.find((item) => isPointNearEdge(x, y, item, byId));
    if (edge) {
      selected = edge;
      render();
      details.textContent = JSON.stringify(publicEdge(edge, byId), null, 2);
      return;
    }
    selected = null;
    render();
    details.textContent = "{}";
  });

  canvas.addEventListener("mousemove", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * canvas.width;
    const y = ((event.clientY - rect.top) / rect.height) * canvas.height;
    const hoveringNode = nodes.some((item) => Math.hypot(item._x - x, item._y - y) <= item._radius + 4);
    const hoveringEdge = edges.some((item) => isPointNearEdge(x, y, item, byId));
    canvas.style.cursor = hoveringNode || hoveringEdge ? "pointer" : "default";
  });

  render();
}

function simulateLayout(nodes, edges, byId, width, height) {
  const area = width * height;
  const ideal = Math.sqrt(area / Math.max(nodes.length, 1)) * 0.75;
  for (let step = 0; step < 220; step += 1) {
    nodes.forEach((node) => {
      node._vx *= 0.82;
      node._vy *= 0.82;
    });

    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const a = nodes[i];
        const b = nodes[j];
        const dx = a._x - b._x || 0.01;
        const dy = a._y - b._y || 0.01;
        const distance = Math.max(1, Math.hypot(dx, dy));
        const force = (ideal * ideal) / distance;
        const fx = (dx / distance) * force * 0.015;
        const fy = (dy / distance) * force * 0.015;
        a._vx += fx;
        a._vy += fy;
        b._vx -= fx;
        b._vy -= fy;
      }
    }

    edges.forEach((edge) => {
      const source = byId.get(edge.source);
      const target = byId.get(edge.target);
      if (!source || !target) return;
      const dx = target._x - source._x;
      const dy = target._y - source._y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const force = (distance - ideal * 0.95) * 0.018;
      const fx = (dx / distance) * force;
      const fy = (dy / distance) * force;
      source._vx += fx;
      source._vy += fy;
      target._vx -= fx;
      target._vy -= fy;
    });

    nodes.forEach((node) => {
      node._vx += (width / 2 - node._x) * 0.002;
      node._vy += (height / 2 - node._y) * 0.002;
      node._x = clamp(node._x + node._vx, 70, width - 70);
      node._y = clamp(node._y + node._vy, 70, height - 80);
    });
  }
}

function drawEdge(ctx, edge, source, target, selected) {
  const curve = edgeCurve(edge, source, target);
  ctx.strokeStyle = selected ? "#176b87" : "#94a3b8";
  ctx.fillStyle = selected ? "#176b87" : "#94a3b8";
  ctx.lineWidth = selected ? 2.8 : 1.4;
  ctx.beginPath();
  ctx.moveTo(curve.start.x, curve.start.y);
  ctx.quadraticCurveTo(curve.control.x, curve.control.y, curve.end.x, curve.end.y);
  ctx.stroke();

  drawArrow(ctx, curve.control, curve.end, selected);

  const label = shortLabel(edge.label || edge.action || "");
  if (label) {
    const mid = quadraticPoint(curve.start, curve.control, curve.end, 0.5);
    ctx.font = "11px system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillStyle = selected ? "#104f66" : "#475569";
    ctx.fillText(label, mid.x, mid.y - 6);
  }
}

function drawArrow(ctx, from, to, selected) {
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  const size = selected ? 10 : 8;
  ctx.beginPath();
  ctx.moveTo(to.x, to.y);
  ctx.lineTo(to.x - Math.cos(angle - 0.45) * size, to.y - Math.sin(angle - 0.45) * size);
  ctx.lineTo(to.x - Math.cos(angle + 0.45) * size, to.y - Math.sin(angle + 0.45) * size);
  ctx.closePath();
  ctx.fill();
}

function edgeCurve(edge, source, target) {
  if (source.id === target.id) {
    const radius = source._radius;
    return {
      start: { x: source._x + radius * 0.72, y: source._y - radius * 0.72 },
      control: {
        x: source._x + Number(edge._offset || 0),
        y: source._y - radius * 3.4 - Math.abs(Number(edge._offset || 0)),
      },
      end: { x: source._x - radius * 0.72, y: source._y - radius * 0.72 },
    };
  }
  const dx = target._x - source._x;
  const dy = target._y - source._y;
  const distance = Math.max(1, Math.hypot(dx, dy));
  const nx = -dy / distance;
  const ny = dx / distance;
  const offset = Number(edge._offset || 0);
  const start = {
    x: source._x + (dx / distance) * source._radius,
    y: source._y + (dy / distance) * source._radius,
  };
  const end = {
    x: target._x - (dx / distance) * target._radius,
    y: target._y - (dy / distance) * target._radius,
  };
  const control = {
    x: (source._x + target._x) / 2 + nx * offset,
    y: (source._y + target._y) / 2 + ny * offset,
  };
  return { start, control, end };
}

function isPointNearEdge(x, y, edge, byId) {
  const source = byId.get(edge.source);
  const target = byId.get(edge.target);
  if (!source || !target) return false;
  const curve = edgeCurve(edge, source, target);
  let previous = curve.start;
  for (let index = 1; index <= 18; index += 1) {
    const point = quadraticPoint(curve.start, curve.control, curve.end, index / 18);
    if (distanceToSegment(x, y, previous, point) <= 8) return true;
    previous = point;
  }
  return false;
}

function quadraticPoint(start, control, end, t) {
  const inverse = 1 - t;
  return {
    x: inverse * inverse * start.x + 2 * inverse * t * control.x + t * t * end.x,
    y: inverse * inverse * start.y + 2 * inverse * t * control.y + t * t * end.y,
  };
}

function distanceToSegment(x, y, start, end) {
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const length = dx * dx + dy * dy;
  const t = length ? clamp(((x - start.x) * dx + (y - start.y) * dy) / length, 0, 1) : 0;
  const px = start.x + t * dx;
  const py = start.y + t * dy;
  return Math.hypot(x - px, y - py);
}

function publicNode(node) {
  const { _x, _y, _vx, _vy, _radius, ...publicData } = node;
  return publicData;
}

function publicEdge(edge, byId) {
  const { _offset, ...publicData } = edge;
  return {
    ...publicData,
    source_label: byId.get(edge.source)?.label || edge.source,
    target_label: byId.get(edge.target)?.label || edge.target,
  };
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function shortLabel(value) {
  const text = String(value || "").replace(/\s+/g, " ").trim();
  if (text.length <= 22) return text;
  return text.slice(0, 21) + "...";
}

drawGraph();
