const API_BASE = "/api";
const ASSETS_BASE = "";

const translations = {
  "繁體中文": {
    "title": "AI Tarot <span class=\"divider\">&</span> I-Ching",
    "subtitle": "探索潛意識的古老智慧引導",
    "tab_tarot": "🔮 塔羅占卜",
    "tab_iching": "☯️ 易經卜卦",
    "tab_history": "📜 歷史紀錄",
    "tarot_heading": "塔羅占卜",
    "label_spread": "選擇牌陣",
    "loading_spreads": "載入中...",
    "label_question": "你的問題（選填）",
    "placeholder_question": "請在心中默念問題，或寫下來由 AI 幫您解讀...",
    "btn_draw": "抽取塔羅牌",
    "iching_heading": "易經卜卦",
    "label_question_req": "你的問題（必填）",
    "btn_cast": "擲筊卜卦",
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
    "tab_history": "📜 历史纪录",
    "tarot_heading": "塔罗占卜",
    "label_spread": "选择牌阵",
    "loading_spreads": "载入中...",
    "label_question": "你的问题（选填）",
    "placeholder_question": "请在心中默念问题，或写下来由 AI 帮您解读...",
    "btn_draw": "抽取塔罗牌",
    "iching_heading": "易经卜卦",
    "label_question_req": "你的问题（必填）",
    "btn_cast": "掷筊卜卦",
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
  const tabHistory = document.getElementById("tabHistory");
  const tarotPanel = document.getElementById("tarotPanel");
  const ichingPanel = document.getElementById("ichingPanel");
  const historyPanel = document.getElementById("historyPanel");

  // Input & Buttons
  const drawBtn = document.getElementById("drawBtn");
  const castBtn = document.getElementById("castBtn");
  const spreadSelect = document.getElementById("spreadSelect");
  const spreadDescription = document.getElementById("spreadDescription");
  const questionInput = document.getElementById("questionInput");
  const ichingQuestionInput = document.getElementById("ichingQuestionInput");
  const micTarot = document.getElementById("micTarot");
  const micIChing = document.getElementById("micIChing");
  const langSelect = document.getElementById("langSelect");

  // Initial UI logic
  if (langSelect) {
      updateUI(langSelect.value);
      langSelect.addEventListener("change", (e) => {
        updateUI(e.target.value);
      });
  }

  // Output Elements
  const loader = document.getElementById("loader");
  const resultArea = document.getElementById("resultArea");
  const cardsGrid = document.getElementById("cardsGrid");
  const hexagramContainer = document.getElementById("hexagramContainer");
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
  }

  // Tab Switch Logic
  tabTarot.addEventListener("click", () => {
    currentMode = "tarot";
    tabTarot.classList.add("active");
    tabIChing.classList.remove("active");
    tabHistory.classList.remove("active");
    tarotPanel.classList.remove("hidden");
    ichingPanel.classList.add("hidden");
    historyPanel.classList.add("hidden");
    resultArea.classList.add("hidden");
  });

  tabIChing.addEventListener("click", () => {
    currentMode = "iching";
    tabIChing.classList.add("active");
    tabTarot.classList.remove("active");
    tabHistory.classList.remove("active");
    ichingPanel.classList.remove("hidden");
    tarotPanel.classList.add("hidden");
    historyPanel.classList.add("hidden");
    resultArea.classList.add("hidden");
  });

  tabHistory.addEventListener("click", () => {
    currentMode = "history";
    tabHistory.classList.add("active");
    tabTarot.classList.remove("active");
    tabIChing.classList.remove("active");
    historyPanel.classList.remove("hidden");
    tarotPanel.classList.add("hidden");
    ichingPanel.classList.add("hidden");
    resultArea.classList.add("hidden");
    loadHistory();
  });

  drawBtn.addEventListener("click", async () => {
    const spreadId = spreadSelect.value;
    const question = questionInput.value.trim();

    // Reset UI
    resultArea.classList.add("hidden");
    interpretationPanel.classList.add("hidden");
    audioPlayerContainer.classList.add("hidden");
    cardsGrid.innerHTML = "";
    cardsGrid.classList.remove("hidden");
    hexagramContainer.innerHTML = "";
    hexagramContainer.classList.add("hidden");
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
              <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${card.image_path}" alt="${card.name_zh}" onerror="this.src='/vite.svg'">
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

    // Reset UI
    resultArea.classList.add("hidden");
    interpretationPanel.classList.add("hidden");
    audioPlayerContainer.classList.add("hidden");
    cardsGrid.innerHTML = "";
    cardsGrid.classList.add("hidden");
    hexagramContainer.innerHTML = "";
    hexagramContainer.classList.remove("hidden");
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
              <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${data.hexagram_id}.png" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
              <div style="color: #B8A88A; margin-top: 0.5rem;">${data.upper_trigram}上 ${data.lower_trigram}下</div>
              <p style="margin-top: 1rem; color: #ccc;">${data.hexagram_description}</p>
              <div class="hexagram-lines" style="margin-top:1rem;">${linesHtml}</div>
            </div>
            ${data.changed_hexagram_id ? `
            <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
              <h2 style="color: #E8D5B7;">之卦：${data.changed_hexagram_name}</h2>
              <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${data.changed_hexagram_id}.png" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
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
      castBtn.innerText = "重新卜卦";
    }
  });

  async function loadHistory() {
    loader.classList.remove("hidden");
    historyGrid.innerHTML = "";
    try {
      const res = await fetch(`${API_BASE}/history?limit=30&t=${Date.now()}`);
      const records = await res.json();
      
      if (records.length === 0) {
        historyGrid.innerHTML = "<p>無歷史紀錄。</p>";
        return;
      }

      records.forEach(r => {
        let title = r.type === "tarot" ? "🔮 塔羅" : "☯️ 易經";
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
    let detailHtml = `
      <h2 style="color: var(--primary-color); margin-bottom: 1rem; font-family: var(--font-title); text-align: center;">
        ${r.type === 'tarot' ? '🔮 塔羅紀錄' : '☯️ 易經紀錄'}
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
                 <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${imgPath}" alt="${card.card_name_zh||card.name_zh}" onerror="this.src='/vite.svg'">
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
       const origImg = res.original_image_path ? `${ASSETS_BASE}${res.original_image_path}` : null;
       const changedImg = res.changed_image_path ? `${ASSETS_BASE}${res.changed_image_path}` : null;
       
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
