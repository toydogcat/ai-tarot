import { drawTarot, getSpreads } from './tarotEngine.js';
import { castIChing } from './ichingEngine.js';
import { drawZhuge } from './zhugeEngine.js';
import { drawXiaoliuren } from './xiaoliurenEngine.js';
import { castDaliuren } from './daliurenEngine.js';

// Auto-detect serverless environment (e.g. GitHub Pages)
const isGitHubPages = window.location.hostname.endsWith('github.io');
let currentMode = localStorage.getItem('divination_run_mode') || (isGitHubPages ? 'offline' : 'api');

export function getRunMode() {
  return currentMode;
}

export function setRunMode(mode) {
  currentMode = mode;
  localStorage.setItem('divination_run_mode', mode);
}

export function isOffline() {
  return currentMode === 'offline';
}

// Local History Management
const LOCAL_HISTORY_KEY = 'ai_tarot_offline_history';

function getLocalHistory() {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_HISTORY_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function saveLocalHistory(records) {
  localStorage.setItem(LOCAL_HISTORY_KEY, JSON.stringify(records));
}

export function saveLocalRecord(type, question, result) {
  const records = getLocalHistory();
  const newRecord = {
    id: `local_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    type: type,
    question: question || "無問題",
    created_at: new Date().toISOString(),
    result: result,
    ai_interpretation: result.interpretation,
    audio_path: null,
    client_id: "local_user",
    mentor_id: "local_mentor"
  };
  records.unshift(newRecord);
  // Cap history size to 50 items locally
  if (records.length > 50) {
    records.pop();
  }
  saveLocalHistory(records);
  return newRecord;
}

// Unified API Wrapper
export async function fetchSpreads(apiBase) {
  if (isOffline()) {
    return getSpreads();
  }
  const res = await fetch(`${apiBase}/tarot/spreads`);
  if (!res.ok) throw new Error("Failed to fetch spreads");
  return await res.json();
}

export async function drawTarotCard(apiBase, params) {
  if (isOffline()) {
    const result = drawTarot(params);
    if (params.question) {
      saveLocalRecord('tarot', params.question, result);
    }
    return result;
  }

  const response = await fetch(`${apiBase}/tarot/draw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error("HTTP error " + response.status);
  return await response.json();
}

export async function castIChingHexagram(apiBase, params) {
  if (isOffline()) {
    const result = castIChing(params);
    if (params.question) {
      saveLocalRecord('iching', params.question, result);
    }
    return result;
  }

  const response = await fetch(`${apiBase}/iching/cast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error("HTTP error " + response.status);
  return await response.json();
}

export async function drawZhugeLot(apiBase, params) {
  if (isOffline()) {
    const result = drawZhuge(params);
    if (params.question) {
      saveLocalRecord('zhuge', params.question, result);
    }
    return result;
  }

  const response = await fetch(`${apiBase}/zhuge/draw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error("HTTP error " + response.status);
  return await response.json();
}

export async function drawXiaoliurenLesson(apiBase, params) {
  if (isOffline()) {
    const result = drawXiaoliuren(params);
    if (params.question) {
      saveLocalRecord('xiaoliuren', params.question, result);
    }
    return result;
  }

  const response = await fetch(`${apiBase}/xiaoliuren/draw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error("HTTP error " + response.status);
  return await response.json();
}

export async function castDaliurenLesson(apiBase, params) {
  if (isOffline()) {
    const result = castDaliuren(params);
    if (params.question) {
      saveLocalRecord('daliuren', params.question, result);
    }
    return result;
  }

  const response = await fetch(`${apiBase}/daliuren/cast`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params)
  });
  if (!response.ok) throw new Error("HTTP error " + response.status);
  return await response.json();
}

export async function fetchHistory(apiBase, qs) {
  if (isOffline()) {
    return getLocalHistory();
  }
  const res = await fetch(`${apiBase}/history?limit=30&t=${Date.now()}${qs}`);
  if (!res.ok) throw new Error("HTTP error " + res.status);
  return await res.json();
}

export async function fetchClientList(apiBase, mentorIdParam) {
  if (isOffline()) {
    return ["local_user"];
  }
  const res = await fetch(`${apiBase}/history/clients?t=${Date.now()}${mentorIdParam}`);
  if (!res.ok) throw new Error("HTTP error " + res.status);
  return await res.json();
}
