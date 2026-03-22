const API_BASE = "/api";
const ASSETS_BASE = "";

const translations = {
  "繁體中文": {
    "title": "AI Tarot <span class=\"divider\">&</span> I-Ching",
    "subtitle": "探索潛意識的古老智慧引導",
    "tab_tarot": "🔮 塔羅占卜",
    "tab_iching": "☯️ 易經卜卦",
    "tab_zhuge": "🎋 諸葛神算",
    "tab_daliuren": "🌌 大六壬",
    "tab_history": "📜 歷史紀錄",
    "tarot_heading": "塔羅占卜",
    "label_spread": "選擇牌陣",
    "loading_spreads": "載入中...",
    "label_question": "你的問題（選填）",
    "placeholder_question": "請在心中默念問題，或寫下來由古老智慧幫您解讀...",
    "btn_draw": "抽取塔羅牌",
    "iching_heading": "易經卜卦",
    "label_question_req": "你的問題（必填）",
    "btn_cast": "擲筊卜卦",
    "zhuge_heading": "諸葛神算",
    "btn_draw_zhuge": "抽籤",
    "daliuren_heading": "大六壬",
    "btn_cast_daliuren": "起課",
    "loader_text": "神祕力量正在運作中...",
    "result_title": "結果",
    "ai_interpret_title": "AI 專屬解讀",
    "audio_label": "語音解讀：",
    "footer_text": "&copy; 2026 AI Tarot & I-Ching. Powered by FastAPI & Vite."
  },
  "简体中文": {
    "title": "AI Tarot <span class=\"divider\">&</span> I-Ching",
    "subtitle": "探索潜意识的古老智慧引导",
    "tab_tarot": "🔮 塔罗占卜",
    "tab_iching": "☯️ 易经卜卦",
    "tab_zhuge": "🎋 诸葛神算",
    "tab_daliuren": "🌌 大六壬",
    "tab_history": "📜 历史纪录",
    "tarot_heading": "塔罗占卜",
    "label_spread": "选择牌阵",
    "loading_spreads": "载入中...",
    "label_question": "你的问题（选填）",
    "placeholder_question": "请在心中默念问题，或写下来由古老智慧帮您解读...",
    "btn_draw": "抽取塔罗牌",
    "iching_heading": "易经卜卦",
    "label_question_req": "你的问题（必填）",
    "btn_cast": "掷筊卜卦",
    "zhuge_heading": "诸葛神算",
    "btn_draw_zhuge": "抽签",
    "daliuren_heading": "大六壬",
    "btn_cast_daliuren": "起课",
    "loader_text": "神祕力量正在运作中...",
    "result_title": "结果",
    "ai_interpret_title": "AI 专属解读",
    "audio_label": "语音解读：",
    "footer_text": "&copy; 2026 AI Tarot & I-Ching. Powered by FastAPI & Vite."
  },
  "English": {
    "title": "AI Tarot <span class=\"divider\">&</span> I-Ching",
    "subtitle": "Explore the ancient wisdom of your subconscious",
    "tab_tarot": "🔮 Tarot Reading",
    "tab_iching": "☯️ I-Ching Divination",
    "tab_zhuge": "🎋 Zhuge Shensuan",
    "tab_xiaoliuren": "🎲 Xiao Liu Ren",
    "tab_daliuren": "🌌 Da Liu Ren",
    "tab_history": "📜 History Logs",
    "tarot_heading": "Tarot Reading",
    "label_spread": "Select Spread",
    "loading_spreads": "Loading...",
    "label_question": "Your Question (Optional)",
    "placeholder_question": "Silently ask your question, or type it here...",
    "btn_draw": "Draw Tarot Cards",
    "iching_heading": "I-Ching Divination",
    "label_question_req": "Your Question (Required)",
    "btn_cast": "Cast Hexagram",
    "zhuge_heading": "Zhuge Shensuan",
    "btn_draw_zhuge": "Draw Lot",
    "xiaoliuren_heading": "Xiao Liu Ren",
    "btn_cast_xiaoliuren": "Cast Divination",
    "daliuren_heading": "Da Liu Ren",
    "btn_cast_daliuren": "Cast Divination",
    "loader_text": "Mystical forces at work...",
    "result_title": "Results",
    "ai_interpret_title": "AI Interpretation",
    "audio_label": "Audio Reading:",
    "footer_text": "&copy; 2026 AI Tarot & I-Ching. Powered by FastAPI & Vite."
  },
  "日本語": {
    "title": "AI タロット <span class=\"divider\">&</span> 易経",
    "subtitle": "潜在意識の古の知恵を導く",
    "tab_tarot": "🔮 タロット占い",
    "tab_iching": "☯️ 易占い",
    "tab_zhuge": "🎋 諸葛神算",
    "tab_daliuren": "🌌 大六壬",
    "tab_history": "📜 占い履歴",
    "tarot_heading": "タロット占い",
    "label_spread": "スプレッドの選択",
    "loading_spreads": "読み込み中...",
    "label_question": "あなたの質問（任意）",
    "placeholder_question": "心の中で質問を念じるか、ここに入力してください...",
    "btn_draw": "タロットカードを引く",
    "iching_heading": "易占い",
    "label_question_req": "あなたの質問（必須）",
    "btn_cast": "筮竹を振る",
    "zhuge_heading": "諸葛神算",
    "btn_draw_zhuge": "おみくじを引く",
    "daliuren_heading": "大六壬",
    "btn_cast_daliuren": "占う",
    "loader_text": "神秘の力が働いています...",
    "result_title": "結果",
    "ai_interpret_title": "AI 専用リーディング",
    "audio_label": "音声リーディング：",
    "footer_text": "&copy; 2026 AI Tarot & I-Ching. Powered by FastAPI & Vite."
  },
  "Español": {
    "title": "AI Tarot <span class=\"divider\">&</span> I-Ching",
    "subtitle": "Explora la antigua sabiduría de tu subconsciente",
    "tab_tarot": "🔮 Lectura de Tarot",
    "tab_iching": "☯️ Adivinación I-Ching",
    "tab_zhuge": "🎋 Shensuan de Zhuge",
    "tab_daliuren": "🌌 Da Liu Ren",
    "tab_history": "📜 Historial",
    "tarot_heading": "Lectura de Tarot",
    "label_spread": "Selecciona Tirada",
    "loading_spreads": "Cargando...",
    "label_question": "Tu Pregunta (Opcional)",
    "placeholder_question": "Haz tu pregunta, o escríbela aquí...",
    "btn_draw": "Sacar Cartas de Tarot",
    "iching_heading": "Adivinación I-Ching",
    "label_question_req": "Tu Pregunta (Obligatoria)",
    "btn_cast": "Lanzar Hexagrama",
    "zhuge_heading": "Shensuan de Zhuge",
    "btn_draw_zhuge": "Sacar Suerte",
    "daliuren_heading": "Da Liu Ren",
    "btn_cast_daliuren": "Lanzar Adivinación",
    "loader_text": "Fuerzas místicas en acción...",
    "result_title": "Resultados",
    "ai_interpret_title": "Interpretación de IA",
    "audio_label": "Lectura de Audio:",
    "footer_text": "&copy; 2026 AI Tarot & I-Ching. Powered by FastAPI & Vite."
  }
};

const langToCode = {
  "繁體中文": "zh-TW",
  "简体中文": "zh-CN",
  "English": "en-US",
  "日本語": "ja-JP",
  "Español": "es-ES"
};

function updateUI(lang) {
  const dict = translations[lang] || translations["繁體中文"];
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) el.innerHTML = dict[key];
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) el.setAttribute("placeholder", dict[key]);
  });
}


document.addEventListener("DOMContentLoaded", () => {
  // Tabs
  const tabTarot = document.getElementById("tabTarot");
  const tabIChing = document.getElementById("tabIChing");
  const tabZhuge = document.getElementById("tabZhuge");
  const tabXiaoliuren = document.getElementById("tabXiaoliuren");
  const tabDaliuren = document.getElementById("tabDaliuren");
  const tabHistory = document.getElementById("tabHistory");
  
  const tarotPanel = document.getElementById("tarotPanel");
  const ichingPanel = document.getElementById("ichingPanel");
  const zhugePanel = document.getElementById("zhugePanel");
  const xiaoliurenPanel = document.getElementById("xiaoliurenPanel");
  const daliurenPanel = document.getElementById("daliurenPanel");
  const historyPanel = document.getElementById("historyPanel");

  // Input & Buttons
  const drawBtn = document.getElementById("drawBtn");
  const castBtn = document.getElementById("castBtn");
  const drawZhugeBtn = document.getElementById("drawZhugeBtn");
  const castXiaoliurenBtn = document.getElementById("castXiaoliurenBtn");
  const castDaliurenBtn = document.getElementById("castDaliurenBtn");
  
  const spreadSelect = document.getElementById("spreadSelect");
  const spreadDescription = document.getElementById("spreadDescription");
  const questionInput = document.getElementById("questionInput");
  const ichingQuestionInput = document.getElementById("ichingQuestionInput");
  const zhugeQuestionInput = document.getElementById("zhugeQuestionInput");
  const xiaoliurenQuestionInput = document.getElementById("xiaoliurenQuestionInput");
  const daliurenQuestionInput = document.getElementById("daliurenQuestionInput");
  
  const micTarot = document.getElementById("micTarot");
  const micIChing = document.getElementById("micIChing");
  const micZhuge = document.getElementById("micZhuge");
  const micXiaoliuren = document.getElementById("micXiaoliuren");
  const micDaliuren = document.getElementById("micDaliuren");
  const langSelect = document.getElementById("langSelect");

  // Initial UI logic
  if (langSelect) {
      updateUI(langSelect.value);
      langSelect.addEventListener("change", (e) => {
        updateUI(e.target.value);
      });
  }

  // Question Sync & Stash Elements
  const questionStashPanel = document.getElementById("questionStashPanel");
  const stashButtons = [0,1,2,3,4,5].map(i => document.getElementById(`stashBtn-${i}`));
  const clearStashBtn = document.getElementById("clearStashBtn");
  let questionStash = ["", "", "", "", "", ""];

  function syncInputs(val) {
      questionInput.value = val;
      ichingQuestionInput.value = val;
      zhugeQuestionInput.value = val;
      xiaoliurenQuestionInput.value = val;
      daliurenQuestionInput.value = val;
  }

  [questionInput, ichingQuestionInput, zhugeQuestionInput, xiaoliurenQuestionInput, daliurenQuestionInput].forEach(inp => {
      inp.addEventListener('input', (e) => syncInputs(e.target.value));
  });

  function getCurrentActiveQuestion() {
      return questionInput.value.trim();
  }

  function updateStashUI() {
      if (currentUserRole === 'toby' && questionStashPanel) {
          questionStashPanel.style.display = "block";
      }
      stashButtons.forEach((btn, i) => {
          if (!btn) return;
          const txt = questionStash[i];
          btn.innerText = txt ? (txt.length > 5 ? txt.substring(0, 5) + "..." : txt) : "[空]";
          btn.title = txt || "空位";
      });
  }

  function addToStash(q) {
      if (!q) return;
      if (q === getCurrentActiveQuestion()) return;
      if (questionStash.includes(q)) return; // 避免重複
      
      let emptyIdx = questionStash.findIndex(x => x === "");
      if (emptyIdx !== -1) {
          questionStash[emptyIdx] = q;
      } else {
          questionStash.shift();
          questionStash.push(q);
      }
      updateStashUI();
  }

  stashButtons.forEach((btn, i) => {
      if (!btn) return;
      btn.addEventListener("click", () => {
          const txt = questionStash[i];
          if (txt) {
              syncInputs(txt);
          } else {
              // 點擊空的暫存區，自動把從目前輸入框的文字存入
              const currentQ = getCurrentActiveQuestion();
              if (currentQ && !questionStash.includes(currentQ)) {
                  questionStash[i] = currentQ;
                  updateStashUI();
              }
          }
      });
  });

  if (clearStashBtn) {
      clearStashBtn.addEventListener("click", () => {
          questionStash = ["", "", "", "", "", ""];
          updateStashUI();
      });
  }

  // Output Elements
  const loader = document.getElementById("loader");
  const resultArea = document.getElementById("resultArea");
  const cardsGrid = document.getElementById("cardsGrid");
  const hexagramContainer = document.getElementById("hexagramContainer");
  const zhugeContainer = document.getElementById("zhugeContainer");
  const xiaoliurenContainer = document.getElementById("xiaoliurenContainer");
  const daliurenContainer = document.getElementById("daliurenContainer");
  const resultTitle = document.getElementById("resultTitle");
  const interpretationPanel = document.getElementById("interpretationPanel");
  const interpretationText = document.getElementById("interpretationText");
  const audioPlayerContainer = document.getElementById("audioPlayerContainer");
  const audioPlayer = document.getElementById("audioPlayer");
  const historyGrid = document.getElementById("historyGrid");

  // Modal Elements
  const historyModal = document.getElementById("historyModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const modalBody = document.getElementById("modalBody");

  // Close modal logic
  closeModalBtn.addEventListener("click", () => {
    historyModal.classList.add("hidden");
    modalBody.innerHTML = "";
  });
  
  historyModal.addEventListener("click", (e) => {
    if (e.target === historyModal) {
      historyModal.classList.add("hidden");
      modalBody.innerHTML = "";
    }
  });

  let currentMode = "tarot";
  let currentUserRole = null; // 'toby' or 'client'
  let isTobyOnline = false;
  let currentUserName = null;
  let ws = null;
  let guideName = 'toby';

  const loginOverlay = document.getElementById("loginOverlay");
  const usernameInput = document.getElementById("usernameInput");
  const enterMagicBtn = document.getElementById("enterMagicBtn");
  const clientWaitingOverlay = document.getElementById("clientWaitingOverlay");
  const clientWaitText = document.getElementById("clientWaitText");

  // --- Usage Limit Update ---
  async function updateUsageLimit() {
      if (currentUserRole !== 'toby') return;
      try {
          const res = await fetch(`${API_BASE}/system/config`);
          const data = await res.json();
          const usageSpan = document.getElementById("usageLimitSpan");
          const usageText = document.getElementById("usageStatusText");
          if (usageSpan && data.usage_limit !== undefined) {
              usageSpan.innerText = data.usage_limit;
              usageText.style.display = "block";
          }
      } catch (e) {
          console.error("Failed to fetch usage limit", e);
      }
  }

  function connectWebSocket(username) {
      // 判斷當前環境來決定 WS URL 屬性
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host; 
      // 動態抓取當前網域，完整支援 Ngrok 等外部服務
      const wsUrl = `${protocol}//${host}/ws/${encodeURIComponent(username)}`;

      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
          console.log("WebSocket connected as", username);
          loginOverlay.style.display = "none";
          if (currentUserRole === 'client') {
             document.querySelector('.tabs').style.display = 'none'; // 客戶看不到 Tabs
             // 客戶端立即獲得發問權限，無需等待導師
             setupClientQuestionUI('tarot'); 
          } else {
             updateStashUI(); // 導師顯示問題暫存區
          }
      };

      ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          console.log("WS Recevied:", data);

          if (data.type === "error") {
              alert(data.message);
              window.location.reload();
          } else if (data.type === "kicked") {
              alert(data.message);
              window.location.reload();
          } else if (data.type === "client_connected") {
              if (currentUserRole === 'toby') {
                  updateUIWithClient(data.client_name);
              }
          } else if (data.type === "divination_start") {
              // (已移除: 客戶端不再因為導師切換頁籤而跟著閃爍跳轉)
          } else if (data.type === "client_question") {
              // 客戶傳送問題給 Toby
              if (currentUserRole === 'toby') {
                  const incoming = data.question;
                  if (getCurrentActiveQuestion() === "") {
                      syncInputs(incoming); // Auto populate
                  } else if (getCurrentActiveQuestion() !== incoming) {
                      addToStash(incoming); // Auto stash if different
                  }
                  alert("獲得客戶傳送的靈能意念 (問題已送達)！");
              }
          } else if (data.type === "divination_result") {
              // Toby 占卜完成，傳結果給客戶
              if (currentUserRole === 'client') {
                  clientWaitingOverlay.classList.add("hidden");
                  renderSummaryResult(data);
              } else if (currentUserRole === 'toby') {
                  updateUsageLimit();
              }
          } else if (data.type === "toby_status") {
              isTobyOnline = data.is_online;
              if (currentUserRole === 'client') {
                  if (isTobyOnline) {
                      drawBtn.disabled = false; castBtn.disabled = false; drawZhugeBtn.disabled = false; castDaliurenBtn.disabled = false;
                      alert("導師已經上線，您可以開始發送問題了！");
                  } else {
                      drawBtn.disabled = true; castBtn.disabled = true; drawZhugeBtn.disabled = true; castDaliurenBtn.disabled = true;
                      alert("導師目前離線中，系統已暫停發問功能，請等待導師上線。");
                  }
              }
          }
      };

      ws.onclose = () => {
          console.log("WebSocket disconnected");
          if (loginOverlay.style.display === "none") {
             alert("連線已中斷，請確認網路狀態重新整理。");
          }
      };
  }

  function updateUIWithClient(clientName) {
      alert(`客戶 ${clientName} 已連線！`);
      // 可在此處更新左上角顯示 "目前客戶: xxx"
  }

  function setupClientQuestionUI(mode) {
      clearResultContainers();
      const dict = translations[langSelect.value] || translations["繁體中文"];
      
      // 隱藏 Clients 不該看到的 UI (標題與牌陣選擇)
      document.querySelectorAll('.controls h2').forEach(el => el.style.display = 'none');
      document.querySelectorAll('.controls .form-group').forEach(group => {
          const label = group.querySelector('label');
          if (label && !label.innerText.includes('問題')) {
              group.style.display = 'none';
          }
      });

      // 把主要的 "抽牌", "卜卦" 按鈕改成 "送出問題"
      if (mode === 'tarot') {
          drawBtn.innerText = "送出問題給導師";
          drawBtn.disabled = false;
          questionInput.placeholder = dict["placeholder_question"] || "請在心中默念問題，或寫下來由古老智慧幫您解讀...";
      } else if (mode === 'iching') {
          castBtn.innerText = "送出問題給導師";
          castBtn.disabled = false;
          ichingQuestionInput.placeholder = dict["placeholder_question"] || "請在心中默念問題，或寫下來由古老智慧幫您解讀...";
      } else if (mode === 'zhuge') {
          drawZhugeBtn.innerText = "送出問題給導師";
          drawZhugeBtn.disabled = false;
          zhugeQuestionInput.placeholder = dict["placeholder_question"] || "請在心中默念問題，或寫下來由古老智慧幫您解讀...";
      } else if (mode === 'daliuren') {
          castDaliurenBtn.innerText = "送出問題給導師";
          castDaliurenBtn.disabled = false;
          daliurenQuestionInput.placeholder = dict["placeholder_question"] || "請在心中默念問題，或寫下來由古老智慧幫您解讀...";
      }
  }

  function renderSummaryResult(data) {
      clearResultContainers();
      resultTitle.innerText = `✨ 解讀結果 ✨`;
      resultArea.classList.remove("hidden");
      
      if (data.mode === 'tarot') {
          cardsGrid.classList.remove("hidden");
          data.result.cards.forEach((card, index) => {
              const cardOrientation = card.is_reversed ? 'reversed' : '';
              const orientationText = card.is_reversed ? '(逆位)' : '(正位)';
              const delay = index * 0.3;
              const cardHTML = `
                <div class="card-item" style="animation-delay: ${delay}s">
                  <div class="card-image-wrapper">
                    <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${card.image_path.replace('.png', '.jpg')}" alt="${card.name_zh}" onerror="this.src='/vite.svg'">
                  </div>
                  <div class="card-info glass-panel">
                      <div class="card-position">${card.position_name || ("Card " + (index + 1))}</div>
                      <div class="card-name">${card.name_zh} <span style="font-size:0.8rem">${orientationText}</span></div>
                  </div>
                </div>
              `;
              cardsGrid.innerHTML += cardHTML;
          });
      } else if (data.mode === 'iching') {
          hexagramContainer.classList.remove("hidden");
          const res = data.result;
          let linesHtml = '';
          res.lines_binary.forEach((binary, idx) => {
            const isMoving = res.moving_indices.includes(idx);
            const movingClass = isMoving ? 'moving' : '';
            if (binary === 1) {
              linesHtml += `<div class="hex-line yang ${movingClass}"><div class="hex-line-part"></div></div>`;
            } else {
              linesHtml += `<div class="hex-line yin ${movingClass}"><div class="hex-line-part"></div><div class="hex-line-part"></div></div>`;
            }
          });

          hexagramContainer.innerHTML = `
            <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
                <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
                  <h2 style="color: #E8D5B7;">本卦：${res.hexagram_name}</h2>
                  <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${res.hexagram_id}.jpg" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
                  <div style="color: #B8A88A; margin-top: 0.5rem;">${res.upper_trigram}上 ${res.lower_trigram}下</div>
                  <div class="hexagram-lines" style="margin-top:1rem;">${linesHtml}</div>
                </div>
            </div>
          `;
      } else if (data.mode === 'zhuge') {
          zhugeContainer.classList.remove("hidden");
          const res = data.result;
          // 資訊複雜度：streamlit(工程師) > Vite(導師) > Vite(客戶)
          // Vite(客戶) 僅顯示籤詩，Vite(導師) 會額外顯示 interp1, interp2 以及 AI 解讀
          zhugeContainer.innerHTML = `
            <div class="zg-container glass-panel" style="max-width:600px; margin: 0 auto; text-align: center; padding: 2rem;">
                <div class="zg-header" style="color: #FFD700; font-size: 1.5rem; margin-bottom: 1.5rem; font-weight: bold;">
                    🎋 諸葛神算 第 ${res.id} 籤
                </div>
                <div class="zg-poem" style="font-family: 'Noto Serif TC', serif; font-size: 1.25rem; white-space: pre-wrap; line-height: 2; color: #fff; margin-bottom: 2rem;">${res.poem}</div>
                ${currentUserRole === 'toby' ? `
                    ${res.interp1 || res.explanation ? `
                    <div class="zg-explanation-title" style="color: #FFD700; margin-bottom: 0.8rem; font-weight: bold;">白話解讀</div>
                    <div class="zg-explanation" style="font-size: 0.95rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 8px; margin-bottom: 1rem;">${res.interp1 || res.explanation}</div>
                    ` : ''}
                    ${res.interp2 ? `
                    <div class="zg-explanation-title" style="color: #FFD700; margin-bottom: 0.8rem; font-weight: bold;">古典意象</div>
                    <div class="zg-explanation" style="font-size: 0.95rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 8px;">${res.interp2}</div>
                    ` : ''}
                ` : ''}
            </div>
          `;
          
          if (currentUserRole === 'toby' && res.interpretation) {
            interpretationPanel.classList.remove("hidden");
            interpretationText.innerHTML = res.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
            if (res.audio_path) {
              let relPath = res.audio_path.includes("history/audio/") ? "/history/audio/" + res.audio_path.split("history/audio/")[1] : (res.audio_path.startsWith("/") ? res.audio_path : "/" + res.audio_path);
              audioPlayer.src = `${ASSETS_BASE}${relPath}`;
              audioPlayerContainer.classList.remove("hidden");
            }
          }
      } else if (data.mode === 'xiaoliuren') {
          xiaoliurenContainer.classList.remove("hidden");
          const xlrResult = data.result || {};
          const states = xlrResult.small_six_states || data.states || ["", "", ""];
          const numbers = xlrResult.numbers || data.numbers || [0, 0, 0];
          const determination = xlrResult.final_state || data.determination || "";
          const description = xlrResult.details?.description || data.details?.description_zh || "";
          const poetry = xlrResult.details?.poem || data.details?.poetry_zh || "";
          
          xiaoliurenContainer.innerHTML = `
          <div class="xlr-container glass-panel" style="max-width:800px; margin: 0 auto; padding: 1.5rem; text-align: center;">
              <div class="xlr-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,215,0,0.3); padding-bottom: 1rem;">
                 🎲 <b>小六壬起卦完成</b>
              </div>
              
              <div class="xlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">三態解讀</div>
              <div class="xlr-row" style="display:flex; justify-content:space-around; align-items:flex-start; margin-bottom:1rem;">
                  <div class="xlr-item" style="flex:1;">
                      <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">初傳</div>
                      <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[0]}</div>
                      <div style="font-size:0.85rem; color:#aaa;">(${numbers[0]})</div>
                  </div>
                  <div class="xlr-item" style="flex:1;">
                      <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">中傳</div>
                      <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[1]}</div>
                      <div style="font-size:0.85rem; color:#aaa;">(${numbers[1]})</div>
                  </div>
                  <div class="xlr-item" style="flex:1;">
                      <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">終傳</div>
                      <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[2]}</div>
                      <div style="font-size:0.85rem; color:#aaa;">(${numbers[2]})</div>
                  </div>
              </div>
              <div class="xlr-result" style="margin-top:2rem;">
                  <h3 style="color:#FFD700; margin-bottom:1rem;">綜合判定: ${determination}</h3>
                  ${currentUserRole === 'toby' ? `<p style="color:#ddd; margin-bottom:1rem; line-height:1.6;">${description}</p>` : ''}
                  <div style="font-family:'Noto Serif TC', serif; color:#fff; font-size:1.1rem; border:1px solid rgba(255,255,255,0.2); padding:1rem; border-radius:8px; white-space:pre-wrap;">${poetry}</div>
              </div>
          </div>`;
          
          if (currentUserRole === 'toby' && data.interpretation) {
              interpretationPanel.classList.remove("hidden");
              interpretationText.innerHTML = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
              if (data.audio_path) {
                  let relPath = data.audio_path.includes("history/audio/") ? "/history/audio/" + data.audio_path.split("history/audio/")[1] : (data.audio_path.startsWith("/") ? data.audio_path : "/" + data.audio_path);
                  audioPlayer.src = `${ASSETS_BASE}${relPath}`;
                  audioPlayerContainer.classList.remove("hidden");
              }
          }
      } else if (data.mode === 'daliuren') {
          daliurenContainer.classList.remove("hidden");
          const res = data.result;
          let patternStr = Array.isArray(res.pattern) && res.pattern.length > 0 ? res.pattern.join('、') : '無特殊格局';
          let daliurenHtml = `
          <div class="dlr-container glass-panel" style="max-width:800px; margin: 0 auto; padding: 1.5rem; text-align: center;">
              <div class="dlr-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,215,0,0.3); padding-bottom: 1rem;">
                  🌌 <b>時局</b>：${res.date} (${res.jieqi}) &nbsp;|&nbsp; <b>格局</b>：${patternStr}
              </div>
              <div class="dlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">三傳</div>
              <div class="dlr-row">`;
          const scKeys = {"初傳": "初傳", "中傳": "中傳", "末傳": "末傳"};
          for (let k in scKeys) {
              let val = res.san_chuan[k];
              if(val) {
                  let display_val = Array.isArray(val) && val.length > 0 ? val[0] : String(val);
                  let sub_val = Array.isArray(val) && val.length > 1 ? val[1] : "";
                  daliurenHtml += `
                    <div class="dlr-item">
                        <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">${scKeys[k]}</span>
                        <span class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif;">${display_val}</span>
                        <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-top: 0.5rem;">${sub_val}</span>
                    </div>
                  `;
              }
          }
          daliurenHtml += `</div></div>`;
          daliurenContainer.innerHTML = daliurenHtml;
      }
  }

  enterMagicBtn.addEventListener("click", () => {
      const name = usernameInput.value.trim();
      currentUserName = name || "未知客戶";
      if (currentUserName.toLowerCase() === guideName.toLowerCase()) {
          currentUserRole = 'toby';
      } else {
          currentUserRole = 'client';
      }
      connectWebSocket(currentUserName);
      updateUsageLimit();
  });

  let availableSpreads = [];

  // Init - Load Spreads
  async function loadSpreads() {
    try {
      const res = await fetch(`${API_BASE}/tarot/spreads`);
      availableSpreads = await res.json();
      spreadSelect.innerHTML = "";
      availableSpreads.forEach(s => {
        const option = document.createElement("option");
        option.value = s.id;
        option.innerText = `${s.name}`;
        spreadSelect.appendChild(option);
      });
      
      const updateDesc = () => {
        const selected = availableSpreads.find(s => s.id === spreadSelect.value);
        if (selected && spreadDescription) {
            spreadDescription.innerText = `📝 [${selected.card_count}張牌] ${selected.description}`;
        }
      };
      
      spreadSelect.addEventListener("change", updateDesc);
      updateDesc(); // initial load
    } catch (e) {
      console.error(e);
      spreadSelect.innerHTML = `<option value="single">單支牌</option>`;
      if (spreadDescription) spreadDescription.innerText = "";
    }
  }
  loadSpreads();

  // Load system config for BGM
  fetch(`${API_BASE}/system/config`)
    .then(res => res.json())
    .then(data => {
      if (data.guide_name) {
          guideName = data.guide_name;
      }
      
      // Auto-login fallback if multiuser login is disabled (backwards compatibility)
      if (data.enable_multiuser_login !== true) {
          currentUserName = guideName;
          currentUserRole = 'toby';
          loginOverlay.style.display = "none";
          connectWebSocket(currentUserName);
          
          const usageSpan = document.getElementById("usageLimitSpan");
          const usageText = document.getElementById("usageStatusText");
          if (usageSpan && data.usage_limit !== undefined) {
              usageSpan.innerText = data.usage_limit;
              usageText.style.display = "block";
          }
      }
      if (data.language) {
         const optionExists = Array.from(langSelect.options).some(opt => opt.value === data.language);
         if (optionExists) {
             langSelect.value = data.language;
             updateUI(data.language);
         }
      }

      const bgmId = data.bgm_id || 1;
      const audio = new Audio(`${ASSETS_BASE}/assets/music/background${bgmId}.mp3`);
      audio.loop = true;
      audio.volume = 0.3;
      
      const playBGM = () => {
        const playPromise = audio.play();
        if (playPromise !== undefined) {
            playPromise.catch(e => console.log("BGM autoplay blocked until user interacts"));
        }
        document.removeEventListener('click', playBGM);
      };
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {
          playPromise.catch(e => {
            document.addEventListener('click', playBGM);
          });
      }
    })
    .catch(err => console.error("Could not load system config", err));

  // Speech Recognition Setup
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
      micTarot.style.display = "block";
      micIChing.style.display = "block";
      micZhuge.style.display = "block";
      micDaliuren.style.display = "block";
      
      function setupMic(btn, inputEl) {
          let recognizing = false;
          let recognition = new SpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = false;

          recognition.onstart = function() {
              recognizing = true;
              btn.innerText = "🛑";
              inputEl.placeholder = "正在聽取聲音...";
          };

          recognition.onresult = function(event) {
              const transcript = event.results[0][0].transcript;
              inputEl.value += (inputEl.value ? " " : "") + transcript;
          };

          recognition.onerror = function(event) {
              console.error("Speech recognition error", event.error);
              inputEl.placeholder = "語音辨識失敗，請手動輸入...";
          };

          recognition.onend = function() {
              recognizing = false;
              btn.innerText = "🎤";
              inputEl.placeholder = "請在心中默念問題，或寫下來由 AI 幫您解讀...";
          };

          btn.addEventListener("click", () => {
              if (recognizing) {
                  recognition.stop();
              } else {
                  recognition.lang = langToCode[langSelect.value] || 'zh-TW';
                  recognition.start();
              }
          });
      }
      setupMic(micTarot, questionInput);
      setupMic(micIChing, ichingQuestionInput);
      setupMic(micZhuge, zhugeQuestionInput);
      setupMic(micDaliuren, daliurenQuestionInput);
  }

  function hideAllPanels() {
    tarotPanel.classList.add("hidden");
    ichingPanel.classList.add("hidden");
    zhugePanel.classList.add("hidden");
    daliurenPanel.classList.add("hidden");
    xiaoliurenPanel.classList.add("hidden");
    historyPanel.classList.add("hidden");
    resultArea.classList.add("hidden");
  }

  function clearResultContainers() {
    if(cardsGrid) { cardsGrid.innerHTML = ""; cardsGrid.classList.add("hidden"); }
    if(hexagramContainer) { hexagramContainer.innerHTML = ""; hexagramContainer.classList.add("hidden"); }
    if(zhugeContainer) { zhugeContainer.innerHTML = ""; zhugeContainer.classList.add("hidden"); }
    if(xiaoliurenContainer) { xiaoliurenContainer.innerHTML = ""; xiaoliurenContainer.classList.add("hidden"); }
    if(daliurenContainer) { daliurenContainer.innerHTML = ""; daliurenContainer.classList.add("hidden"); }
    interpretationPanel.classList.add("hidden");
    audioPlayerContainer.classList.add("hidden");
    resultArea.classList.add("hidden");
    resultTitle.innerText = "";
  }

  function removeAllTabActive() {
    tabTarot.classList.remove("active");
    tabIChing.classList.remove("active");
    tabZhuge.classList.remove("active");
    tabXiaoliuren.classList.remove("active");
    tabDaliuren.classList.remove("active");
    tabHistory.classList.remove("active");
  }

  // Tab Switch Logic
  tabTarot.addEventListener("click", () => {
    currentMode = "tarot";
    removeAllTabActive();
    tabTarot.classList.add("active");
    hideAllPanels();
    tarotPanel.classList.remove("hidden");
  });

  tabIChing.addEventListener("click", () => {
    currentMode = "iching";
    removeAllTabActive();
    tabIChing.classList.add("active");
    hideAllPanels();
    ichingPanel.classList.remove("hidden");
  });

  tabZhuge.addEventListener("click", () => {
    currentMode = "zhuge";
    removeAllTabActive();
    tabZhuge.classList.add("active");
    hideAllPanels();
    zhugePanel.classList.remove("hidden");
  });

  tabXiaoliuren.addEventListener("click", () => {
    currentMode = "xiaoliuren";
    removeAllTabActive();
    tabXiaoliuren.classList.add("active");
    hideAllPanels();
    xiaoliurenPanel.classList.remove("hidden");
  });

  tabDaliuren.addEventListener("click", () => {
    currentMode = "daliuren";
    removeAllTabActive();
    tabDaliuren.classList.add("active");
    hideAllPanels();
    daliurenPanel.classList.remove("hidden");
  });

  tabHistory.addEventListener("click", () => {
    currentMode = "history";
    removeAllTabActive();
    tabHistory.classList.add("active");
    hideAllPanels();
    historyPanel.classList.remove("hidden");
    loadHistory();
  });

  drawBtn.addEventListener("click", async () => {
    const spreadId = spreadSelect.value;
    const question = questionInput.value.trim();

    if (currentUserRole === 'client') {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: "client_question", mode: "tarot", question: question}));
            clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
            clientWaitingOverlay.classList.remove("hidden");
        }
        return;
    }

    // Reset UI
    clearResultContainers();
    cardsGrid.classList.remove("hidden");
    resultArea.classList.remove("hidden");
    loader.classList.remove("hidden");
    drawBtn.disabled = true;
    drawBtn.innerText = "靈能抽牌中...";

    try {
      const response = await fetch(`${API_BASE}/tarot/draw`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          spread_id: spreadId,
          question: question ? question : null,
          language: langSelect.value
        })
      });

      if (!response.ok) {
        throw new Error("占卜伺服器無回應，請確認 FastAPI 已啟動。");
      }

      const data = await response.json();
      
      // Send result to WebSocket Client
      if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({type: "divination_result", mode: "tarot", result: data}));
      }

      // Render Spread Result
      resultTitle.innerText = `🔮 ${data.spread_name} 🔮`;
      
      data.cards.forEach((card, index) => {
        // Build card HTML
        const cardOrientation = card.is_reversed ? 'reversed' : '';
        const orientationText = card.is_reversed ? '(逆位)' : '(正位)';
        
        // 延遲載入動畫以製造沉浸感
        const delay = index * 0.3;

        const cardHTML = `
          <div class="card-item" style="animation-delay: ${delay}s">
            <div class="card-image-wrapper">
              <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${card.image_path.replace('.png', '.jpg')}" alt="${card.name_zh}" onerror="this.src='/vite.svg'">
            </div>
            <div class="card-info glass-panel">
                <div class="card-position">${card.position_name || `Card ${index + 1}`}</div>
                <div class="card-name">${card.name_zh} <span style="font-size:0.8rem">${orientationText}</span></div>
                <div class="card-meaning">${card.meaning}</div>
            </div>
          </div>
        `;
        cardsGrid.innerHTML += cardHTML;
      });

      // Handle Interpretation
      if (data.interpretation) {
        interpretationPanel.classList.remove("hidden");
        // Convert markdown bold to html bold (simple parsing)
        const formatText = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        interpretationText.innerHTML = formatText;

        if (data.audio_path) {
          let relPath = data.audio_path;
          if (relPath.includes("history/audio/")) {
              relPath = "/history/audio/" + relPath.split("history/audio/")[1];
          } else if (!relPath.startsWith("/")) {
              relPath = "/" + relPath;
          }
          audioPlayer.src = `${ASSETS_BASE}${relPath}`;
          audioPlayerContainer.classList.remove("hidden");
        }
      }

      // Show Results
      loader.classList.add("hidden");
      resultArea.classList.remove("hidden");

    } catch (err) {
      alert("抽牌失敗: " + err.message);
      loader.classList.add("hidden");
    } finally {
      drawBtn.disabled = false;
      drawBtn.innerText = "重新抽取塔羅牌";
    }
  });

  castBtn.addEventListener("click", async () => {
    const question = ichingQuestionInput.value.trim();

    if (currentUserRole === 'client') {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: "client_question", mode: "iching", question: question}));
            clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
            clientWaitingOverlay.classList.remove("hidden");
        }
        return;
    }

    // Reset UI
    clearResultContainers();
    hexagramContainer.classList.remove("hidden");
    resultArea.classList.remove("hidden");
    loader.classList.remove("hidden");
    castBtn.disabled = true;
    castBtn.innerText = "六爻推演中...";

    try {
      const response = await fetch(`${API_BASE}/iching/cast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: question ? question : null,
          language: langSelect.value
        })
      });

      if (!response.ok) {
        throw new Error("占卜伺服器無回應，請確認 FastAPI 已啟動。");
      }

      const data = await response.json();
      
      if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({type: "divination_result", mode: "iching", result: data}));
      }

      // Render I-Ching Result
      resultTitle.innerText = `☯️ 卜卦結果 ☯️`;
      
      let linesHtml = '';
      data.lines_binary.forEach((binary, idx) => {
        const isMoving = data.moving_indices.includes(idx);
        const movingClass = isMoving ? 'moving' : '';
        if (binary === 1) {
          linesHtml += `<div class="hex-line yang ${movingClass}"><div class="hex-line-part"></div></div>`;
        } else {
          linesHtml += `<div class="hex-line yin ${movingClass}"><div class="hex-line-part"></div><div class="hex-line-part"></div></div>`;
        }
      });

      hexagramContainer.innerHTML = `
        <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
            <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
              <h2 style="color: #E8D5B7;">本卦：${data.hexagram_name}</h2>
              <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${data.hexagram_id}.jpg" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
              <div style="color: #B8A88A; margin-top: 0.5rem;">${data.upper_trigram}上 ${data.lower_trigram}下</div>
              <p style="margin-top: 1rem; color: #ccc;">${data.hexagram_description}</p>
              <div class="hexagram-lines" style="margin-top:1rem;">${linesHtml}</div>
            </div>
            ${data.changed_hexagram_id ? `
            <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
              <h2 style="color: #E8D5B7;">之卦：${data.changed_hexagram_name}</h2>
              <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${data.changed_hexagram_id}.jpg" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
              <p style="margin-top: 1rem; color: #ccc;">（動爻變化產生）</p>
            </div>
            ` : ''}
        </div>
      `;

      // Handle Interpretation
      if (data.interpretation) {
        interpretationPanel.classList.remove("hidden");
        const formatText = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        interpretationText.innerHTML = formatText;

        if (data.audio_path) {
          let relPath = data.audio_path;
          if (relPath.includes("history/audio/")) {
              relPath = "/history/audio/" + relPath.split("history/audio/")[1];
          } else if (!relPath.startsWith("/")) {
              relPath = "/" + relPath;
          }
          audioPlayer.src = `${ASSETS_BASE}${relPath}`;
          audioPlayerContainer.classList.remove("hidden");
        }
      }

      loader.classList.add("hidden");
      resultArea.classList.remove("hidden");

    } catch (err) {
      alert("卜卦失敗: " + err.message);
      loader.classList.add("hidden");
    } finally {
      castBtn.disabled = false;
      const dict = translations[langSelect.value] || translations["繁體中文"];
      castBtn.innerText = dict["btn_cast"] || "擲筊卜卦";
    }
  });

  drawZhugeBtn.addEventListener("click", async () => {
    const question = zhugeQuestionInput.value.trim();

    if (currentUserRole === 'client') {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: "client_question", mode: "zhuge", question: question}));
            clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
            clientWaitingOverlay.classList.remove("hidden");
        }
        return;
    }

    // Reset UI
    hideAllPanels(); // Hides the main panels if somehow shown
    clearResultContainers();
    zhugeContainer.classList.remove("hidden");
    resultArea.classList.remove("hidden");
    loader.classList.remove("hidden");
    drawZhugeBtn.disabled = true;
    drawZhugeBtn.innerText = "神算啟動中...";

    try {
      const response = await fetch(`${API_BASE}/zhuge/draw`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: question ? question : null,
          language: langSelect.value
        })
      });

      if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

      const data = await response.json();
      
      if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({type: "divination_result", mode: "zhuge", result: data}));
      }

      resultTitle.innerText = `🎋 諸葛神算 🎋`;
      
      // 資訊複雜度：streamlit(工程師) > Vite(導師) > Vite(客戶)
      // Vite(客戶) 僅顯示籤詩，Vite(導師) 會額外顯示 interp1, interp2 以及 AI 解讀
      zhugeContainer.innerHTML = `
        <div class="zg-container glass-panel" style="max-width:600px; margin: 0 auto; text-align: center; padding: 2rem;">
            <div class="zg-header" style="color: #FFD700; font-size: 1.5rem; margin-bottom: 1.5rem; font-weight: bold;">
                🎋 諸葛神算 第 ${data.id} 籤
            </div>
            <div class="zg-poem" style="font-family: 'Noto Serif TC', serif; font-size: 1.25rem; white-space: pre-wrap; line-height: 2; color: #fff; margin-bottom: 2rem;">${data.poem}</div>
            ${currentUserRole === 'toby' ? `
                ${data.interp1 || data.explanation ? `
                <div class="zg-explanation-title" style="color: #FFD700; margin-bottom: 0.8rem; font-weight: bold;">白話解讀</div>
                <div class="zg-explanation" style="font-size: 0.95rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 8px; margin-bottom: 1rem;">${data.interp1 || data.explanation}</div>
                ` : ''}
                ${data.interp2 ? `
                <div class="zg-explanation-title" style="color: #FFD700; margin-bottom: 0.8rem; font-weight: bold;">古典意象</div>
                <div class="zg-explanation" style="font-size: 0.95rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 8px;">${data.interp2}</div>
                ` : ''}
            ` : ''}
        </div>
      `;

      if (currentUserRole === 'toby' && data.interpretation) {
        interpretationPanel.classList.remove("hidden");
        const formatText = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        interpretationText.innerHTML = formatText;

        if (data.audio_path) {
          let relPath = data.audio_path;
          if (relPath.includes("history/audio/")) {
              relPath = "/history/audio/" + relPath.split("history/audio/")[1];
          } else if (!relPath.startsWith("/")) {
              relPath = "/" + relPath;
          }
          audioPlayer.src = `${ASSETS_BASE}${relPath}`;
          audioPlayerContainer.classList.remove("hidden");
        }
      }

    } catch (err) {
      alert("抽籤失敗: " + err.message);
    } finally {
      loader.classList.add("hidden");
      drawZhugeBtn.disabled = false;
      const dict = translations[langSelect.value] || translations["繁體中文"];
      drawZhugeBtn.innerText = dict["btn_draw_zhuge"] || "抽籤";
    }
  });

  castXiaoliurenBtn.addEventListener("click", async () => {
    const question = xiaoliurenQuestionInput.value.trim();

    if (currentUserRole === 'client') {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: "client_question", mode: "xiaoliuren", question: question}));
            clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
            clientWaitingOverlay.classList.remove("hidden");
        }
        return;
    }

    // Reset UI
    hideAllPanels();
    clearResultContainers();
    xiaoliurenContainer.classList.remove("hidden");
    resultArea.classList.remove("hidden");
    loader.classList.remove("hidden");
    castXiaoliurenBtn.disabled = true;
    castXiaoliurenBtn.innerText = "起卦中...";

    try {
      const response = await fetch(`${API_BASE}/xiaoliuren/draw`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: question ? question : null,
          language: langSelect.value
        })
      });

      if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

      const data = await response.json();
      
      if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({type: "divination_result", mode: "xiaoliuren", result: data}));
      }

      resultTitle.innerText = `🎲 小六壬 🎲`;
      
      const xlrResult = data.result || {};
      const states = xlrResult.small_six_states || data.states || ["", "", ""];
      const numbers = xlrResult.numbers || data.numbers || [0, 0, 0];
      const determination = xlrResult.final_state || data.determination || "";
      const description = xlrResult.details?.description || data.details?.description_zh || "";
      const poetry = xlrResult.details?.poem || data.details?.poetry_zh || "";
      
      xiaoliurenContainer.innerHTML = `
      <div class="xlr-container glass-panel" style="max-width:800px; margin: 0 auto; padding: 1.5rem; text-align: center;">
          <div class="xlr-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,215,0,0.3); padding-bottom: 1rem;">
             🎲 <b>小六壬起卦完成</b>
          </div>
          
          <div class="xlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">三態解讀</div>
          <div class="xlr-row" style="display:flex; justify-content:space-around; align-items:flex-start; margin-bottom:1rem;">
              <div class="xlr-item" style="flex:1;">
                  <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">初傳</div>
                  <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[0]}</div>
                  <div style="font-size:0.85rem; color:#aaa;">(${numbers[0]})</div>
              </div>
              <div class="xlr-item" style="flex:1;">
                  <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">中傳</div>
                  <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[1]}</div>
                  <div style="font-size:0.85rem; color:#aaa;">(${numbers[1]})</div>
              </div>
              <div class="xlr-item" style="flex:1;">
                  <div style="font-size:0.85rem; color:#aaa; margin-bottom:0.5rem;">終傳</div>
                  <div style="font-size:1.5rem; color:#fff; font-weight:bold;">${states[2]}</div>
                  <div style="font-size:0.85rem; color:#aaa;">(${numbers[2]})</div>
              </div>
          </div>
          <div class="xlr-result" style="margin-top:2rem;">
              <h3 style="color:#FFD700; margin-bottom:1rem;">綜合判定: ${determination}</h3>
              <p style="color:#ddd; margin-bottom:1rem; line-height:1.6;">${description}</p>
              <div style="font-family:'Noto Serif TC', serif; color:#fff; font-size:1.1rem; border:1px solid rgba(255,255,255,0.2); padding:1rem; border-radius:8px; white-space:pre-wrap;">${poetry}</div>
          </div>
      </div>`;

      if (data.interpretation) {
        interpretationPanel.classList.remove("hidden");
        const formatText = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        interpretationText.innerHTML = formatText;

        if (data.audio_path) {
          let relPath = data.audio_path;
          if (relPath.includes("history/audio/")) {
              relPath = "/history/audio/" + relPath.split("history/audio/")[1];
          } else if (!relPath.startsWith("/")) {
              relPath = "/" + relPath;
          }
          audioPlayer.src = `${ASSETS_BASE}${relPath}`;
          audioPlayerContainer.classList.remove("hidden");
        }
      }

    } catch (err) {
      alert("起卦失敗: " + err.message);
    } finally {
      loader.classList.add("hidden");
      castXiaoliurenBtn.disabled = false;
      const dict = translations[langSelect.value] || translations["繁體中文"];
      castXiaoliurenBtn.innerText = dict["btn_cast_xiaoliuren"] || "起卦";
    }
  });

  castDaliurenBtn.addEventListener("click", async () => {
    const question = daliurenQuestionInput.value.trim();

    if (currentUserRole === 'client') {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: "client_question", mode: "daliuren", question: question}));
            clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
            clientWaitingOverlay.classList.remove("hidden");
        }
        return;
    }

    // Reset UI
    hideAllPanels();
    clearResultContainers();
    daliurenContainer.classList.remove("hidden");
    resultArea.classList.remove("hidden");
    loader.classList.remove("hidden");
    castDaliurenBtn.disabled = true;
    castDaliurenBtn.innerText = "起課中...";

    try {
      const response = await fetch(`${API_BASE}/daliuren/cast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: question ? question : null,
          language: langSelect.value
        })
      });

      if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

      const data = await response.json();
      
      if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({type: "divination_result", mode: "daliuren", result: data}));
      }

      resultTitle.innerText = `🌌 大六壬 🌌`;
      
      let patternStr = Array.isArray(data.pattern) && data.pattern.length > 0 ? data.pattern.join('、') : '無特殊格局';
      let daliurenHtml = `
      <div class="dlr-container glass-panel" style="max-width:800px; margin: 0 auto; padding: 1.5rem; text-align: center;">
          <div class="dlr-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,215,0,0.3); padding-bottom: 1rem;">
              🌌 <b>時局</b>：${data.date} (${data.jieqi}) &nbsp;|&nbsp; <b>格局</b>：${patternStr}
          </div>
          
          <div class="dlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">三傳</div>
          <div class="dlr-row">
      `;
      const scKeys = {"初傳": "初傳", "中傳": "中傳", "末傳": "末傳"};
      for (let k in scKeys) {
          let val = data.san_chuan[k];
          if(val) {
              let display_val = Array.isArray(val) && val.length > 0 ? val[0] : String(val);
              let sub_val = Array.isArray(val) && val.length > 1 ? val[1] : "";
              daliurenHtml += `
                <div class="dlr-item">
                    <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">${scKeys[k]}</span>
                    <span class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif;">${display_val}</span>
                    <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-top: 0.5rem;">${sub_val}</span>
                </div>
              `;
          }
      }
      daliurenHtml += `</div>
          <div class="dlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">四課</div>
          <div class="dlr-row">
      `;
      const skKeys = {"一課": "第一課", "二課": "第二課", "三課": "第三課", "四課": "第四課"};
      for (let k in skKeys) {
          let val = data.si_ke[k];
          if(val && val.length >= 2) {
              daliurenHtml += `
                <div class="dlr-item">
                    <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">${skKeys[k]}</span>
                    <span class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif; margin-bottom: 0.2rem;">${val[0]}</span>
                    <span class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif;">${val[1]}</span>
                </div>
              `;
          } else if (val) {
              daliurenHtml += `
                <div class="dlr-item">
                    <span class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">${skKeys[k]}</span>
                    <span class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif;">${val}</span>
                </div>
              `;
          }
      }
      daliurenHtml += `</div></div>`;
      
      daliurenContainer.innerHTML = daliurenHtml;

      if (data.interpretation) {
        interpretationPanel.classList.remove("hidden");
        const formatText = data.interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
        interpretationText.innerHTML = formatText;

        if (data.audio_path) {
          let relPath = data.audio_path;
          if (relPath.includes("history/audio/")) {
              relPath = "/history/audio/" + relPath.split("history/audio/")[1];
          } else if (!relPath.startsWith("/")) {
              relPath = "/" + relPath;
          }
          audioPlayer.src = `${ASSETS_BASE}${relPath}`;
          audioPlayerContainer.classList.remove("hidden");
        }
      }

    } catch (err) {
      alert("起課失敗: " + err.message);
    } finally {
      loader.classList.add("hidden");
      castDaliurenBtn.disabled = false;
      const dict = translations[langSelect.value] || translations["繁體中文"];
      castDaliurenBtn.innerText = dict["btn_cast_daliuren"] || "起課";
    }
  });

  tabHistory.addEventListener("click", async () => {
    currentMode = "history";
    removeAllTabActive();
    tabHistory.classList.add("active");
    hideAllPanels();
    historyPanel.classList.remove("hidden");
    
    try {
        const res = await fetch(`${API_BASE}/history/clients`);
        if (res.ok) {
            const clients = await res.json();
            const historyClientFilter = document.getElementById("historyClientFilter");
            if (historyClientFilter) {
                const currentVal = historyClientFilter.value;
                historyClientFilter.innerHTML = `<option value="">全部客戶 (All)</option>`;
                clients.forEach(c => {
                    const opt = document.createElement("option");
                    opt.value = c;
                    opt.innerText = c;
                    historyClientFilter.appendChild(opt);
                });
                if (clients.includes(currentVal)) {
                    historyClientFilter.value = currentVal;
                }
            }
        }
    } catch(e) { console.error("載入歷史客戶選單失敗:", e); }

    loadHistory();
  });

  const historyClientFilter = document.getElementById("historyClientFilter");
  if (historyClientFilter) {
      historyClientFilter.addEventListener("change", loadHistory);
  }

  async function loadHistory() {
    loader.classList.remove("hidden");
    historyGrid.innerHTML = "";
    
    let qs = "";
    const filterEl = document.getElementById("historyClientFilter");
    if (filterEl && filterEl.value) {
        qs = `&client_name=${encodeURIComponent(filterEl.value)}`;
    }
    
    try {
      const res = await fetch(`${API_BASE}/history?limit=30&t=${Date.now()}${qs}`);
      const records = await res.json();
      
      if (records.length === 0) {
        historyGrid.innerHTML = "<p>無歷史紀錄。</p>";
        return;
      }

      records.forEach(r => {
        let title = "📜 紀錄";
        if (r.type === "tarot") title = "🔮 塔羅";
        else if (r.type === "iching") title = "☯️ 易經";
        else if (r.type === "zhuge") title = "🎋 諸葛神算";
        else if (r.type === "xiaoliuren") title = "🎲 小六壬";
        else if (r.type === "daliuren") title = "🌌 大六壬";
        
        let summary = "";
        
        if (r.type === "tarot") {
          const spread = r.result?.spread || r.spread;
          const cards = r.result?.cards || r.cards;
          if (spread && cards) {
            summary = `[${spread.name}] ` + cards.map(c => c.card_name_zh).join(", ");
          }
        } else if (r.type === "iching") {
          const orig = r.result?.original_hexagram || r.original_hexagram;
          const changed = r.result?.changed_hexagram || r.changed_hexagram;
          if (orig) {
            summary = `本卦：${orig}` + (changed ? ` ➔ 之卦：${changed}` : '');
          }
        } else if (r.type === "zhuge") {
          const id = r.result?.id;
          if (id) summary = `第 ${id} 籤`;
        } else if (r.type === "xiaoliuren") {
          const determination = r.result?.final_state || r.result?.determination;
          if (determination) summary = `判定：${determination}`;
        } else if (r.type === "daliuren") {
          const date = r.result?.date;
          if (date) summary = `時局：${date}`;
        }

        const isSuccess = r.ai_interpretation && typeof r.ai_interpretation === 'string' && !r.ai_interpretation.includes("error");
        const statusClass = isSuccess ? "success" : "error";
        const statusText = isSuccess ? "解讀成功" : "解讀失敗 (需修復)";

        const itemDiv = document.createElement("div");
        itemDiv.className = "history-item";
        itemDiv.style.cursor = "pointer";
        itemDiv.innerHTML = `
            <div class="history-header">
              <span class="history-type">${title}</span>
              <span class="history-time">${r.timestamp.split("T")[0]} ${r.time_display}</span>
            </div>
            <div class="history-question">Q: ${r.question ? r.question : "無設定問題"}</div>
            <div class="history-result-summary">${summary}</div>
            <div class="history-status ${statusClass}">${statusText}</div>
        `;
        itemDiv.addEventListener("click", () => showHistoryDetail(r));
        historyGrid.appendChild(itemDiv);
      });
      
    } catch (e) {
      console.error(e);
      historyGrid.innerHTML = "<p>無法載入歷史紀錄。</p>";
    } finally {
      loader.classList.add("hidden");
    }
  }

  function showHistoryDetail(r) {
    let titleText = "📜 紀錄";
    if (r.type === 'tarot') titleText = '🔮 塔羅紀錄';
    else if (r.type === 'iching') titleText = '☯️ 易經紀錄';
    else if (r.type === 'zhuge') titleText = '🎋 諸葛神算紀錄';
    else if (r.type === 'xiaoliuren') titleText = '🎲 小六壬紀錄';
    else if (r.type === 'daliuren') titleText = '🌌 大六壬紀錄';

    let detailHtml = `
      <h2 style="color: var(--primary-color); margin-bottom: 1rem; font-family: var(--font-title); text-align: center;">
        ${titleText}
      </h2>
      <p style="font-style: italic; margin-bottom: 2rem; color: #a78bfa; text-align: center; font-size: 1.2rem;">Q: ${r.question || '無'}</p>
    `;

    if (r.type === 'tarot') {
       const cards = r.result?.cards || r.cards;
       if (cards) {
         detailHtml += `<div class="cards-grid" style="transform: scale(0.85); margin: -1rem 0 1rem 0;">`;
         cards.forEach((card, index) => {
           let isRev = false;
           let cardOrientation = '';
           let orientationText = '(正位)';
           if (card.is_reversed || card.orientation === "逆位") { isRev = true; cardOrientation = "reversed"; orientationText = '(逆位)'; }
           
           let imgPath = card.image_path;

           detailHtml += `
             <div class="card-item">
               <div class="card-image-wrapper">
                 <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${imgPath.replace('.png', '.jpg')}" alt="${card.card_name_zh||card.name_zh}" onerror="this.src='/vite.svg'">
               </div>
               <div class="card-info glass-panel" style="background: rgba(0,0,0,0.5);">
                   <div class="card-position">${card.position_name || card.position || `Card ${index + 1}`}</div>
                   <div class="card-name">${card.card_name_zh||card.name_zh} <span style="font-size:0.8rem">${orientationText}</span></div>
               </div>
             </div>
           `;
         });
         detailHtml += `</div>`;
       }
    } else if (r.type === 'iching') {
       const res = r.result || {};
       const origHex = res.original_hexagram || r.original_hexagram;
       const changedHex = res.changed_hexagram || r.changed_hexagram;
       const origImg = res.original_image_path ? `${ASSETS_BASE}${res.original_image_path.replace('.png', '.jpg')}` : null;
       const changedImg = res.changed_image_path ? `${ASSETS_BASE}${res.changed_image_path.replace('.png', '.jpg')}` : null;
       
       detailHtml += `<div class="iching-history-cards" style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-bottom:2rem;">`;
       if (origImg) {
           detailHtml += `<div style="text-align:center;"><h4 style="color:var(--primary-color);">本卦: ${origHex}</h4><img src="${origImg}" style="max-width:200px; border-radius:10px; margin-top:10px;" onerror="this.src='/vite.svg'"></div>`;
       } else {
           detailHtml += `<div style="text-align:center;"><h4 style="color:var(--primary-color);">本卦: ${origHex}</h4></div>`;
       }
       if (changedHex) {
           if (changedImg) {
               detailHtml += `<div style="text-align:center;"><h4 style="color:var(--primary-color);">之卦: ${changedHex}</h4><img src="${changedImg}" style="max-width:200px; border-radius:10px; margin-top:10px;" onerror="this.src='/vite.svg'"></div>`;
           } else {
               detailHtml += `<div style="text-align:center;"><h4 style="color:var(--primary-color);">之卦: ${changedHex}</h4></div>`;
           }
       }
       detailHtml += `</div>`;
    } else if (r.type === 'zhuge') {
         const res = r.result || {};
         detailHtml += `
            <div class="zg-container glass-panel" style="max-width:100%; text-align: center; margin-bottom: 2rem;">
                <div class="zg-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1rem;">
                    🎋 諸葛神算 第 ${res.id || ''} 籤
                </div>
                <div class="zg-poem" style="font-family: 'Noto Serif TC', serif; font-size: 1.1rem; white-space: pre-wrap; line-height: 2; color: #fff; margin-bottom: 1rem;">${res.poem || ''}</div>
            </div>
         `;
    } else if (r.type === 'daliuren') {
         const res = r.result || {};
         let patternStr = Array.isArray(res.pattern) && res.pattern.length > 0 ? res.pattern.join('、') : '無特殊格局';
         detailHtml += `
            <div class="dlr-container glass-panel" style="max-width:100%; text-align: center; margin-bottom: 2rem;">
                <div class="dlr-header" style="color: #FFD700; font-size: 1rem; margin-bottom: 1rem;">
                    🌌 <b>時局</b>：${res.date || ''} (${res.jieqi || ''}) &nbsp;|&nbsp; <b>格局</b>：${patternStr}
                </div>
                <div class="dlr-row" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
         `;
         const scKeys = {"chu": "初傳", "zhong": "中傳", "mo": "末傳"};
         for (let k in scKeys) {
             let val = (res.san_chuan || {})[k];
             if(val) {
                 let display_val = Array.isArray(val) && val.length > 0 ? val[0] : String(val);
                 detailHtml += `<div style="padding: 0.5rem; background: rgba(255,255,255,0.05); border-radius: 4px;"><span style="color:#aaa;font-size:0.8rem;">${scKeys[k]}</span><br><span style="font-size:1.2rem;color:#fff;">${display_val}</span></div>`;
             }
         }
         detailHtml += `</div></div>`;
    }

    if (r.ai_interpretation) {
      const formatText = r.ai_interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
      detailHtml += `
        <div class="interpretation" style="margin-top: 1rem;">
          <h3>AI 專屬解讀</h3>
          <div style="line-height: 1.8;">${formatText}</div>
        </div>
      `;
    }

    if (r.ai_interpretation_audio_path) {
      let relativePath = r.ai_interpretation_audio_path;
      if (relativePath.includes("history/audio/")) {
         relativePath = "/history/audio/" + relativePath.split("history/audio/")[1];
      }
      detailHtml += `
        <div class="audio-container" style="margin-top: 2rem; display: flex;">
           <p class="audio-label">語音解讀：</p>
           <audio controls src="${ASSETS_BASE}${relativePath}" style="width: 100%;"></audio>
        </div>
      `;
    }

    modalBody.innerHTML = detailHtml;
    historyModal.classList.remove("hidden");
  }

});
