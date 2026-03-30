const VITE_API_URL = import.meta.env.VITE_API_URL;
// 判斷是否為「同域」存取：如果當前網址跟 API 網址一致，或是在 Tunnel 模式下直接訪問
const IS_SAME_ORIGIN = !VITE_API_URL || VITE_API_URL.includes(window.location.hostname);
const IS_LOCAL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.hostname.startsWith("192.168."));

// 如果是同域訪問（例如直接開 Tunnel 網址），直接用相對路徑 /api
const API_BASE = (IS_SAME_ORIGIN || IS_LOCAL) ? "/api" : `${VITE_API_URL}/api`;
const ASSETS_BASE = (IS_SAME_ORIGIN || IS_LOCAL) ? "" : VITE_API_URL;
const WS_HOST = (IS_SAME_ORIGIN || IS_LOCAL) ? window.location.host : VITE_API_URL.replace(/^https?:\/\//, "");
const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

// --- Ngrok Skip Warning Patch ---
const originalFetch = window.fetch;
window.fetch = async function (url, options = {}) {
    if (typeof url === 'string' && (url.includes('trycloudflare.com') || url.includes('ngrok-free.dev') || url.includes('/api/'))) {
        if (!options.headers) {
            options.headers = {};
        }
        
        if (options.headers instanceof Headers) {
            options.headers.set('ngrok-skip-browser-warning', '69420');
            options.headers.set('cf-skip-browser-warning', 'any');
        } else {
            options.headers['ngrok-skip-browser-warning'] = '69420';
            options.headers['cf-skip-browser-warning'] = 'any';
        }
    }
    return originalFetch(url, options);
};

// --- BGM Control Logic ---
const bgmTracks = [
    { name: "Mystical Zen", file: "/assets/music/background1.mp3" },
    { name: "Celestial Void", file: "/assets/music/background2.mp3" }
];
let currentTrackIdx = 0;
let bgmAudio, bgmToggle, bgmName, volumeSlider;
let isMainClient = true; // For multi-person room role restriction

function initBGM() {
    bgmAudio = document.getElementById("bgmAudio");
    bgmToggle = document.getElementById("bgmToggle");
    bgmName = document.getElementById("bgmName");
    volumeSlider = document.getElementById("volumeSlider");
    const bgmPrev = document.getElementById("bgmPrev");
    const bgmNext = document.getElementById("bgmNext");

    if (!bgmAudio || !bgmToggle) {
        console.warn("[BGM] Elements not found, skipping init.");
        return;
    }

    function loadTrack(idx) {
        const track = bgmTracks[idx];
        bgmAudio.src = track.file;
        bgmName.innerText = track.name;
        console.log(`[BGM] Track loaded: ${track.name}`);
    }

    function toggleBgm() {
        console.log(`[BGM] Toggle clicked. Current state: ${bgmAudio.paused ? 'Paused' : 'Playing'}`);
        if (bgmAudio.paused) {
            bgmAudio.play()
                .then(() => {
                    bgmToggle.innerText = "⏸";
                    console.log("[BGM] Playing started.");
                })
                .catch(err => {
                    console.warn("[BGM] Play failed:", err);
                    alert("請點擊頁面任何地方後再按下播放，以啟動沉浸音效。");
                });
        } else {
            bgmAudio.pause();
            bgmToggle.innerText = "▶️";
            console.log("[BGM] Paused successfully.");
        }
    }

    bgmToggle.addEventListener("click", (e) => {
        e.stopPropagation();
        toggleBgm();
    });

    bgmPrev.addEventListener("click", (e) => {
        e.stopPropagation();
        currentTrackIdx = (currentTrackIdx - 1 + bgmTracks.length) % bgmTracks.length;
        loadTrack(currentTrackIdx);
        bgmAudio.play().then(() => bgmToggle.innerText = "⏸");
    });

    bgmNext.addEventListener("click", (e) => {
        e.stopPropagation();
        currentTrackIdx = (currentTrackIdx + 1) % bgmTracks.length;
        loadTrack(currentTrackIdx);
        bgmAudio.play().then(() => bgmToggle.innerText = "⏸");
    });

    volumeSlider.addEventListener("input", (e) => {
        bgmAudio.volume = e.target.value;
    });

    // Initialize
    loadTrack(0);
    bgmAudio.volume = 0.5;

    // Collapsible Logic
    const toggleBtn = document.getElementById("toggleControlsBtn");
    const container = document.getElementById("systemControls");
    if (toggleBtn && container) {
        toggleBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            container.classList.toggle("collapsed");
            toggleBtn.innerHTML = container.classList.contains("collapsed") ? "🪄" : "✖️";
        });
    }
}
let translations = {};

async function loadTranslations() {
    try {
        const response = await fetch('/i18n.json');
        if (!response.ok) throw new Error('Failed to load i18n.json');
        translations = await response.json();
        console.log("Translations loaded successfully.");

        // Initial UI update once loaded
        const ls = document.getElementById("langSelect");
        if (ls) updateUI(ls.value);
    } catch (error) {
        console.error("I18N Error:", error);
    }
}

loadTranslations();

const langToCode = {
    "繁體中文": "zh-TW",
    "简体中文": "zh-CN",
    "English": "en-US",
    "日本語": "ja-JP",
    "Español": "es-ES",
    "한국어": "ko-KR",
    "Français": "fr-FR",
    "Tiếng Việt": "vi-VN"
};

function updateUI(lang) {
    if (!translations || Object.keys(translations).length === 0) {
        console.warn("Translations not yet loaded. Skipping UI update.");
        return;
    }
    const dict = translations[lang] || translations["繁體中文"];
    const fallbackDict = translations["繁體中文"];

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const val = dict[key] || fallbackDict[key];
        if (val !== undefined) el.innerHTML = val;
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        const val = dict[key] || fallbackDict[key];
        if (val !== undefined) el.setAttribute("placeholder", val);
    });

    document.querySelectorAll("[data-i18n-title]").forEach(el => {
        const key = el.getAttribute("data-i18n-title");
        const val = dict[key] || fallbackDict[key];
        if (val !== undefined) el.setAttribute("title", val);
    });

    // Refresh stateful UI
    if (typeof refreshStatefulUI === "function") refreshStatefulUI();
}

let isAdminMode = false;
let currentUserRole = null; // 'toby' or 'client'
let drawBtn, castBtn, drawZhugeBtn, castXiaoliurenBtn, castDaliurenBtn;
let currentMode = "tarot";
let isTobyOnline = false;
let isWsConnected = false;
let currentUserName = null;
let currentMentorId = null;
let currentAnnouncement = "";
let ws = null;
let guideName = 'toby';

const isMentor = () => {
    return (currentUserRole === 'toby' || (currentMentorId !== null && currentUserRole !== 'client'));
};

function refreshStatefulUI() {
    const lang = document.getElementById("langSelect")?.value || "繁體中文";
    const dict = translations[lang] || translations["繁體中文"];
    const fallbackDict = translations["繁體中文"];

    // Admin Login Toggle
    const toggleAdminText = document.getElementById("toggleAdminText");
    const pathLabelTop = document.getElementById("pathLabelTop");

    if (toggleAdminText) {
        const key = isAdminMode ? "admin_login_toggle_back" : "admin_login_toggle_key";
        toggleAdminText.innerText = dict[key] || fallbackDict[key] || (isAdminMode ? "返回客戶入座" : "使用 Key 登入 (Login with Key)");
    }
    if (pathLabelTop) {
        const key = isAdminMode ? "admin_login_path_label_admin" : "admin_login_path_label_client";
        pathLabelTop.innerText = dict[key] || fallbackDict[key] || (isAdminMode ? "導師登入 (Admin Login)" : "我是客戶 (I am Client)");
        pathLabelTop.style.color = isAdminMode ? "#a78bfa" : "#888";
    }

    // Client Question Buttons (if in client mode)
    if (currentUserRole === 'client') {
        const btnKey = "send_question_btn";
        const btnTxt = dict[btnKey] || fallbackDict[btnKey] || "送出問題給導師";

        if (drawBtn) drawBtn.innerText = btnTxt;
        if (castBtn) castBtn.innerText = btnTxt;
        if (drawZhugeBtn) drawZhugeBtn.innerText = btnTxt;
        if (castXiaoliurenBtn) castXiaoliurenBtn.innerText = btnTxt;
        if (castDaliurenBtn) castDaliurenBtn.innerText = btnTxt;
    }
}


document.addEventListener("DOMContentLoaded", () => {
    // --- Quick Login Helpers ---
    function getSavedAccountsLocal() {
        try {
            return JSON.parse(localStorage.getItem("recent_mentors") || "[]");
        } catch (e) { return []; }
    }

    function saveAccountLocal(mentorId, key) {
        if (!mentorId || !key) return;
        let accounts = getSavedAccountsLocal();
        // Remove if exists to update position
        accounts = accounts.filter(a => a.id !== mentorId);
        accounts.unshift({ id: mentorId, key: key, time: Date.now() });
        // Max 5
        localStorage.setItem("recent_mentors", JSON.stringify(accounts.slice(0, 5)));
        renderQuickLogin();
    }

    function renderQuickLogin() {
        const container = document.getElementById("quickLoginContainer");
        const section = document.getElementById("quickLoginSection");
        if (!container || !section) return;

        const accounts = getSavedAccountsLocal();
        if (accounts.length === 0) {
            section.classList.add("hidden");
            return;
        }

        section.classList.remove("hidden");
        container.innerHTML = "";
        accounts.forEach(acc => {
            const btn = document.createElement("button");
            btn.className = "secondary-btn";
            btn.style.padding = "6px 12px";
            btn.style.fontSize = "0.8rem";
            btn.style.borderRadius = "20px";
            btn.style.border = "1px solid rgba(167, 139, 250, 0.3)";
            btn.innerHTML = `👤 ${acc.id}`;
            btn.onclick = () => {
                document.getElementById("adminMentorInput").value = acc.id;
                document.getElementById("adminKeyInput").value = acc.key;
                isAdminMode = true; // Ensure mode is set
                document.getElementById("enterMagicBtn").click();
            };
            container.appendChild(btn);
        });
    }

    // Helper to handle successful mentor login
    async function handleLoginSuccess(mentorId, role, manualKey = null) {
        currentMentorId = mentorId;
        currentUserRole = role;

        if (manualKey) {
            saveAccountLocal(mentorId, manualKey);
        }

        const loginOverlay = document.getElementById("loginOverlay");
        if (loginOverlay) loginOverlay.classList.add("hidden");

        // Update Welcome Message
        const welcomeArea = document.getElementById("welcomeMentor");
        const nameSpan = document.getElementById("welcomeMentorName");
        if (welcomeArea && nameSpan) {
            nameSpan.innerText = mentorId;
            welcomeArea.style.display = "block";
        }
        // Load Room Settings for Mentor
        if (isMentor()) {
            await initRoomSettings();
        }

        connectWebSocket(mentorId, role);

        // 導師模式：顯示控制面板，隱藏客戶等待區
        const clientWaitingOverlay = document.getElementById("clientWaitingOverlay");
        if (clientWaitingOverlay) clientWaitingOverlay.classList.add("hidden");

        if (document.getElementById("questionStashPanel")) document.getElementById("questionStashPanel").style.display = "block";
        if (document.getElementById("usageStatusText")) document.getElementById("usageStatusText").style.display = "block";
        const socialBtn = document.getElementById("socialToggleBtn");
        if (socialBtn) socialBtn.classList.remove("hidden");

        console.log(`[Auth] ${role} ${mentorId} logged in successfully.`);
    }

    async function initRoomSettings() {
        const panel = document.getElementById("roomSettingsPanel");
        if (!panel) return;

        try {
            const res = await fetch(`${API_BASE}/auth/me?mentor_id=${encodeURIComponent(currentMentorId)}`);
            const data = await res.json();

            if (res.ok) {
                panel.classList.remove("hidden");

                const levelBadge = document.getElementById("roomLevelBadge");
                const aiToggle = document.getElementById("aiEnabledToggle");
                const maxGuestsInp = document.getElementById("maxGuestsInput");
                const aiNote = document.getElementById("aiRestrictionNote");
                const guestNote = document.getElementById("guestRestrictionNote");

                levelBadge.innerText = `LEVEL: ${data.room_level.toUpperCase()}`;
                aiToggle.checked = data.ai_enabled;
                maxGuestsInp.value = data.max_clients;

                const announcementInp = document.getElementById("announcementInput");
                if (announcementInp) {
                    announcementInp.value = data.announcement || "";
                    announcementInp.onchange = () => updateRoomSettings();
                }

                const shareBtn = document.getElementById("copyShareLinkBtn");
                if (shareBtn) {
                    shareBtn.onclick = () => copyShareLink();
                }

                const usageSpan = document.getElementById("usageLimitSpan");
                if (usageSpan && data.usage_limit !== undefined) {
                    usageSpan.innerText = data.usage_limit;
                }

                // Restrict based on level
                if (data.room_level === 'single' && data.enable_multiuser) {
                    aiToggle.disabled = true;
                    aiNote.innerText = "(Single Room - AI Always On)";
                    maxGuestsInp.disabled = true;
                    guestNote.innerText = "(Fixed to 0)";
                    panel.querySelectorAll('.setting-item').forEach(el => el.classList.add('disabled'));
                } else if (data.room_level === 'double') {
                    maxGuestsInp.disabled = true;
                    guestNote.innerText = "(Fixed to 1)";
                    // Double can toggle AI
                } else if (data.room_level === 'multi') {
                    // Full control
                }

                // Event Listeners
                aiToggle.onchange = () => updateRoomSettings();
                maxGuestsInp.onchange = () => updateRoomSettings();
            }
        } catch (e) {
            console.error("Failed to init room settings", e);
        }
    }

    async function updateRoomSettings() {
        const aiToggle = document.getElementById("aiEnabledToggle");
        const maxGuestsInp = document.getElementById("maxGuestsInput");
        const statusEl = document.getElementById("settingsUpdateStatus");

        statusEl.innerText = "正在同步設定...";
        statusEl.style.color = "#E8D5B7";

        try {
            const res = await fetch(`${API_BASE}/auth/settings`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId,
                    ai_enabled: aiToggle.checked,
                    max_clients: parseInt(maxGuestsInp.value),
                    announcement: document.getElementById("announcementInput")?.value || ""
                })
            });

            if (res.ok) {
                statusEl.innerText = "✅ 設定已更新";
                statusEl.style.color = "#10b981";
                setTimeout(() => { if (statusEl.innerText === "✅ 設定已更新") statusEl.innerText = ""; }, 3000);
            } else {
                statusEl.innerText = "❌ 更新失敗";
                statusEl.style.color = "#ef4444";
            }
        } catch (e) {
            statusEl.innerText = "❌ 網路錯誤";
            statusEl.style.color = "#ef4444";
        }
    }
    // Firebase Google Auth Callback
    window.loginWithGoogleFirebase = async () => {
        try {
            console.log("[Auth] Starting Firebase Google Login...");
            const provider = new firebase.auth.GoogleAuthProvider();
            const result = await firebase.auth().signInWithPopup(provider);
            const user = result.user;
            const idToken = await user.getIdToken();

            console.log("[Auth] Firebase ID Token obtained, verifying with backend...");
            const r = await fetch(`${API_BASE}/auth/google_login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ credential: idToken })
            });

            const data = await r.json();

            // Task 2: Handle restriction if backend returns 403 (blocked admin/guest)
            if (r.status === 403) {
                alert(data.detail || "此帳號受限 (Access Restricted)");
                return;
            }

            if (r.ok && (data.role === "toby" || data.role === "admin")) {
                handleLoginSuccess(data.mentor_id, data.role);
            } else if (r.status === 404 && data.detail === "NOT_REGISTERED") {
                // New user - show signup modal Step 2
                const emailInfo = document.getElementById("signupVerifiedEmail");
                const step1 = document.getElementById("signupStep1");
                const step2 = document.getElementById("signupStep2");
                const modal = document.getElementById("signupModal");
                
                if (emailInfo && step1 && step2 && modal) {
                    emailInfo.innerText = user.email || "";
                    window._currentFirebaseToken = idToken; // Store for final submission
                    step1.classList.add("hidden");
                    step2.classList.remove("hidden");
                    modal.classList.remove("hidden");
                    alert("Firebase 驗證成功！您目前的 Google 帳號尚未註冊。");
                }
            } else {
                alert("Firebase 登入失敗：" + (data.detail || "未知錯誤"));
            }
        } catch (e) {
            console.error("Firebase Auth Error:", e);
            if (e.code !== "auth/popup-closed-by-user") {
                alert("Google 驗證連線異常: " + e.message);
            }
        }
    };
    initBGM();
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
    drawBtn = document.getElementById("drawBtn");
    castBtn = document.getElementById("castBtn");
    drawZhugeBtn = document.getElementById("drawZhugeBtn");
    castXiaoliurenBtn = document.getElementById("castXiaoliurenBtn");
    castDaliurenBtn = document.getElementById("castDaliurenBtn");

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
    langSelect.addEventListener("change", (e) => {
        updateUI(e.target.value);
    });
    // Initial update
    updateUI(langSelect.value);

    // SSO & Registration Elements
    const signupModal = document.getElementById("signupModal");
    const showSignupBtn = document.getElementById("showSignupBtn");
    const closeSignupBtn = document.getElementById("closeSignupBtn");
    const submitSignupBtn = document.getElementById("submitSignupBtn");
    const signupEmailInput = document.getElementById("signupEmailInput");
    const signupIdInput = document.getElementById("signupIdInput");

    // Client Identification Elements
    const targetMentorInput = document.getElementById("targetMentorInput");
    const clientNameInput = document.getElementById("clientNameInput");
    const enterMagicBtn = document.getElementById("enterMagicBtn");

    // 管理員登入切換邏輯
    const toggleAdminLogin = document.getElementById("toggleAdminLogin");
    const adminLoginFields = document.getElementById("adminLoginFields");

    if (toggleAdminLogin) {
        const toggleAdminIcon = document.getElementById("toggleAdminIcon");

        toggleAdminLogin.onclick = (e) => {
            e.preventDefault();
            isAdminMode = !isAdminMode;
            adminLoginFields.classList.toggle("hidden", !isAdminMode);

            if (toggleAdminIcon) toggleAdminIcon.innerText = isAdminMode ? "⬅️" : "🔑";
            refreshStatefulUI();

            // 若進入管理員模式，暫時隱藏客戶輸入區
            const clientInputs = document.querySelector(".client-inputs");
            if (clientInputs) clientInputs.classList.toggle("hidden", isAdminMode);
        };
    }

    // 密碼顯示/隱藏切換
    const togglePasswordBtn = document.getElementById("togglePasswordBtn");
    const adminKeyInput = document.getElementById("adminKeyInput");
    if (togglePasswordBtn && adminKeyInput) {
        togglePasswordBtn.onclick = () => {
            const isPassword = adminKeyInput.type === "password";
            adminKeyInput.type = isPassword ? "text" : "password";
            togglePasswordBtn.innerText = isPassword ? "🔓" : "👁️";
            togglePasswordBtn.style.color = isPassword ? "#d4af37" : "rgba(255,255,255,0.4)";
        };
    }

    if (enterMagicBtn) {
        enterMagicBtn.onclick = async () => {
            if (isAdminMode) {
                const mId = document.getElementById("adminMentorInput").value.trim();
                const key = document.getElementById("adminKeyInput").value.trim();
                if (!mId || !key) return alert("管理員 ID 與密鑰不可為空");

                try {
                    const r = await fetch(`${API_BASE}/auth/login`, {
                        method: "POST", headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ mentor: mId, key: key })
                    });
                    const data = await r.json();
                    if (r.ok && data.role === "toby") {
                        handleLoginSuccess(data.mentor_id, "toby", key);
                    } else {
                        alert("登入失敗：" + (data.detail || "帳號或密鑰錯誤"));
                    }
                } catch (e) {
                    console.error("Login Error:", e);
                    alert(`登入介面連線異常 (URL: ${API_BASE}): ` + e.message);
                }
            } else {
                // 客戶路徑
                const mentorId = targetMentorInput.value.trim();
                let clientName = clientNameInput.value.trim();

                if (!mentorId) return alert("請填寫欲諮詢的導師 ID (Mentor ID is required)");
                if (!clientName) clientName = `緣人-${Math.floor(Math.random() * 900) + 100}`;

                currentUserName = clientName;
                currentUserRole = 'client';
                loginOverlay.classList.add("hidden");
                clientWaitingOverlay.classList.remove("hidden"); // 顯示水晶球
                console.log(`Entering as Client: ${clientName} for Mentor: ${mentorId}`);

                connectWebSocket(mentorId, clientName);
            }
        };
    }

    if (showSignupBtn) {
        showSignupBtn.onclick = (e) => { 
            e.preventDefault(); 
            document.getElementById("signupStep1").classList.remove("hidden");
            document.getElementById("signupStep2").classList.add("hidden");
            signupModal.classList.remove("hidden"); 
        };
    }

    const googleSignupVerifyBtn = document.getElementById("googleSignupVerifyBtn");
    if (googleSignupVerifyBtn) {
        googleSignupVerifyBtn.onclick = () => window.loginWithGoogleFirebase();
    }

    if (closeSignupBtn) {
        closeSignupBtn.onclick = () => signupModal.classList.add("hidden");
    }
    if (submitSignupBtn) {
        submitSignupBtn.onclick = async () => {
            const mentor_id = signupIdInput.value.trim();
            const idToken = window._currentFirebaseToken;

            if (!idToken) return alert("請先完成 Google 驗證");
            if (!mentor_id) return alert("請填寫您想要的 導師 ID");

            submitSignupBtn.disabled = true;
            submitSignupBtn.innerText = "提交中...";
            try {
                const r = await fetch(`${API_BASE}/auth/register`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ credential: idToken, mentor_id: mentor_id })
                });
                const data = await r.json();
                if (r.ok) {
                    alert("申請已提交！驗證通過後管理員將進行審核。");
                    signupModal.classList.add("hidden");
                } else {
                    alert(data.detail || "申請失敗");
                }
            } catch (e) { alert("網路連線錯誤"); }
            finally {
                submitSignupBtn.disabled = false;
                submitSignupBtn.innerText = "提交申請(Submit)";
            }
        };
    }

    // Question Sync & Stash Elements
    const questionStashPanel = document.getElementById("questionStashPanel");
    const stashButtons = [0, 1, 2, 3, 4, 5].map(i => document.getElementById(`stashBtn-${i}`));
    const clearStashBtn = document.getElementById("clearStashBtn");
    let questionStash = ["", "", "", "", "", ""];

    function syncInputs(val) {
        questionInput.value = val;
        ichingQuestionInput.value = val;
        zhugeQuestionInput.value = val;
        xiaoliurenQuestionInput.value = val;
        daliurenQuestionInput.value = val;
    }

    function formatZhugePoem(poem) {
        if (!poem) return "(原始籤文修復中...)";
        const p = poem.replace(/。/g, "，"); // Standardize
        const parts = p.split("，").map(s => s.trim()).filter(s => s.length > 0);

        if (parts.length >= 4) {
            return `<span class="zg-poem-line">${parts[0]}，${parts[1]}</span>
                  <span class="zg-poem-line">${parts[2]}，${parts[3]}</span>
                  <div class="zg-seal">諸葛<br>神算</div>`;
        } else if (parts.length >= 2) {
            return `<span class="zg-poem-line">${parts[0]}</span>
                  <span class="zg-poem-line">${parts[1]}</span>
                  <div class="zg-seal">諸葛<br>神算</div>`;
        }
        return `<span class="zg-poem-line">${poem}</span><div class="zg-seal">諸葛<br>神算</div>`;
    }

    [questionInput, ichingQuestionInput, zhugeQuestionInput, xiaoliurenQuestionInput, daliurenQuestionInput].forEach(inp => {
        inp.addEventListener('input', (e) => syncInputs(e.target.value));
    });

    function getCurrentActiveQuestion() {
        return questionInput.value.trim();
    }

    function updateStashUI() {
        if (isMentor() && questionStashPanel) {
            questionStashPanel.style.display = "block";
        }
        if (!stashContainer) return;
        stashContainer.innerHTML = ""; // Clear

        const colorsMap = {
            "red": "#ff4b2b",
            "orange": "#ff9068",
            "yellow": "#fff94c",
            "green": "#4ef037",
            "blue": "#0080ff",
            "indigo": "#4b0082",
            "purple": "#9d50bb",
            "gold": "#d4af37"
        };

        questionStash.forEach((item, i) => {
            const isOccupied = !!(typeof item === 'object' ? item.q : item);
            const qText = typeof item === 'object' ? item.q : item;
            const qColor = typeof item === 'object' ? (item.color || "gold") : "gold";
            const glowColor = colorsMap[qColor] || colorsMap.gold;

            const card = document.createElement("div");
            card.className = `seeker-card ${isOccupied ? 'occupied' : ''}`;
            if (isOccupied) {
                card.style.setProperty('--card-glow', glowColor);
                card.innerHTML = `
                  <div class="seeker-status-dot"></div>
                  <div class="seeker-name">${qText.length > 8 ? qText.substring(0, 8) + "..." : qText}</div>
                  <div style="font-size:0.6rem; opacity:0.5; margin-top:2px;">CONNECTED</div>
              `;
                card.title = qText;
            } else {
                card.innerHTML = `<span style="opacity:0.3; font-size:0.8rem;">[ EMPTY ]</span>`;
            }

            card.addEventListener("click", () => {
                if (isOccupied) {
                    syncInputs(qText);
                } else {
                    const currentQ = getCurrentActiveQuestion();
                    if (currentQ) {
                        const exists = questionStash.some(x => (typeof x === 'object' ? x.q : x) === currentQ);
                        if (!exists) {
                            questionStash[i] = { q: currentQ, color: "gold" };
                            updateStashUI();
                        }
                    }
                }
            });
            stashContainer.appendChild(card);
        });
    }

    function addToStash(q, color = "gold") {
        if (!q) return;
        if (q === getCurrentActiveQuestion()) return;
        // 檢查是否已存在
        const exists = questionStash.some(x => (typeof x === 'object' ? x.q : x) === q);
        if (exists) return;

        let emptyIdx = questionStash.findIndex(x => x === "" || (typeof x === 'object' && !x.q));
        if (emptyIdx !== -1) {
            questionStash[emptyIdx] = { q: q, color: color };
        } else {
            questionStash.shift();
            questionStash.push({ q: q, color: color });
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

    currentMode = "tarot";
    currentUserRole = null; // 'toby' or 'client'
    isTobyOnline = false;
    isWsConnected = false;
    currentUserName = null;
    currentMentorId = null;
    ws = null;
    guideName = 'toby';

    const loginOverlay = document.getElementById("loginOverlay");
    const usernameInput = document.getElementById("usernameInput");
    // const enterMagicBtn = document.getElementById("enterMagicBtn"); // 移除重複聲明
    const clientWaitingOverlay = document.getElementById("clientWaitingOverlay");
    const clientWaitText = document.getElementById("clientWaitText");

    // --- Usage Limit Update ---
    async function updateUsageLimit() {
        if (!isMentor()) return;
        try {
            const res = await fetch(`${API_BASE}/auth/me?mentor_id=${encodeURIComponent(currentMentorId)}`);
            const data = await res.json();
            const usageSpan = document.getElementById("usageLimitSpan");
            const usageText = document.getElementById("usageStatusText");
            if (usageSpan && data.usage_limit !== undefined) {
                usageSpan.innerText = data.usage_limit;
                usageText.style.display = "block";
            }
        } catch (e) {
            console.error("Failed to fetch personal usage limit", e);
        }
    }

    function connectWebSocket(mentorId, clientId) {
        if (!mentorId) mentorId = guideName; // 預設
        if (!clientId) clientId = currentUserName || 'guest';

        const protocol = WS_PROTOCOL;
        const host = WS_HOST;

        let wsUrl = "";
        if (isMentor()) {
            wsUrl = `${protocol}//${host}/ws/${encodeURIComponent(mentorId)}/mentor`;
        } else {
            wsUrl = `${protocol}//${host}/ws/${encodeURIComponent(mentorId)}/client/${encodeURIComponent(clientId)}`;
        }

        console.log(`[WebSocket] Role: ${currentUserRole}, URL: ${wsUrl}`);
        const loadingStatus = document.getElementById("loadingStatus");
        if (loadingStatus && currentUserRole === 'client') {
            loadingStatus.innerText = `正在連線至 ${mentorId} 的房間...`;
        }

        ws = new WebSocket(wsUrl);

        ws.onopen = () => {
            console.log("WebSocket connected as", currentUserRole);
            isWsConnected = true;
            loginOverlay.style.display = "none";
            
            const badge = document.getElementById("wsStatusBadge");
            if (badge) {
                badge.innerText = "WS: ONLINE";
                badge.classList.remove("disconnected");
                badge.classList.add("connected");
            }

            if (currentUserRole === 'client') {
                document.querySelector('.tabs').style.display = 'none'; // 客戶看不到 Tabs
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
                if (isMentor()) {
                    updateUIWithClient(data.client_name);
                }
            } else if (data.type === "room_init") {
                isMainClient = data.is_main;
                isTobyOnline = data.toby_online; // Sync initial status

                if (data.announcement) {
                    renderAnnouncement(data.announcement);
                }
                console.log("[Room] Init. Main Client:", isMainClient, "Toby Online:", isTobyOnline);

                if (currentUserRole === 'client') {
                    clientWaitingOverlay.classList.toggle("hidden", isTobyOnline);
                }
                updateObserverUI();
            } else if (data.type === "role_upgrade") {
                isMainClient = data.is_main;
                alert("您已晉升為主要客戶，現在可以進行操作！");
                updateObserverUI();
            } else if (data.type === "room_update") {
                console.log("[Room] Level Updated:", data.room_level);
            } else if (data.type === "announcement_update") {
                renderAnnouncement(data.text);
            } else if (data.type === "divination_start") {
                // (已移除: 客戶端不再因為導師切換頁籤而跟著閃爍跳轉)
            } else if (data.type === "client_question") {
                // 客戶傳送問題給 Toby
                if (isMentor()) {
                    const incoming = data.question;
                    const color = data.color || "gold";
                    if (getCurrentActiveQuestion() === "") {
                        syncInputs(incoming); // Auto populate
                    } else if (getCurrentActiveQuestion() !== incoming) {
                        addToStash(incoming, color); // Auto stash if different
                    }
                    alert("獲得客戶傳送的靈能意念 (問題已送達)！");
                }
            } else if (data.type === "divination_result") {
                // Toby 占卜完成，傳結果給客戶
                if (currentUserRole === 'client') {
                    clientWaitingOverlay.classList.add("hidden");
                    renderSummaryResult(data);
                } else if (isMentor()) {
                    updateUsageLimit();
                }
            } else if (data.type === "toby_status") {
                isTobyOnline = data.is_online;
                if (currentUserRole === 'client') {
                    clientWaitingOverlay.classList.toggle("hidden", isTobyOnline);

                    // Hide spread selection and other mentor-only controls for clients
                    document.querySelectorAll('.controls .form-group').forEach(group => {
                        if (group.querySelector('label') && (group.querySelector('label').getAttribute('data-i18n') === 'label_spread')) {
                            group.style.display = 'none';
                        }
                    });

                    updateObserverUI();

                    if (isTobyOnline) {
                        if (isMainClient) {
                            drawBtn.disabled = false; castBtn.disabled = false; drawZhugeBtn.disabled = false; castXiaoliurenBtn.disabled = false; castDaliurenBtn.disabled = false;
                        }
                        alert("導師已經上線，您可以開始與神祕智慧連結了！");
                    } else {
                        drawBtn.disabled = true; castBtn.disabled = true; drawZhugeBtn.disabled = true; castXiaoliurenBtn.disabled = true; castDaliurenBtn.disabled = true;
                        alert("導師目前離線中，系統已暫停發問功能，請等待導師上線。");
                    }
                }
            } else if (data.type === "friend_request") {
                if (currentUserRole === 'toby' || currentMentorId) {
                    fetchNotifications();
                    // (Optional) still show alert if desired, but bell is the main way now
                    console.log("Friend request received from:", data.from);
                }
            } else if (data.type === "friend_accepted") {
                if (currentUserRole === 'toby' || currentMentorId) {
                    fetchNotifications();
                    window.loadFriendsList && window.loadFriendsList();
                }
            } else if (data.type === "friend_presence") {
                if (currentUserRole === 'toby' || currentMentorId) {
                    window.loadFriendsList && window.loadFriendsList();
                }
            } else if (data.type === "chat_message") {
                if (currentUserRole === 'toby' || currentMentorId) {
                    fetchNotifications();
                    window.handleIncomingChat && window.handleIncomingChat(data);
                }
            }
        };

        ws.onclose = (event) => {
            console.log("WebSocket disconnected with code:", event.code);
            isWsConnected = false;

            if (event.code === 4002) {
                const busyArea = document.getElementById("busyMessageArea");
                const waitText = document.getElementById("clientWaitText");
                if (busyArea) {
                    busyArea.classList.remove("hidden");
                }
                if (waitText) {
                    waitText.style.opacity = "0.5";
                }
                return; // 忙碌中不重連
            }

            if (loginOverlay.style.display === "none") {
                // 斷線 5 秒後嘗試重連 (僅限客戶端，導師端由用戶手動處理重啟)
                if (!isAdminMode) {
                    setTimeout(() => {
                        if (!isWsConnected) connectWebSocket(currentMentorId, currentUserName);
                    }, 5000);
                }
            }
        };

        function updateObserverUI() {
            if (currentUserRole !== 'client') return;

            const interactiveElements = [
                'questionInput', 'drawBtn', 'micTarot',
                'ichingQuestionInput', 'castBtn', 'micIChing',
                'zhugeQuestionInput', 'drawZhugeBtn', 'micZhuge',
                'xiaoliurenQuestionInput', 'castXiaoliurenBtn', 'micXiaoliuren',
                'daliurenQuestionInput', 'castDaliurenBtn', 'micDaliuren'
            ];

            const displayStyle = isMainClient ? 'block' : 'none';
            const flexStyle = isMainClient ? 'flex' : 'none';

            interactiveElements.forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    if (el.tagName === 'DIV' || el.tagName === 'SECTION') {
                        el.style.display = displayStyle;
                    } else if (id.includes('Input')) {
                        // Textareas are usually inside a flex div
                        if (el.parentElement.style.display === 'flex' || !isMainClient) {
                            el.parentElement.style.display = flexStyle;
                        }
                    } else {
                        el.style.display = displayStyle;
                    }
                }
            });

            // Special handling for the "Send Question" banner/text if needed
            const waitText = document.getElementById("clientWaitText");
            if (waitText) {
                if (!isMainClient) {
                    const dict = translations[langSelect.value] || translations["繁體中文"];
                    waitText.innerHTML = `<span style="color:var(--primary-color)">[ 觀測模式 ]</span><br>您目前正在觀看他人的占卜`;
                } else {
                    // Restore default waiting text via translation
                    const dict = translations[langSelect.value] || translations["繁體中文"];
                    waitText.innerText = dict.client_wait_text;
                }
            }
        }
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

        refreshStatefulUI(); // This sets the button text

        // Update placeholders
        const placeholder = dict["placeholder_question"] || "請在心中默念問題，或寫下來由古老智慧幫您解讀...";
        if (mode === 'tarot') {
            drawBtn.disabled = false;
            questionInput.placeholder = placeholder;
        } else if (mode === 'iching') {
            castBtn.disabled = false;
            ichingQuestionInput.placeholder = placeholder;
        } else if (mode === 'zhuge') {
            drawZhugeBtn.disabled = false;
            zhugeQuestionInput.placeholder = placeholder;
        } else if (mode === 'daliuren') {
            castDaliurenBtn.disabled = false;
            daliurenQuestionInput.placeholder = placeholder;
        }
    }

    function renderAnnouncement(text) {
        const banner = document.getElementById("announcementBanner");
        const textEl = document.getElementById("announcementText");
        if (!banner || !textEl) return;

        if (!text || text.trim() === "") {
            banner.classList.add("hidden");
            return;
        }

        // URL regex to auto-link
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const html = text.replace(urlRegex, (url) => {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });

        textEl.innerHTML = html;
        banner.classList.remove("hidden");
    }

    function copyShareLink() {
        if (!currentMentorId) return;
        // Default client name: GuestUser
        const baseUrl = window.location.origin + window.location.pathname;
        const shareUrl = `${baseUrl}?mentor=${encodeURIComponent(currentMentorId)}&client=${encodeURIComponent("GuestUser")}`;

        navigator.clipboard.writeText(shareUrl).then(() => {
            const status = document.getElementById("copyLinkStatus");
            if (status) {
                status.style.opacity = "1";
                setTimeout(() => status.style.opacity = "0", 2000);
            }
        }).catch(err => {
            console.error("Failed to copy link:", err);
            alert("複製連結失敗，請手動複製: " + shareUrl);
        });
    }

    function renderSummaryResult(data) {
        const dict = translations[langSelect.value] || translations["繁體中文"];
        const fallbackDict = translations["繁體中文"];
        clearResultContainers();
        resultTitle.innerText = dict["result_heading"] || fallbackDict["result_heading"] || `✨ 解讀結果 ✨`;
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

            let changedLinesHtml = '';
            if (res.changed_hexagram_id) {
                const changedBinary = res.lines_binary.map((b, idx) =>
                    res.moving_indices.includes(idx) ? (b === 1 ? 0 : 1) : b
                );
                changedBinary.forEach((binary) => {
                    if (binary === 1) {
                        changedLinesHtml += `<div class="hex-line yang"><div class="hex-line-part"></div></div>`;
                    } else {
                        changedLinesHtml += `<div class="hex-line yin"><div class="hex-line-part"></div><div class="hex-line-part"></div></div>`;
                    }
                });
            }

            hexagramContainer.innerHTML = `
            <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
                <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
                  <h2 style="color: #E8D5B7;">本卦：${res.hexagram_name}</h2>
                  <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${res.hexagram_id}.jpg" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
                  <div style="color: #B8A88A; margin-top: 0.5rem;">${res.upper_trigram}上 ${res.lower_trigram}下</div>
                  <div class="hexagram-lines" style="margin-top:1rem;">${linesHtml}</div>
                </div>
                ${res.changed_hexagram_id ? `
                <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px;">
                  <h2 style="color: #E8D5B7;">之卦：${res.changed_hexagram_name}</h2>
                  <img src="${ASSETS_BASE}/assets/images/iching/hexagrams/${res.changed_hexagram_id}.jpg" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
                  <div class="hexagram-lines" style="margin-top:1rem;">${changedLinesHtml}</div>
                  <div style="color: #B8A88A; margin-top: 1rem; font-size: 0.9rem;">(動爻變化產生)</div>
                </div>
                ` : ''}
            </div>
          `;
        } else if (data.mode === 'zhuge') {
            zhugeContainer.classList.remove("hidden");
            const res = data.result;
            // 資訊複雜度：streamlit(工程師) > Vite(導師) > Vite(客戶)
            // Vite(客戶) 僅顯示籤詩，Vite(導師) 會額外顯示 interp1, interp2 以及 AI 解讀
            zhugeContainer.innerHTML = `
            <div class="zg-container glass-panel" style="max-width:550px; margin: 0 auto; text-align: center; padding: 2.5rem; position: relative; border: 1px solid rgba(255,215,0,0.2); background: linear-gradient(135deg, rgba(30,30,30,0.8), rgba(15,15,15,0.9));">
                <div class="zg-seal" style="position: absolute; top: 1.5rem; right: 1.5rem; width: 50px; height: 50px; border: 2px solid #b22222; color: #b22222; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; transform: rotate(15deg); font-weight: bold; border-radius: 4px; pointer-events: none; opacity: 0.7;">諸葛<br>神算</div>
                <div class="zg-header" style="color: #FFD700; font-size: 1.1rem; margin-bottom: 2rem; letter-spacing: 0.2rem; opacity: 0.8;">
                    — 第 ${res.id} 籤 —
                </div>
                <div class="zg-poem-wrapper" style="margin-bottom: 2.5rem; display: inline-block; text-align: left;">
                    <div class="zg-poem" style="font-family: 'Noto Serif TC', serif; font-size: 1.6rem; white-space: pre-wrap; line-height: 2.2; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">${res.poem}</div>
                </div>
                ${isMentor() ? `
                    <div class="zg-details" style="margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1.5rem;">
                        ${res.interp1 || res.explanation ? `
                        <div class="zg-explanation-title" style="color: #B8A88A; font-size: 0.8rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.1rem;">白話解讀</div>
                        <div class="zg-explanation" style="font-size: 1rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 8px; margin-bottom: 1rem;">${res.interp1 || res.explanation}</div>
                        ` : ''}
                        ${res.interp2 ? `
                        <div class="zg-explanation-title" style="color: #B8A88A; font-size: 0.8rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.1rem;">古典意象</div>
                        <div class="zg-explanation" style="font-size: 1rem; color: #ddd; line-height: 1.6; text-align: left; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 8px;">${res.interp2}</div>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
          `;

            if (isMentor() && res.interpretation) {
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
                  ${isMentor() ? `<p style="color:#ddd; margin-bottom:1rem; line-height:1.6;">${description}</p>` : ''}
                  <div style="font-family:'Noto Serif TC', serif; color:#fff; font-size:1.1rem; border:1px solid rgba(255,255,255,0.2); padding:1rem; border-radius:8px; white-space:pre-wrap;">${poetry}</div>
              </div>
          </div>`;

            if (isMentor() && data.interpretation) {
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
            const scKeys = { "初傳": "初傳", "中傳": "中傳", "末傳": "末傳" };
            for (let k in scKeys) {
                let val = res.san_chuan[k];
                if (val) {
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
              <div class="dlr-title" style="color: #a78bfa; margin-top: 1.5rem; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">四課</div>
              <div class="dlr-row" style="margin-bottom: 1rem;">`;
            const skKeys = ["第一課", "第二課", "第三課", "第四課"];
            skKeys.forEach(k => {
                let val = res.si_ke[k];
                if (val) {
                    let top = Array.isArray(val) && val.length > 0 ? val[0] : "";
                    let bottom = Array.isArray(val) && val.length > 1 ? val[1] : "";
                    daliurenHtml += `
                    <div class="dlr-item" style="border: 1px solid rgba(255,255,255,0.05);">
                        <span style="font-size: 0.75rem; color: #aaa; margin-bottom: 0.3rem;">${k}</span>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #fff;">${top}</span>
                        <span style="font-size: 1.2rem; color: #ddd;">${bottom}</span>
                    </div>
                  `;
                }
            });
            daliurenHtml += `</div></div>`;
            daliurenContainer.innerHTML = daliurenHtml;
        }
    }

    // Legacy login block removed - using the dual-mode block at line 288 instead.

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

            // Initializing Firebase-based Google Auth UI
            const btnContainer = document.getElementById("googleSigninContainer");
            if (btnContainer) {
                btnContainer.innerHTML = `
              <button onclick="loginWithGoogleFirebase()" style="
                  display: flex; align-items: center; justify-content: center;
                  width: 310px; height: 50px; background: white; color: #444;
                  border: 1px solid #ddd; border-radius: 25px; cursor: pointer;
                  font-family: Roboto, sans-serif; font-weight: 500; font-size: 16px;
                  transition: all 0.2s;
              " onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='white'">
                  <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" style="width: 18px; margin-right: 12px;">
                  Continue with Google (Firebase)
              </button>
          `;
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

            recognition.onstart = function () {
                recognizing = true;
                btn.innerText = "🛑";
                inputEl.placeholder = "正在聽取聲音...";
            };

            recognition.onresult = function (event) {
                const transcript = event.results[0][0].transcript;
                inputEl.value += (inputEl.value ? " " : "") + transcript;
            };

            recognition.onerror = function (event) {
                console.error("Speech recognition error", event.error);
                inputEl.placeholder = "語音辨識失敗，請手動輸入...";
            };

            recognition.onend = function () {
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
        if (cardsGrid) { cardsGrid.innerHTML = ""; cardsGrid.classList.add("hidden"); }
        if (hexagramContainer) { hexagramContainer.innerHTML = ""; hexagramContainer.classList.add("hidden"); }
        if (zhugeContainer) { zhugeContainer.innerHTML = ""; zhugeContainer.classList.add("hidden"); }
        if (xiaoliurenContainer) { xiaoliurenContainer.innerHTML = ""; xiaoliurenContainer.classList.add("hidden"); }
        if (daliurenContainer) { daliurenContainer.innerHTML = ""; daliurenContainer.classList.add("hidden"); }
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

    let selectedEnergyColor = "red";

    // Color Selector Logic (Client Only)
    document.querySelectorAll("#clientColorSelector .color-opt").forEach(opt => {
        opt.addEventListener("click", () => {
            opt.parentElement.querySelectorAll(".color-opt").forEach(el => el.classList.remove("active"));
            opt.classList.add("active");
            selectedEnergyColor = opt.getAttribute("data-color");

            const ball = document.getElementById("magicCrystalBall");
            if (ball) {
                ball.className = `crystal-ball ball-${selectedEnergyColor}`;
            }
        });
    });

    function showLoader() {
        // This is for the mentor's general loader (simple spinner)
        const loader = document.getElementById("loader");
        loader.classList.remove("hidden");
    }

    drawBtn.addEventListener("click", async () => {
        const spreadId = spreadSelect.value;
        const question = questionInput.value.trim();

        if (currentUserRole === 'client') {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: "client_question",
                    mode: "tarot",
                    question: question,
                    color: selectedEnergyColor || "red"
                }));
                clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
                clientWaitingOverlay.classList.remove("hidden");
            }
            return;
        }

        // Reset UI
        clearResultContainers();
        cardsGrid.classList.remove("hidden");
        resultArea.classList.remove("hidden");
        showLoader();
        drawBtn.disabled = true;
        drawBtn.innerText = "靈能抽牌中...";

        try {
            const response = await fetch(`${API_BASE}/tarot/draw`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId || guideName,
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
                ws.send(JSON.stringify({ type: "divination_result", mode: "tarot", result: data }));
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
                ws.send(JSON.stringify({
                    type: "client_question",
                    mode: "iching",
                    question: question,
                    color: selectedEnergyColor || "red"
                }));
                clientWaitText.innerText = "問題已送出，導師正在為您解讀天意...";
                clientWaitingOverlay.classList.remove("hidden");
            }
            return;
        }

        // Reset UI
        clearResultContainers();
        hexagramContainer.classList.remove("hidden");
        resultArea.classList.remove("hidden");
        showLoader();
        castBtn.disabled = true;
        castBtn.innerText = "六爻推演中...";

        try {
            const response = await fetch(`${API_BASE}/iching/cast`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId || guideName,
                    question: question ? question : null,
                    language: langSelect.value
                })
            });

            if (!response.ok) {
                throw new Error("占卜伺服器無回應，請確認 FastAPI 已啟動。");
            }

            const data = await response.json();

            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "divination_result", mode: "iching", result: data }));
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
                ws.send(JSON.stringify({
                    type: "client_question",
                    mode: "zhuge",
                    question: question,
                    color: selectedEnergyColor || "red"
                }));
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
        showLoader();
        drawZhugeBtn.disabled = true;
        drawZhugeBtn.innerText = "神算啟動中...";

        try {
            const response = await fetch(`${API_BASE}/zhuge/draw`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId || guideName,

                    question: question ? question : null,
                    language: langSelect.value
                })
            });

            if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

            const data = await response.json();

            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "divination_result", mode: "zhuge", result: data }));
            }

            resultTitle.innerText = `🎋 諸葛神算 🎋`;

            // 資訊複雜度：streamlit(工程師) > Vite(導師) > Vite(客戶)
            // Vite(客戶) 僅顯示籤詩，Vite(導師) 會額外顯示 interp1, interp2 以及 AI 解讀
            zhugeContainer.innerHTML = `
         <div class="zg-container glass-panel" style="max-width:100%; margin: 0 auto; padding: 2.5rem; text-align: center; background: rgba(0,0,0,0.6); border-radius: 20px; border: 1px solid rgba(255,215,0,0.15);">
            <div class="zg-title-badge" style="display:inline-block; padding: 0.6rem 2rem; background: linear-gradient(135deg, #FFD700, #B8860B); color: #000; border-radius: 30px; font-weight: 800; font-size: 1.1rem; margin-bottom: 2.5rem; box-shadow: 0 4px 15px rgba(255,215,0,0.3); border: 2px solid rgba(255,255,255,0.2);">
                🎋 諸葛神算 第 ${data.id || ''} 籤
            </div>
            
            <div class="zg-poem-wrapper">
                <div class="zg-poem">
                    ${formatZhugePoem(data.poem)}
                </div>
            </div>

            <div class="zg-details" style="display: flex; flex-direction: column; gap: 1.2rem; text-align: left;">
                <div class="zg-interp-card" style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #FFD700;">
                    <div style="font-size: 0.85rem; color: #FFD700; font-weight: bold; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px;">✨ 白話解讀</div>
                    <div style="font-size: 1rem; color: #eee; line-height: 1.7;">${data.interp1 || data.explanation}</div>
                </div>
                
                <div class="zg-interp-card" style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #a78bfa;">
                    <div style="font-size: 0.85rem; color: #a78bfa; font-weight: bold; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px;">📜 古典意象</div>
                    <div style="font-size: 1rem; color: #ddd; line-height: 1.7;">${data.interp2}</div>
                </div>
            </div>
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
                ws.send(JSON.stringify({
                    type: "client_question",
                    mode: "xiaoliuren",
                    question: question,
                    color: selectedEnergyColor || "red"
                }));
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
        showLoader();
        castXiaoliurenBtn.disabled = true;
        castXiaoliurenBtn.innerText = "起卦中...";

        try {
            const response = await fetch(`${API_BASE}/xiaoliuren/draw`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId || guideName,

                    question: question ? question : null,
                    language: langSelect.value
                })
            });

            if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

            const data = await response.json();

            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "divination_result", mode: "xiaoliuren", result: data }));
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
                ws.send(JSON.stringify({
                    type: "client_question",
                    mode: "daliuren",
                    question: question,
                    color: selectedEnergyColor || "red"
                }));
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
        showLoader();
        castDaliurenBtn.disabled = true;
        castDaliurenBtn.innerText = "起課中...";

        try {
            const response = await fetch(`${API_BASE}/daliuren/cast`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    mentor_id: currentMentorId || guideName,

                    question: question ? question : null,
                    language: langSelect.value
                })
            });

            if (!response.ok) throw new Error("伺服器無回應，請確認 FastAPI 已啟動。");

            const data = await response.json();

            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "divination_result", mode: "daliuren", result: data }));
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
            const scKeys = { "初傳": "初傳", "中傳": "中傳", "末傳": "末傳" };
            for (let k in scKeys) {
                let val = data.san_chuan[k];
                if (val) {
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
            const skKeys = { "一課": "第一課", "二課": "第二課", "三課": "第三課", "四課": "第四課" };
            for (let k in skKeys) {
                let val = data.si_ke[k];
                if (val && val.length >= 2) {
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
            const mentorIdParam = currentMentorId ? `&mentor_id=${encodeURIComponent(currentMentorId)}` : '';
            const res = await fetch(`${API_BASE}/history/clients?t=${Date.now()}${mentorIdParam}`);
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
        } catch (e) { console.error("載入歷史客戶選單失敗:", e); }

        loadHistory();
    });

    const historyClientFilter = document.getElementById("historyClientFilter");
    if (historyClientFilter) {
        historyClientFilter.addEventListener("change", loadHistory);
    }

    async function loadHistory() {
        const dict = translations[langSelect.value] || translations["繁體中文"];
        const fallbackDict = translations["繁體中文"];

        loader.classList.remove("hidden");
        historyGrid.innerHTML = "";

        const finalMentorId = currentMentorId || guideName;
        let qs = `&mentor_id=${encodeURIComponent(finalMentorId)}`;
        const filterEl = document.getElementById("historyClientFilter");
        if (filterEl && filterEl.value) {
            qs += `&client_name=${encodeURIComponent(filterEl.value)}`;
        }

        try {
            const res = await fetch(`${API_BASE}/history?limit=30&t=${Date.now()}${qs}`);
            const records = await res.json();

            if (records.length === 0) {
                historyGrid.innerHTML = `<div class="empty-state" style="text-align:center; padding: 3rem; color: #aaa;">${dict["history_no_records"] || fallbackDict["history_no_records"]}</div>`;
                return;
            }

            records.forEach(r => {
                let title = "📜";
                if (r.type === "tarot") title = "🔮";
                else if (r.type === "iching") title = "☯️";
                else if (r.type === "zhuge") title = "🎋";
                else if (r.type === "xiaoliuren") title = "🎲";
                else if (r.type === "daliuren") title = "🌌";

                let summary = "";
                if (r.type === "tarot") {
                    const cards = r.result?.cards || r.cards;
                    if (cards) summary = cards.map(c => c.card_name_zh || c.name_zh).join(", ");
                } else if (r.type === "iching") {
                    const orig = r.result?.hexagram_name || r.original_hexagram;
                    summary = orig ? `本卦：${orig}` : "";
                } else if (r.type === "zhuge") {
                    summary = `第 ${r.result?.id || "?"} 籤`;
                } else if (r.type === "xiaoliuren") {
                    summary = r.result?.final_state || "起卦完成";
                } else if (r.type === "daliuren") {
                    summary = r.result?.date || "時局分析";
                }

                const isSuccess = r.ai_interpretation && typeof r.ai_interpretation === 'string' && !r.ai_interpretation.includes("error");
                const statusClass = isSuccess ? "success" : "error";
                const statusText = isSuccess ? (dict["history_success"] || "解讀成功") : (dict["history_error_fix"] || "分析異常");

                const itemDiv = document.createElement("div");
                itemDiv.className = "history-item glass-panel";
                itemDiv.style.cssText = "cursor: pointer; padding: 1.2rem; margin-bottom: 1rem; transition: transform 0.2s; border-left: 4px solid " + (isSuccess ? "#10b981" : "#ef4444");
                itemDiv.innerHTML = `
            <div class="history-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
              <span class="history-type" style="font-weight:bold; color: #FFD700;">${title}</span>
              <span class="history-time" style="font-size:0.8rem; color:#888;">${r.timestamp.split("T")[0]}</span>
            </div>
            <div class="history-question" style="font-size:0.95rem; color:#fff; margin-bottom:0.5rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                <span style="color:#B8A88A;">${dict["history_q_prefix"] || "Q:"}</span> ${r.question || "..."}
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div class="history-result-summary" style="font-size:0.85rem; color:#aaa;">${summary}</div>
                <div class="history-status ${statusClass}" style="font-size:0.75rem; padding: 2px 8px; border-radius:10px; background: ${isSuccess ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'}; color: ${isSuccess ? '#10b981' : '#ef4444'};">
                    ${statusText}
                </div>
            </div>
        `;
                itemDiv.addEventListener("click", () => showHistoryDetail(r));
                historyGrid.appendChild(itemDiv);
            });

        } catch (e) {
            console.error(e);
            historyGrid.innerHTML = `<p style="text-align:center; padding:2rem; color:#ef4444;">${dict["history_load_error"] || "Load Error"}</p>`;
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
                 <img class="card-image ${cardOrientation}" src="${ASSETS_BASE}${imgPath.replace('.png', '.jpg')}" alt="${card.card_name_zh || card.name_zh}" onerror="this.src='/vite.svg'">
               </div>
               <div class="card-info glass-panel" style="background: rgba(0,0,0,0.5);">
                   <div class="card-position">${card.position_name || card.position || `Card ${index + 1}`}</div>
                   <div class="card-name">${card.card_name_zh || card.name_zh} <span style="font-size:0.8rem">${orientationText}</span></div>
               </div>
             </div>
           `;
                });
                detailHtml += `</div>`;
            }
        } else if (r.type === 'iching') {
            const res = r.result || {};
            let orig = res.original_hexagram;
            let changed = res.changed_hexagram;

            // Handle legacy records where hexagram might be a string or missing from result
            if (typeof orig !== 'object') {
                orig = {
                    id: res.hexagram_id || r.hexagram_id,
                    name: r.original_hexagram || (typeof orig === 'string' ? orig : '未知'),
                    trigrams: res.original_trigrams || { upper: (r.upper_trigram && r.upper_trigram !== '上') ? r.upper_trigram : '', lower: (r.lower_trigram && r.lower_trigram !== '下') ? r.lower_trigram : '' }
                }
            }
            if (typeof changed !== 'object' && (r.changed_hexagram || changed || res.changed_hexagram_id)) {
                changed = {
                    id: res.changed_hexagram_id || r.changed_hexagram_id,
                    name: r.changed_hexagram || (typeof changed === 'string' ? changed : '變卦')
                };
            }

            let linesInfo = res.lines_info || [];
            if (linesInfo.length === 0 && res.lines_binary) {
                // Synthesize for records that have binary data but not full info objects
                const moving = res.moving_indices || r.moving_indices || [];
                linesInfo = res.lines_binary.map((b, idx) => ({
                    original: b,
                    moving: moving.includes(idx),
                    changed: moving.includes(idx) ? (b === 1 ? 0 : 1) : b
                }));
            }

            let linesHtml = '';
            if (linesInfo.length > 0) {
                linesInfo.forEach((line) => {
                    let origVal = line.original;
                    if (origVal === undefined && line.value !== undefined) {
                        const v = Number(line.value);
                        origVal = (v === 7 || v === 9) ? 1 : 0;
                    }
                    const movingClass = line.moving ? 'moving' : '';
                    if (Number(origVal) === 1) {
                        linesHtml += `<div class="hex-line yang ${movingClass}"><div class="hex-line-part"></div></div>`;
                    } else {
                        linesHtml += `<div class="hex-line yin ${movingClass}"><div class="hex-line-part"></div><div class="hex-line-part"></div></div>`;
                    }
                });
            }

            let changedLinesHtml = '';
            if (changed && (changed.id || changed.name) && linesInfo.length > 0) {
                linesInfo.forEach((line) => {
                    let cVal = line.changed;
                    if (cVal === undefined && line.value !== undefined) {
                        const v = Number(line.value);
                        cVal = (v === 6 || v === 7) ? 1 : 0;
                    }
                    if (Number(cVal) === 1) {
                        changedLinesHtml += `<div class="hex-line yang"><div class="hex-line-part"></div></div>`;
                    } else {
                        changedLinesHtml += `<div class="hex-line yin"><div class="hex-line-part"></div><div class="hex-line-part"></div></div>`;
                    }
                });
            }

            // Image fallbacks
            const origImgPath = (orig && orig.id) ? `${ASSETS_BASE}/assets/images/iching/hexagrams/${orig.id}.jpg` : (res.original_image_path ? `${ASSETS_BASE}${res.original_image_path.replace('.png', '.jpg')}` : '/vite.svg');
            const changedImgPath = (changed && changed.id) ? `${ASSETS_BASE}/assets/images/iching/hexagrams/${changed.id}.jpg` : (res.changed_image_path ? `${ASSETS_BASE}${res.changed_image_path.replace('.png', '.jpg')}` : '/vite.svg');

            // Trigram label fix
            const upperT = (orig.trigrams?.upper && orig.trigrams.upper !== '上') ? orig.trigrams.upper : '';
            const lowerT = (orig.trigrams?.lower && orig.trigrams.lower !== '下') ? orig.trigrams.lower : '';
            const trigramDisplay = (upperT || lowerT) ? `${upperT}上 ${lowerT}下` : '';

            detailHtml += `
          <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap; margin-bottom:2rem;">
              <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px; background: rgba(0,0,0,0.5);">
                <h3 style="color: #E8D5B7;">本卦：${orig.name || '無'}</h3>
                <img src="${origImgPath}" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
                <div style="color: #B8A88A; margin-top: 0.5rem;">${trigramDisplay}</div>
                <div class="hexagram-lines" style="margin-top:1rem;">${linesHtml}</div>
              </div>
              ${(changed && (changed.id || (changed.name && changed.name !== '變卦' && changed.name !== '未知'))) ? `
              <div class="glass-panel" style="text-align: center; margin-bottom: 1rem; flex:1; min-width:250px; background: rgba(0,0,0,0.5);">
                <h3 style="color: #E8D5B7;">之卦：${changed.name}</h3>
                <img src="${changedImgPath}" style="max-width:200px; border-radius:10px; margin:10px auto; display:block;" onerror="this.src='/vite.svg'">
                <div class="hexagram-lines" style="margin-top:1rem;">${changedLinesHtml}</div>
                <div style="color: #B8A88A; margin-top: 1rem; font-size: 0.9rem;">(動爻變化產生)</div>
              </div>
              ` : ''}
          </div>
        `;
        } else if (r.type === 'zhuge') {
            const res = r.result || {};
            detailHtml += `
             <div class="zg-container glass-panel" style="max-width:100%; margin: 0 auto; padding: 2.5rem; text-align: center; background: rgba(0,0,0,0.6); border-radius: 20px; border: 1px solid rgba(255,215,0,0.15);">
                <div class="zg-title-badge" style="display:inline-block; padding: 0.6rem 2rem; background: linear-gradient(135deg, #FFD700, #B8860B); color: #000; border-radius: 30px; font-weight: 800; font-size: 1.1rem; margin-bottom: 2.5rem; box-shadow: 0 4px 15px rgba(255,215,0,0.3); border: 2px solid rgba(255,255,255,0.2);">
                    🎋 諸葛神算 第 ${res.id || ''} 籤
                </div>
                
                <div class="zg-poem-wrapper">
                    <div class="zg-poem">
                        ${formatZhugePoem(res.poem)}
                    </div>
                </div>

                <div class="zg-details" style="display: flex; flex-direction: column; gap: 1.2rem; text-align: left;">
                    ${res.interp1 || res.explanation ? `
                    <div class="zg-interp-card" style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #FFD700;">
                        <div style="font-size: 0.85rem; color: #FFD700; font-weight: bold; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px;">✨ 白話解讀</div>
                        <div style="font-size: 1rem; color: #eee; line-height: 1.7;">${res.interp1 || res.explanation}</div>
                    </div>
                    ` : ''}
                    
                    ${res.interp2 ? `
                    <div class="zg-interp-card" style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #a78bfa;">
                        <div style="font-size: 0.85rem; color: #a78bfa; font-weight: bold; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 1px;">📜 古典意象</div>
                        <div style="font-size: 1rem; color: #ddd; line-height: 1.7;">${res.interp2}</div>
                    </div>
                    ` : ''}
                </div>
            </div>
         `;
        } else if (r.type === 'xiaoliuren') {
            const res = r.result || {};
            const states = res.small_six_states || ["", "", ""];
            const determination = res.final_state || "";
            const description = res.details?.description || "";
            const poetry = res.details?.poem || "";

            const xlrColors = {
                "大安": "#4ade80",
                "留連": "#fbbf24",
                "速喜": "#f87171",
                "赤口": "#ef4444",
                "小吉": "#60a5fa",
                "空亡": "#94a3b8"
            };
            const getXlrColor = (s) => xlrColors[s] || "#fff";

            detailHtml += `
          <div class="xlr-container glass-panel" style="max-width:100%; margin: 0 auto; padding: 2rem; text-align: center; background: rgba(0,0,0,0.5); border-radius: 16px;">
              <div class="xlr-header" style="color: #FFD700; font-size: 1.4rem; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,215,0,0.2); padding-bottom: 1rem; font-weight: bold; letter-spacing: 2px;">
                 🎲 小六壬起卦紀錄
              </div>
              
              <div class="xlr-steps" style="display: flex; justify-content: center; align-items: center; margin-bottom: 2.5rem; gap: 15px; flex-wrap: wrap;">
                  <div class="xlr-step-item" style="width: 120px; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s ease;">
                      <div style="font-size: 0.75rem; color: #888; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">初傳</div>
                      <div style="font-size: 1.2rem; color: ${getXlrColor(states[0])}; font-weight: bold;">${states[0] || '無'}</div>
                  </div>
                  <div style="font-size: 1.5rem; color: rgba(255,255,255,0.2);">➜</div>
                  <div class="xlr-step-item" style="width: 120px; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s ease;">
                      <div style="font-size: 0.75rem; color: #888; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">中傳</div>
                      <div style="font-size: 1.2rem; color: ${getXlrColor(states[1])}; font-weight: bold;">${states[1] || '無'}</div>
                  </div>
                  <div style="font-size: 1.5rem; color: rgba(255,255,255,0.2);">➜</div>
                  <div class="xlr-step-item" style="width: 130px; padding: 1.2rem; background: rgba(255,255,255,0.05); border-radius: 12px; border: 2px solid ${getXlrColor(states[2])}44; box-shadow: 0 0 15px ${getXlrColor(states[2])}22;">
                      <div style="font-size: 0.8rem; color: ${getXlrColor(states[2])}; margin-bottom: 0.5rem; font-weight: bold;">終選結果</div>
                      <div style="font-size: 1.4rem; color: #fff; font-weight: bold;">${states[2] || '無'}</div>
                  </div>
              </div>

              <div class="xlr-final glass-panel" style="background: rgba(255,255,255,0.03); padding: 2rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); position: relative; overflow: hidden;">
                  <div style="position: absolute; top:0; left:0; width: 4px; height: 100%; background: ${getXlrColor(determination)};"></div>
                  <div class="xlr-det" style="font-size: 2rem; color: ${getXlrColor(determination)}; margin-bottom: 1.5rem; font-weight: 800; letter-spacing: 4px; filter: drop-shadow(0 0 10px ${getXlrColor(determination)}44);">
                    ${determination}
                  </div>
                  ${poetry ? `
                  <div class="xlr-poem" style="font-family: 'Noto Serif TC', serif; font-size: 1.3rem; color: #fff; margin-bottom: 1.5rem; line-height: 1.8; letter-spacing: 2px; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
                    ${poetry}
                  </div>` : ''}
                  <div class="xlr-desc" style="font-size: 1rem; color: #bbb; line-height: 1.8; text-align: left; background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.02); white-space: pre-wrap;">${description}</div>
              </div>
          </div>
          `;
        } else if (r.type === 'daliuren') {
            const res = r.result || {};
            let patternStr = Array.isArray(res.pattern) && res.pattern.length > 0 ? res.pattern.join('、') : '無特殊格局';
            detailHtml += `
            <div class="dlr-container glass-panel" style="max-width:800px; margin: 0 auto; padding: 1.5rem; text-align: center; background: rgba(0,0,0,0.5);">
                <div class="dlr-header" style="color: #FFD700; font-size: 1.2rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,215,0,0.3); padding-bottom: 1rem;">
                    🌌 <b>時局</b>：${res.date || ''} (${res.jieqi || ''}) &nbsp;|&nbsp; <b>格局</b>：${patternStr}
                </div>
                <div class="dlr-title" style="color: #a78bfa; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">三傳</div>
                <div class="dlr-row" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
          `;
            const scKeys = { "初傳": "初傳", "中傳": "中傳", "末傳": "末傳" };
            const sanChuan = res.san_chuan || {};
            for (let k in scKeys) {
                let val = sanChuan[k] || sanChuan[{ "初傳": "chu", "中傳": "zhong", "末傳": "mo" }[k]]; // Fallback to legacy/English keys if any
                if (val) {
                    let display_val = Array.isArray(val) && val.length > 0 ? val[0] : String(val);
                    let sub_val = Array.isArray(val) && val.length > 1 ? val[1] : "";
                    detailHtml += `
                    <div class="dlr-item" style="flex:1; min-width:80px; padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                        <div class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-bottom: 0.5rem;">${k}</div>
                        <div class="dlr-val" style="font-size: 1.5rem; font-weight: bold; color: #fff; font-family: 'Noto Serif TC', serif;">${display_val}</div>
                        <div class="dlr-label" style="font-size: 0.85rem; color: #aaa; margin-top: 0.5rem;">${sub_val}</div>
                    </div>
                  `;
                }
            }
            detailHtml += `</div>
              <div class="dlr-title" style="color: #a78bfa; margin-top: 1.5rem; margin-bottom: 1rem; font-weight: bold; font-size: 1.1rem;">四課</div>
              <div class="dlr-row" style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;">`;
            const skKeys = ["第一課", "第二課", "第三課", "第四課"];
            const siKe = res.si_ke || res["四課"] || {};
            skKeys.forEach((k, idx) => {
                const numKey = ['一', '二', '三', '四'][idx];
                let val = siKe[k] || siKe[`${numKey}課`];
                if (!val) {
                    const altKeys = [`ke${idx + 1}`, `課${idx + 1}`, `${idx + 1}`, `課${numKey}`];
                    for (let ak of altKeys) { if (siKe[ak]) { val = siKe[ak]; break; } }
                }
                if (val) {
                    let rawContent = Array.isArray(val) && val.length > 0 ? val[0] : "";
                    let deity = Array.isArray(val) && val.length > 1 ? val[1] : "";

                    // Split 2-character content (e.g., "酉丑") into top/bottom
                    let top = rawContent;
                    let mid = "";
                    if (rawContent.length === 2) {
                        top = rawContent[0];
                        mid = rawContent[1];
                    }

                    detailHtml += `
                    <div class="dlr-item" style="flex:1; min-width:80px; border: 1px solid rgba(255,255,255,0.05); padding: 0.8rem; background: rgba(0,0,0,0.2); border-radius: 8px;">
                        <span style="font-size: 0.75rem; color: #aaa; margin-bottom: 0.3rem; display:block;">${k}</span>
                        <span style="font-size: 1.2rem; font-weight: bold; color: #fff; display:block; font-family: 'Noto Serif TC', serif;">${top}</span>
                        ${mid ? `<span style="font-size: 1.2rem; font-weight: bold; color: #fff; display:block; font-family: 'Noto Serif TC', serif; margin-top:2px;">${mid}</span>` : ''}
                        <span style="font-size: 0.85rem; color: #aaa; margin-top: 0.5rem; display:block;">${deity}</span>
                    </div>
                  `;
                }
            });
            detailHtml += `</div></div>`;
        }

        if (r.ai_interpretation) {
            const formatText = r.ai_interpretation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
            detailHtml += `
        <div class="interpretation" style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
          <h3 style="color: var(--primary-color); margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            ✨ AI 專屬解讀
          </h3>
          <div style="line-height: 1.8; color: #eee;">${formatText}</div>
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

    // --- Social Panel Logic ---
    const socialToggleBtn = document.getElementById("socialToggleBtn");
    const socialPanel = document.getElementById("socialPanel");
    const closeSocialBtn = document.getElementById("closeSocialBtn");
    const tabFriends = document.getElementById("tabFriends");
    const tabChat = document.getElementById("tabChat");
    const friendsView = document.getElementById("friendsView");
    const chatView = document.getElementById("chatView");

    const addFriendInput = document.getElementById("addFriendInput");
    const addFriendBtn = document.getElementById("addFriendBtn");
    const friendsList = document.getElementById("friendsList");

    const chatHeaderTarget = document.getElementById("currentChatTarget");
    const backToFriendsBtn = document.getElementById("backToFriendsBtn");
    const chatMessages = document.getElementById("chatMessages");
    const chatInput = document.getElementById("chatInput");
    const sendChatBtn = document.getElementById("sendChatBtn");

    let currentChatFriendId = null;

    socialToggleBtn.addEventListener("click", () => {
        socialPanel.classList.add("open");
        socialToggleBtn.classList.remove("has-notification");
        if (currentUserRole === "toby") window.loadFriendsList();
    });

    closeSocialBtn.addEventListener("click", () => socialPanel.classList.remove("open"));

    tabFriends.addEventListener("click", () => {
        tabFriends.classList.add("active");
        tabChat.classList.remove("active");
        friendsView.classList.remove("hidden");
        chatView.classList.add("hidden");
        if (currentUserRole === "toby") window.loadFriendsList();
    });

    tabChat.addEventListener("click", () => {
        tabChat.classList.add("active");
        tabFriends.classList.remove("active");
        chatView.classList.remove("hidden");
        friendsView.classList.add("hidden");
        if (currentChatFriendId) loadChatHistory(currentChatFriendId);
    });

    backToFriendsBtn.addEventListener("click", () => tabFriends.click());

    addFriendBtn.addEventListener("click", async () => {
        const targetId = addFriendInput.value.trim();
        if (!targetId) return;
        try {
            const res = await fetch(`${API_BASE}/social/friends/request`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mentor_id: currentMentorId, target_id: targetId })
            });
            if (!res.ok) {
                const data = await res.json();
                alert(data.detail || "發送邀請失敗");
            } else {
                alert("好友邀請已送出！");
                addFriendInput.value = "";
                window.loadFriendsList();
            }
        } catch (e) {
            console.error(e);
        }
    });

    window.loadFriendsList = async function () {
        if (!isMentor()) return;
        try {
            const res = await fetch(`${API_BASE}/social/friends/list?mentor_id=${encodeURIComponent(currentMentorId)}`);
            if (res.ok) {
                const friends = await res.json();
                friendsList.innerHTML = "";
                if (friends.length === 0) {
                    friendsList.innerHTML = `<li style="text-align:center; color:#888;">尚未加入任何好友</li>`;
                    return;
                }
                friends.forEach(f => {
                    const li = document.createElement("li");
                    li.className = "friend-item";
                    li.innerHTML = `
                      <div>
                          <span class="status-dot ${f.is_online ? 'online' : 'offline'}"></span>
                          <span>${f.mentor_id}</span>
                      </div>
                      <button style="background:none;border:none;color:var(--primary-color);cursor:pointer;" title="傳送訊息">💬</button>
                  `;
                    li.addEventListener("click", () => {
                        currentChatFriendId = f.mentor_id;
                        chatHeaderTarget.innerText = f.mentor_id;
                        chatInput.disabled = false;
                        sendChatBtn.disabled = false;
                        tabChat.click();
                    });
                    friendsList.appendChild(li);
                });
            }
        } catch (e) {
            console.error("載入好友失敗", e);
        }
    };

    async function loadChatHistory(friendId) {
        chatMessages.innerHTML = "<div style='text-align:center;color:#888;'>載入中...</div>";
        try {
            const res = await fetch(`${API_BASE}/social/chat/history?mentor_id=${encodeURIComponent(currentMentorId)}&target_id=${encodeURIComponent(friendId)}`);
            if (res.ok) {
                const msgs = await res.json();
                chatMessages.innerHTML = "";
                if (msgs.length === 0) {
                    chatMessages.innerHTML = "<div style='text-align:center;color:#888;'>開始與導師的對話吧！</div>";
                    return;
                }
                msgs.forEach(m => appendChatMessageUI(m));
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        } catch (e) {
            console.error("載入聊天失敗", e);
        }
    }

    function appendChatMessageUI(m) {
        if (currentChatFriendId !== m.sender_id && currentChatFriendId !== m.receiver_id) return;
        const removePlaceholder = chatMessages.querySelector("div[style*='text-align:center']");
        if (removePlaceholder) removePlaceholder.remove();

        const isSelf = m.sender_id === currentMentorId;
        const d = new Date(m.timestamp);
        const timeStr = `${d.getHours()}:${d.getMinutes().toString().padStart(2, '0')}`;

        const div = document.createElement("div");
        div.className = `chat-msg ${isSelf ? 'self' : 'other'}`;
        div.innerHTML = `
          <div>${m.message}</div>
          <div class="chat-msg-time">${timeStr}</div>
      `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    window.handleIncomingChat = function (data) {
        if (!socialPanel.classList.contains("open") || currentChatFriendId !== data.from || chatView.classList.contains("hidden")) {
            socialToggleBtn.classList.add("has-notification");
        }
        if (currentChatFriendId === data.from) {
            appendChatMessageUI({
                sender_id: data.from,
                receiver_id: currentMentorId,
                message: data.message,
                timestamp: data.timestamp
            });
        }
    };

    sendChatBtn.addEventListener("click", async () => {
        const text = chatInput.value.trim();
        if (!text || !currentChatFriendId) return;
        chatInput.disabled = true;
        sendChatBtn.disabled = true;

        try {
            const res = await fetch(`${API_BASE}/social/chat/send`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mentor_id: currentMentorId, receiver_id: currentChatFriendId, message: text })
            });
            if (res.ok) {
                const m = await res.json();
                appendChatMessageUI(m);
                chatInput.value = "";
            } else {
                const err = await res.json();
                alert(err.detail || "傳送失敗");
            }
        } catch (e) {
            console.error(e);
        } finally {
            chatInput.disabled = false;
            sendChatBtn.disabled = false;
            chatInput.focus();
        }
    });

    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendChatBtn.click();
        }
    });

    // Show FAB if role is toby or any mentor
    const obsLogin = new MutationObserver(() => {
        const isMentorLoggedIn = (currentUserRole === 'toby' || currentMentorId) && document.getElementById("loginOverlay").style.display === "none";
        if (isMentorLoggedIn) {
            socialToggleBtn.classList.remove("hidden");
            socialToggleBtn.style.display = "flex";
            notificationBellBtn.classList.remove("hidden");
            notificationBellBtn.style.display = "flex";
            fetchNotifications(); // Fetch once on login
        } else {
            socialToggleBtn.classList.add("hidden");
            socialToggleBtn.style.display = "none";
            notificationBellBtn.classList.add("hidden");
            notificationBellBtn.style.display = "none";
        }
    });
    obsLogin.observe(document.getElementById("loginOverlay"), { attributes: true, attributeFilter: ['style'] });

    // --- Notification System Functions ---
    async function fetchNotifications() {
        if (!currentMentorId) return;
        try {
            const resp = await fetch(`${API_BASE}/social/notifications?mentor_id=${encodeURIComponent(currentMentorId)}`);
            if (!resp.ok) return;
            const data = await resp.json();
            updateNotificationUI(data);
        } catch (err) {
            console.error("Failed to fetch notifications:", err);
        }
    }

    function updateNotificationUI(data) {
        if (!notificationBadge || !notificationBellBtn) return;
        const totalCount = data.unread_messages_count + data.pending_friends_count;
        if (totalCount > 0) {
            notificationBadge.textContent = totalCount > 99 ? '99+' : totalCount;
            notificationBadge.classList.remove('hidden');
            notificationBadge.style.display = 'flex';
        } else {
            notificationBadge.classList.add('hidden');
            notificationBadge.style.display = 'none';
        }
        renderNotifications(data.recent_notifications);
    }

    function renderNotifications(items) {
        if (!notificationList) return;
        if (!items || items.length === 0) {
            notificationList.innerHTML = '<div style="text-align:center; color:#888; padding: 20px;">尚無新通知</div>';
            return;
        }

        notificationList.innerHTML = '';
        items.forEach(item => {
            const div = document.createElement('div');
            div.className = 'notification-item';

            let actionHtml = '';
            if (item.type === 'friend_request') {
                actionHtml = `
                <div class="notif-actions">
                  <button class="notif-btn-sm btn-accept" data-req-id="${item.sender_id}">接受</button>
                  <button class="notif-btn-sm btn-decline" data-req-id="${item.sender_id}">拒絕</button>
                </div>
              `;
            }

            const timeStr = new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            div.innerHTML = `
            <div class="notif-title">${item.type === 'friend_request' ? '👥 好友邀請' : '💬 新訊息'}</div>
            <div class="notif-msg">${item.message}</div>
            <span class="notif-time">${timeStr}</span>
            ${actionHtml}
          `;

            if (item.type === 'unread_message') {
                div.style.cursor = 'pointer';
                div.onclick = () => {
                    notificationPanel.classList.add('hidden');
                    document.getElementById('socialToggleBtn').click();
                    document.getElementById('tabChat').click();
                    // Try to find the friend item and click it, or just start chat
                    const chatHeaderTarget = document.getElementById("currentChatTarget");
                    const chatInput = document.getElementById("chatInput");
                    const sendChatBtn = document.getElementById("sendChatBtn");

                    // Note: startChat logic is integrated here
                    currentChatFriendId = item.sender_id;
                    chatHeaderTarget.innerText = item.sender_id;
                    chatInput.disabled = false;
                    sendChatBtn.disabled = false;
                    loadChatHistory(item.sender_id);

                    // Mark as read
                    fetch(`${API_BASE}/social/messages/read?mentor_id=${encodeURIComponent(currentMentorId)}&sender_id=${encodeURIComponent(item.sender_id)}`, { method: 'POST' })
                        .then(() => fetchNotifications());
                };
            }

            notificationList.appendChild(div);
        });

        notificationList.querySelectorAll('.btn-accept').forEach(btn => {
            btn.onclick = (e) => {
                e.stopPropagation();
                handleFriendResponse(btn.dataset.reqId, 'accept');
            };
        });
        notificationList.querySelectorAll('.btn-decline').forEach(btn => {
            btn.onclick = (e) => {
                e.stopPropagation();
                handleFriendResponse(btn.dataset.reqId, 'decline');
            };
        });
    }

    async function handleFriendResponse(requesterId, action) {
        try {
            const resp = await fetch(`${API_BASE}/social/friends/respond`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    mentor_id: currentMentorId,
                    requester_id: requesterId,
                    action: action
                })
            });
            if (resp.ok) {
                alert(action === 'accept' ? `已接受 ${requesterId} 的好友邀請` : `已拒絕邀請`);
                fetchNotifications();
                if (action === 'accept') window.loadFriendsList();
            }
        } catch (err) {
            console.error("Failed to respond to friend request:", err);
        }
    }

    notificationBellBtn.addEventListener('click', () => {
        notificationPanel.classList.toggle('hidden');
        if (!notificationPanel.classList.contains('hidden')) {
            fetchNotifications();
        }
    });

    document.getElementById('closeNotificationBtn').addEventListener('click', () => {
        notificationPanel.classList.add('hidden');
    });

    setInterval(() => {
        if (currentMentorId && document.getElementById("loginOverlay").style.display === "none") {
            fetchNotifications();
        }
    }, 30000);

    // --- Page-Agent Injection (Frontend) ---
    function initPageAgent(apiKey) {
        if (window.PageAgent) {
            console.log("Page-Agent SDK version:", window.PageAgent.version || "unknown");
            window.PageAgent.init({
                llm: { provider: 'gemini', apiKey: apiKey, model: 'gemini-1.5-flash' }
            });
            const style = document.createElement('style');
            style.innerHTML = `
            #page-agent-container, .page-agent-trigger { 
              left: 20px !important; 
              right: auto !important; 
              z-index: 2147483647 !important;
            }
            .page-agent-trigger {
              bottom: 120px !important; 
              background: linear-gradient(135deg, #6e8efb, #a777e3) !important;
              box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            }
          `;
            document.head.appendChild(style);
            console.log("Page-Agent initialized and styled successfully.");
        } else {
            console.error("Page-Agent SDK not found on window object.");
        }
    }

    // Fetch API key first then init agent
    console.log("Attempting to fetch Gemini Key for Page-Agent...");
    fetch(`${API_BASE}/config/keys`).then(r => {
        if (!r.ok) throw new Error(`HTTP error! status: ${r.status}`);
        return r.json();
    }).then(data => {
        if (data.gemini_key) {
            console.log("Gemini Key obtained. Length:", data.gemini_key.length);
            const script = document.createElement('script');
            script.src = "https://cdn.jsdelivr.net/npm/@alibaba/page-agent@latest/dist/index.iife.js";
            script.async = true;
            script.onload = () => {
                console.log("Page-Agent script loaded successfully.");
                initPageAgent(data.gemini_key);
            };
            script.onerror = () => console.error("Failed to load Page-Agent script from CDN.");
            document.head.appendChild(script);
        } else {
            console.warn("Gemini Key is empty. Page-Agent will not be initialized.");
        }
    }).catch(e => {
        console.error("Failed to load Gemini Key for PageAgent:", e.message);
    });

    renderQuickLogin();

    // --- URL Auto-Join Logic ---
    const urlParams = new URLSearchParams(window.location.search);
    const mentorId = urlParams.get('mentor');
    const clientName = urlParams.get('client');

    if (mentorId) {
        console.log(`[AutoJoin] Detected mentor=${mentorId}, client=${clientName}`);
        targetMentorInput.value = mentorId;
        if (clientName) {
            clientNameInput.value = clientName;
        }
        // Auto-click the button
        const enterBtn = document.getElementById("enterMagicBtn");
        if (enterBtn) {
            setTimeout(() => {
                console.log("[AutoJoin] Triggering login...");
                enterBtn.click();
            }, 500);
        }
    }
});
