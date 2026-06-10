import lessons from '../data/daliuren/lessons.json' with { type: 'json' };

export function castDaliuren({ question, language }) {
  if (!lessons || lessons.length === 0) {
    throw new Error("Daliuren lessons data is not loaded.");
  }
  const randomIndex = Math.floor(Math.random() * lessons.length);
  const lesson = lessons[randomIndex];

  let interpretation = `🌊 【離線本機起課：大六壬式盤】 🌊\n`;
  if (question) interpretation += `問卜內容：${question}\n`;
  interpretation += `\n【起課時間】：${lesson.date} (${lesson.jieqi})\n`;
  interpretation += `【課式格局】：${lesson.pattern.join('、') || '無特殊格局'}\n\n`;
  interpretation += `【三傳（初、中、末）】：\n`;
  Object.entries(lesson.san_chuan).forEach(([k, v]) => {
    const dizhi = Array.isArray(v) && v.length > 0 ? v[0] : '';
    const tianjiang = Array.isArray(v) && v.length > 1 ? v[1] : '';
    interpretation += `• ${k}：${dizhi} (${tianjiang})\n`;
  });
  interpretation += `\n【四課（一、二、三、四）】：\n`;
  Object.entries(lesson.si_ke).forEach(([k, v]) => {
    const tian = (Array.isArray(v) && v.length > 0 && v[0] && v[0][0]) || '';
    const di = (Array.isArray(v) && v.length > 0 && v[0] && v[0][1]) || '';
    interpretation += `• ${k}：天盤 ${tian} / 地盤 ${di}\n`;
  });
  interpretation += `\n💡 *提示：本機離線模式不消耗 Token。如需 AI 深度解讀與語音解說，請切換至 API 連線模式。*`;

  return {
    date: lesson.date, jieqi: lesson.jieqi, pattern: lesson.pattern,
    san_chuan: lesson.san_chuan, si_ke: lesson.si_ke,
    interpretation: question ? interpretation : null, audio_path: null
  };
}

export class Liuren {
  constructor(jieqi, cmonth, daygangzhi, hourgangzhi) {
    this.jieqi = jieqi; this.daygangzhi = daygangzhi; this.hourgangzhi = hourgangzhi; this.cmonth = cmonth;
    this.Gan = "甲乙丙丁戊己庚辛壬癸".split("");
    this.Zhi = "子丑寅卯辰巳午未申酉戌亥".split("");
    this.Cmonth = "正二三四五六七八九十".split("").concat(["十一", "十二"]);

    this.mg_dict = { "亥": "登明", "戌": "河魁", "酉": "從魁", "申": "傳送", "未": "小吉", "午": "勝光", "巳": "太乙", "辰": "天罡", "卯": "太沖", "寅": "功曹", "丑": "大吉", "子": "神後" };
    this.yima_dict = { "丑": "亥", "未": "巳" };
    
    const jigong_list = "寅辰巳未巳未申戌亥丑".split("").concat(this.Zhi);
    this.shigangjigong = {};
    this.Gan.concat(this.Zhi).forEach((k, i) => { this.shigangjigong[k] = jigong_list[i]; });

    this.yimadict = { "戌": "申", "寅": "申", "午": "申", "酉": "亥", "丑": "亥", "巳": "亥", "子": "寅", "辰": "寅", "申": "寅", "亥": "巳", "卯": "巳", "未": "巳" };

    this.liuqing_dict = { "被生": "父", "生": "子", "尅": "財", "比和": "兄", "被尅": "官" };

    this.wuxing = "火水金火木金水土土木,水火火金金木土水木土,火火金金木木土土水水,火木水金木水土火金土,木火金水水木火土土金";
    this.wuxing_relation_2 = {};
    const wr2_vals = "被尅,尅,比和,被生,生".split(",");
    this.wuxing.split(",").forEach((s, i) => { s.match(/../g).forEach(k => { this.wuxing_relation_2[k] = wr2_vals[i]; }); });

    this.ganzhiwuxing_dict = {};
    const gzwx_keys = "甲寅乙卯,丙巳丁午,壬亥癸子,庚申辛酉,未丑戊己未辰戌".split(",");
    const gzwx_vals = "木火水金土".split("");
    gzwx_keys.forEach((group, i) => { group.split("").forEach(char => { if (char !== ",") this.ganzhiwuxing_dict[char] = gzwx_vals[i]; }); });

    this.daynight_richppl_dict = {};
    "卯辰巳午未申".split("").forEach(k => { this.daynight_richppl_dict[k] = "晝"; });
    "酉戌亥子丑寅".split("").forEach(k => { this.daynight_richppl_dict[k] = "夜"; });

    this.ying = Object.fromEntries("寅巳申丑戌未子卯辰亥酉午".split("").map((k, i) => [k, "巳申寅戌未丑卯子辰亥酉午"[i]]));
    this.ying_chong_dict = {};
    "寅巳,申,丑,戌,未,子,卯".split(",").forEach(k => { k.split("").forEach(char => { this.ying_chong_dict[char] = "刑"; }); });
    "午,辰,酉,亥".split(",").forEach(k => { k.split("").forEach(char => { this.ying_chong_dict[char] = "自刑"; }); });

    this.chong2 = Object.fromEntries("子午丑未寅申卯酉辰戌巳亥".split("").map((k, i) => [k, "午子未丑申寅酉卯戌辰亥巳"[i]]));
    this.he = Object.fromEntries("子丑午未巳申寅亥卯戌辰酉".split("").map((k, i) => [k, "丑子未午申巳亥寅戌卯酉辰"[i]]));
    this.hai = Object.fromEntries("子未午丑巳寅辰卯申亥酉戌".split("").map((k, i) => [k, "未子丑午寅巳卯辰亥申戌酉"[i]]));
    this.po = Object.fromEntries("寅亥巳申午卯未戌酉子丑辰".split("").map((k, i) => [k, "亥寅申巳卯午戌未子酉辰丑"[i]]));

    this.sky_generals = "貴蛇雀合勾龍空虎常玄陰后".split("");
    
    this.liujiashun_dict = {};
    const jiazis = this.get_jiazi();
    for (let i = 0; i < 60; i += 10) { const shun = jiazis[i]; for (let j = 0; j < 10; j++) { this.liujiashun_dict[jiazis[i + j]] = shun; } }
  }

  get_jiazi() { const res = []; for (let i = 0; i < 60; i++) { res.push(this.Gan[i % 10] + this.Zhi[i % 12]); } return res; }
  gangzhi_yinyang(gangorzhi) { return "甲丙戊庚壬子寅辰午申戌".includes(gangorzhi) ? "陽" : "陰"; }
  duplicates(lst, item) { const res = []; if (!Array.isArray(lst)) return res; lst.forEach((x, i) => { if (x === item) res.push(i); }); return res.length > 1 ? res : (res.length === 1 ? res[0] : res); }
  multi_key_dict_get(d, k) { for (const key in d) { if (key.split(",").includes(k) || key.includes(k)) return d[key]; } return null; }
  find_duplicates(lst) { const seen = new Set(); const dups = new Set(); lst.forEach(item => { if (seen.has(item)) dups.add(item); else seen.add(item); }); return Array.from(dups); }
  Max(lst) { return lst.length === 0 ? null : Math.max(...lst); }
  new_list(olist, o) { const a = olist.indexOf(o); return a === -1 ? olist : olist.slice(a).concat(olist.slice(0, a)); }

  shunkong(daygangzhi, zhi) {
    const dayshun = this.liujiashun_dict[daygangzhi];
    const heads = this.get_jiazi().filter((_, i) => i % 10 === 0);
    const gans_empty = this.Gan.concat(["空", "空"]);
    const findshun = {};
    const shun_starts = "甲丙戊庚壬空".split("");
    heads.forEach((h, i) => {
        const shifted = this.new_list(gans_empty, shun_starts[i] || "空");
        findshun[h] = Object.fromEntries(this.Zhi.map((z, j) => [z, shifted[j]]));
    });
    return findshun[dayshun] ? findshun[dayshun][zhi] : null;
  }

  Ganzhiwuxing(gangorzhi) { return this.ganzhiwuxing_dict[gangorzhi]; }

  find_ke_relation(ke) {
    const top_bottom = (this.Ganzhiwuxing(ke[0]) || "") + (this.Ganzhiwuxing(ke[1]) || "");
    const rels = "下賊上,上尅下,比和,下生上,上生下".split(",");
    const keys = "火水金火木金水土土木,水火火金金木土水木土,火火金金木木土土水水,火木水金木水土火金土,木火金水水木火土土金".split(",");
    for (let i = 0; i < keys.length; i++) { if (keys[i].match(/../g).includes(top_bottom)) return rels[i]; }
    return null;
  }

  sky_pan_list() {
    const mgd = { '雨水,驚蟄': '亥', '春分,清明': '戌', '穀雨,立夏': '酉', '小滿,芒種': '申', '夏至,小暑': '未', '大暑,立秋': '午', '處暑,白露': '巳', '秋分,寒露': '辰', '霜降,立冬': '卯', '小雪,大雪': '寅', '冬至,小寒': '丑', '大寒,立春': '子' };
    const gmg = this.multi_key_dict_get(mgd, this.jieqi);
    return [this.new_zhi_list(gmg), gmg];
  }

  find_season(s) {
    const jq = "立春雨水驚蟄春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒".match(/../g);
    const season = "春春春春春春夏夏夏夏夏夏秋秋秋秋秋秋冬冬冬冬冬冬".split("");
    return Object.fromEntries(jq.map((k, i) => [k, season[i]]))[s];
  }

  moongeneral() { return this.sky_pan_list()[1]; }

  new_zhi_list(zhi) {
    const zhihead_code = this.Zhi.indexOf(zhi);
    const res1 = [];
    for (let i = 0; i < this.Zhi.length; i++) { res1.push(this.Zhi[(zhihead_code + i) % this.Zhi.length]); }
    return res1;
  }

  sky_n_earth_list() {
    const earth = this.new_zhi_list(this.hourgangzhi[1]);
    const sky = this.sky_pan_list()[0];
    return Object.fromEntries(earth.map((e, i) => [e, sky[i]]));
  }

  earth_n_sky_list() {
    const earth = this.new_zhi_list(this.hourgangzhi[1]);
    const sky = this.sky_pan_list()[0];
    return Object.fromEntries(sky.map((s, i) => [s, earth[i]]));
  }

  all_sike() {
    const sky_n_earth = this.sky_n_earth_list();
    const yike = sky_n_earth[this.shigangjigong[this.daygangzhi[0]]] + this.daygangzhi[0];
    const erke = sky_n_earth[yike[0]] + yike[0];
    const sanke = sky_n_earth[this.daygangzhi[1]] + this.daygangzhi[1];
    const sike = sky_n_earth[sanke[0]] + sanke[0];
    return [sike, sanke, erke, yike];
  }

  new_zhigangcangong_list(zhi) {
    const zhigangcangong = "子丑癸寅甲卯辰乙巳丙戊午未己申庚酉戌辛亥壬".split("");
    const zhihead_code = zhigangcangong.indexOf(zhi);
    const res1 = [];
    for (let i = 0; i < zhigangcangong.length; i++) { res1.push(zhigangcangong[(zhihead_code + i) % zhigangcangong.length]); }
    return res1;
  }

  fanyin() {
    const sky_earth = this.sky_n_earth_list();
    const sky = Object.values(sky_earth);
    const earth = Object.keys(sky_earth);
    const earth_sky_combine_wuxing = earth.map((e, i) => {
        const combine = (this.Ganzhiwuxing(sky[i]) || "") + (this.Ganzhiwuxing(e) || "");
        const rels = "被尅,尅,比和,被生,生".split(",");
        const keys = "火水金火木金水土土木,水火火金金木土水木土,火火金金木木土土水水,火木水金木水土火金土,木火金水水木火土土金".split(",");
        for (let j = 0; j < keys.length; j++) { if (keys[j].match(/../g).includes(combine)) return rels[j]; }
        return null;
    });
    const count = earth_sky_combine_wuxing.filter(x => x === "被尅" || x === "尅").length;
    return [count, earth_sky_combine_wuxing];
  }

  find_sike_relations() {
    let sike_list = [];
    let sike = this.all_sike();
    for (let i of sike) {
        let b = this.find_ke_relation(i);
        sike_list.push(b);
    }
    
    let classify = "試其他";
    const count = (arr, val) => arr.filter(x => x === val).length;

    if (count(sike_list, "下賊上") === 2 && count(sike_list, "上尅下") === 2) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") === 1 && count(sike_list, "下賊上") === 1) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") === 0 && count(sike_list, "下賊上") === 4) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") > 1 && count(sike_list, "下賊上") === 1) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") === 0 && count(sike_list, "下賊上") === 1) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") === 1 && count(sike_list, "下賊上") === 0) {
        classify = "上尅下";
    } else if (count(sike_list, "上尅下") === 1 && count(sike_list, "下賊上") === 3) {
        classify = "下賊上";
    } else if (count(sike_list, "下賊上") === 2 && count(sike_list, "上尅下") === 1) {
        classify = "下賊上";
    } else if (count(sike_list, "下賊上") === 4 && count(sike_list, "上尅下") === 0) {
        classify = "下賊上";
    } else if (count(sike_list, "下賊上") === 2 && count(sike_list, "上尅下") === 0) {
        classify = "下賊上";
    } else if (count(sike_list, "下賊上") >= 2 && count(sike_list, "上尅下") <= 1) {
        classify = "下賊上";
    } else if (count(sike_list, "上尅下") >= 2 && count(sike_list, "下賊上") === 0) {
        classify = "上尅下";
    } else if (count(sike_list, "上生下") === 4) {
        classify = "試八專";
    }

    let dayganzhi_wuxing = this.Ganzhiwuxing(this.daygangzhi[0]);
    let dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    let wuxing_ke = sike.map(i => this.Ganzhiwuxing(i[0]));
    let shangke_list = [];
    for (let d of wuxing_ke) {
        let shangke = this.multi_key_dict_get(this.wuxing_relation_2, d + dayganzhi_wuxing);
        shangke_list.push(shangke);
    }

    let dayganzhi_same_location = "甲寅,丁未,己未,庚申,癸丑".split(",");
    let res = this.get_jiazi().filter(i => !dayganzhi_same_location.includes(i));
    let checkdayganzhi_dict = {
        [dayganzhi_same_location.join(",")]: "日干支同位",
        [res.join(",")]: "日干支不同位"
    };

    let fanyin_days = "丁丑,己丑,辛丑,辛未".split(",");
    let bazhuan_fanyin_days = ["丁未", "己未"];
    let jiazi_remove_fanyin = this.get_jiazi().filter(i => !fanyin_days.includes(i));
    let fanyin_day_dict = {
        [fanyin_days.join(",")]: "反吟",
        [bazhuan_fanyin_days.join(",")]: "反吟八專",
        [jiazi_remove_fanyin.concat(bazhuan_fanyin_days).join(",")]: "非反吟"
    };

    let checkdayganzhi = this.multi_key_dict_get(checkdayganzhi_dict, this.daygangzhi);
    let checkfanyin = this.multi_key_dict_get(fanyin_day_dict, this.daygangzhi);

    let moon_general = this.sky_pan_list()[1];
    let checkmoongeneralconflicttohour = this.multi_key_dict_get(this.wuxing_relation_2, this.Ganzhiwuxing(moon_general) + this.Ganzhiwuxing(this.hourgangzhi[1]));
    let sky_earth_fanyin = this.fanyin()[0];
    let blist = [];
    let fan_yin;

    if ((sky_earth_fanyin >= 8 && count(this.fanyin()[1], "比和") === 4) || count(this.fanyin()[1], "比和") === 12) {
        fan_yin = "天地盤返吟";
    } else {
        fan_yin = "天地盤沒有返吟";
    }

    let checkfuyin;
    if (this.hourgangzhi[1] === moon_general) {
        checkfuyin = "伏吟";
    } else {
        checkfuyin = "非伏吟";
    }

    let findtrue;

    if (count(sike_list, "上尅下") === 0 && count(sike_list, "下賊上") === 0) {
        findtrue = ["試賊尅涉害以外方法", "沒有", "沒有", classify, "沒有", "沒有"];
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    } else if (count(sike_list, "上尅下") === 1 && count(sike_list, "下賊上") === 0) {
        findtrue = ["試賊尅", [sike_list.indexOf("上尅下")], "沒有", classify, "沒有", "沒有"];
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    } else if (count(sike_list, "下賊上") === 1) {
        findtrue = ["試賊尅", [sike_list.indexOf("下賊上")], "沒有", classify, "沒有", "沒有"];
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    } else if (count(sike_list, "下賊上") >= 2 && this.Ganzhiwuxing(this.daygangzhi[0]) !== this.Ganzhiwuxing(this.daygangzhi[1])) {
        findtrue = ["試比用", [sike_list.indexOf("下賊上")], "沒有", classify, "沒有", "沒有", this.Ganzhiwuxing(this.daygangzhi[0]), this.Ganzhiwuxing(this.daygangzhi[1])];
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    } else if (count(sike_list, "下賊上") > 1) {
        let find_ke = this.duplicates(sike_list, "下賊上");
        if (typeof find_ke === 'number') find_ke = [find_ke];
        let zeikeshang_list = [];
        for (let i of find_ke) {
            let zeike = sike[i];
            zeikeshang_list.push(zeike);
        }
        let yy_list = [];
        for (let y of zeikeshang_list) {
            let yy = this.gangzhi_yinyang(y[0]);
            yy_list.push(yy);
        }
        let nn_list = [];
        for (let n of yy_list) {
            let p;
            if (n === dayganzhi_yy) {
                p = "True";
            } else {
                p = "False";
            }
            nn_list.push(p);
        }
        for (let i = 0; i < zeikeshang_list.length; i++) {
            let b = zeikeshang_list[i][0];
            blist.push(b);
        }
        let check_same = new Set(blist).size;

        if (check_same === 1 || new Set(sike_list).size === 1) {
            findtrue = ["試涉害", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        } else if (new Set(zeikeshang_list).size === 2 && count(nn_list, "True") === 1 && count(nn_list, "False") === 1) {
            findtrue = ["試比用", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        } else if (new Set(zeikeshang_list).size >= 2 && count(nn_list, "True") >= 0 && count(nn_list, "False") >= 0) {
            findtrue = ["試涉害", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        }
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    } else if (count(sike_list, "上尅下") > 1) {
        let find_ke = this.duplicates(sike_list, "上尅下");
        if (typeof find_ke === 'number') find_ke = [find_ke];
        let dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
        let zeikeshang_list = [];
        for (let i of find_ke) {
            let zeike = sike[i];
            zeikeshang_list.push(zeike);
        }
        let yy_list = [];
        for (let y of zeikeshang_list) {
            let yy = this.gangzhi_yinyang(y[0]);
            yy_list.push(yy);
        }
        let nn_list = [];
        for (let n of yy_list) {
            let p;
            if (n === dayganzhi_yy) {
                p = "True";
            } else {
                p = "False";
            }
            nn_list.push(p);
        }
        for (let i = 0; i < zeikeshang_list.length; i++) {
            let b = zeikeshang_list[i][0];
            blist.push(b);
        }
        let check_same = new Set(blist).size;

        if (check_same === 1) {
            findtrue = ["試賊尅", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        } else if (new Set(zeikeshang_list).size >= 2 && count(nn_list, "True") === 0) {
            findtrue = ["試涉害", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        } else if (new Set(zeikeshang_list).size >= 2 && count(nn_list, "True") === 1 && count(nn_list, "False") === 1) {
            findtrue = ["試比用", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        } else if (new Set(zeikeshang_list).size >= 2 && count(nn_list, "True") >= 1 && count(nn_list, "False") >= 1) {
            if ((sike.some(i => this.Ganzhiwuxing(i[0]) === this.Ganzhiwuxing(this.daygangzhi[0])) && dayganzhi_yy === "陽") || this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                findtrue = ["試比用", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
            } else {
                findtrue = ["試涉害", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
            }
        } else if (new Set(zeikeshang_list).size >= 2 && count(nn_list, "True") >= 2 && count(nn_list, "False") === 0) {
            findtrue = ["試涉害", find_ke, zeikeshang_list, classify, nn_list, yy_list, check_same];
        }
        return [sike_list, sike, shangke_list, checkdayganzhi, checkfuyin, checkmoongeneralconflicttohour, checkfanyin, findtrue, this.gangzhi_yinyang(this.daygangzhi[0]), fan_yin];
    }
  }

  find_three_pass(firstpass) {
    const sky_n_earth = this.sky_n_earth_list();
    return [firstpass, sky_n_earth[firstpass], sky_n_earth[sky_n_earth[firstpass]]];
  }

  zeike() {
    const countInArray = (arr, val) => arr.filter(x => x === val).length;
    const sike = this.all_sike();
    const dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    //hourganzhi_yy = this.gangzhi_yinyang(this.hourgangzhi[])
    const sike_list = this.find_sike_relations();
    let findtrue;

    //沒有上尅下或下賊上
    if (countInArray(sike_list[0], "上尅下") === 0 && countInArray(sike_list[0], "下賊上") === 0) {
      findtrue = "不適用，或試他法";
      return findtrue;
    }
    //多於一個上尅下或下賊上
    else if (sike_list[7][0] === "試涉害" || sike_list[7][0] === "試比用") {
      findtrue = "不適用，或試他法";
      return findtrue;
    }
    else if (countInArray(sike_list[0], "下賊上") > 2 && sike_list[7][6] > 1 && countInArray(sike_list[2], "尅") > 1) {
      findtrue = "不適用，或試他法";
      return findtrue;
    }
    else if (countInArray(sike_list[0], "下賊上") > 2 && sike_list[7][6] > 1 && countInArray(sike_list[2], "尅") === 1) {
      findtrue = ["賊尅", "重審"];
      return ["賊尅", "重審", this.find_three_pass(sike_list[7][2][sike_list[2].indexOf("尅")][0])];
    }
    else if (countInArray(sike_list[0], "下賊上") > 2 && sike_list[7][6] > 1 && countInArray(sike_list[2], "尅") === 0) {
      findtrue = ["賊尅", "重審"];
      return ["賊尅", "重審", this.find_three_pass(sike_list[7][2][sike_list[2].indexOf("生")][0])];
    }
    else if (countInArray(sike_list[0], "下賊上") > 2 && sike_list[7][6] === 1 && sike_list[9] === '天地盤沒有返吟') {
      findtrue = ["賊尅", "重審", this.find_three_pass(sike_list[7][2][0][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "下賊上") >= 2 && sike_list[7][0] === "試賊尅" && sike_list[7][6] === 1 && sike_list[9] === '天地盤沒有返吟') {
      findtrue = ["賊尅", "重審", this.find_three_pass(sike_list[7][2][0][0])];
      return findtrue;
    }
    //多於一個上尅下或下賊上
    else if (countInArray(sike_list[0], "上尅下") === 2 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[7][2][0] !== sike_list[7][2][1] && sike_list[7][6] > 1) {
      findtrue = "不適用，或試他法";
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") === 2 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[7][2][0] !== sike_list[7][2][1] && sike_list[7][6] === 1) {
      findtrue = ["賊尅", "元首", this.find_three_pass(sike_list[7][2][0][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") === 2 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[7][2][0] === sike_list[7][2][1]) {
      findtrue = ["賊尅", "元首", this.find_three_pass(sike_list[7][2][0][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") >= 2 && countInArray(sike_list[0], "下賊上") === 0) {
      findtrue = "不適用，或試他法";
    }
    else if (countInArray(sike_list[0], "上尅下") >= 2 && countInArray(sike_list[0], "下賊上") === 1) {
      findtrue = ["賊尅", "重審斫輪", this.find_three_pass(sike[sike_list[0].indexOf("下賊上")][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") > 2 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[7][0] === "試賊尅" && new Set(sike_list[7][1]).size === 1) {
      findtrue = ["賊尅", "元首", this.find_three_pass(sike_list[7][2][0][0])];
      return findtrue;
    }
    //一個下賊上
    else if (countInArray(sike_list[0], "下賊上") === 1 && sike_list[9] === '天地盤沒有返吟') {
      findtrue = ["賊尅", "重審", this.find_three_pass(sike[sike_list[0].indexOf("下賊上")][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "下賊上") >= 1 && countInArray(sike_list[0], "上尅下") === 0 && sike_list[9] === '天地盤返吟') {
      if (countInArray(sike_list[2], "生") >= 1) {
        findtrue = ["伏吟", "自任", [this.chong2[this.chong2[sike[sike_list[0].indexOf("下賊上")][0]]], this.daygangzhi[1], this.chong2[this.daygangzhi[1]]]];
        return findtrue;
      }
      if (countInArray(sike_list[2], "比和") >= 1) {
        findtrue = ["伏吟", "杜傳", [this.chong2[this.chong2[sike[sike_list[0].indexOf("下賊上")][0]]], this.daygangzhi[1], "子"]];
        return findtrue;
      }
      else {
        findtrue = "不適用，或試他法";
        return findtrue;
      }
    }
    else if (countInArray(sike_list[0], "下賊上") === 2 && countInArray(sike_list[0], "上尅下") === 0 && sike_list[9] === '天地盤沒有返吟') {
      if (sike_list[7][2][0] === sike_list[7][2][1]) {
        findtrue = ["賊尅", "重審", this.find_three_pass(sike_list[7][2][0][0])];
        return findtrue;
      }
      else if (sike_list[7][2][0] !== sike_list[7][2][1]) {
        findtrue = "不適用，或試他法";
        return findtrue;
      }
    }
    else if (countInArray(sike_list[0], "下賊上") === 2 && countInArray(sike_list[0], "上尅下") === 2 && sike_list[9] === '天地盤返吟') {
      findtrue = ["返吟", "無依", this.find_three_pass(sike[sike_list[0].indexOf("下賊上")][0])];
      return findtrue;
    }
    //一個上尅下
    else if (countInArray(sike_list[0], "上尅下") === 1 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[9] === '天地盤沒有返吟') {
      findtrue = ["賊尅", "元首", this.find_three_pass(sike[sike_list[0].indexOf("上尅下")][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") >= 2 && countInArray(sike_list[0], "下賊上") === 0 && sike_list[9] === '天地盤沒有返吟') {
      if (sike_list[7][2][0] === sike_list[7][2][1]) {
        findtrue = ["賊尅", "元首", this.find_three_pass(sike_list[7][2][0][0])];
      }
      else if (sike_list[7][2][0] !== sike_list[7][2][1]) {
        findtrue = "不適用，或試他法";
      }
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") === 1 && sike_list[9] === '天地盤沒有返吟') {
      findtrue = ["返吟", "無依1", this.find_three_pass(sike[sike_list[0].indexOf("上尅下")][0])];
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") === 1 && sike_list[9] === '天地盤返吟' && countInArray(sike_list[0], "下賊上") === 0) {
      if (this.hourgangzhi[1] !== "子") {
        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["返吟", "勵德", [this.chong2[sike[sike_list[0].indexOf("上尅下")][0]], this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]], this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]];
        }
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["返吟", "稼檣", [this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]], this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]], this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]]];
        }
        else {
          findtrue = ["返吟", "無依", [this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]], this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]], sike[1][0]]];
        }
      }
      if (this.hourgangzhi[1] === "子") {
        if (dayganzhi_yy === "陽") {
          if (sike_list[5] === "被尅") {
            findtrue = ["返吟", "無依", [this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]], this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]], this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]]]];
          }
          else {
            findtrue = ["返吟", "無依", [this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]], this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]], this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]]];
          }
        }
        if (dayganzhi_yy === "陰") {
          findtrue = ["返吟", "無依", [sike[0][1], this.ying[this.chong2[this.chong2[sike[sike_list[0].indexOf("上尅下")][0]]]], sike[0][1]]];
        }
      }
      return findtrue;
    }
    else if (countInArray(sike_list[0], "上尅下") === 1 && countInArray(sike_list[0], "下賊上") === 1 && sike_list[9] === '天地盤返吟') {
      if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
        findtrue = ["返吟", "龍戰", [sike[0][1], sike[0][0], sike[0][1]]];
      }
      if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
        findtrue = ["返吟", "元胎", [sike[2][1], sike[2][0], sike[2][1]]];
      }
      if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
        findtrue = ["返吟", "元胎", [sike[2][0], sike[2][1], sike[2][0]]];
      }
      else {
        try {
          const sikeChars = [];
          for (const item of sike) {
            for (const char of item) {
              sikeChars.push(this.Ganzhiwuxing(char));
            }
          }
          const counter = new Map();
          for (const char of sikeChars) {
            counter.set(char, (counter.get(char) || 0) + 1);
          }
          const charsGt3 = Array.from(counter.entries())
            .filter(([char, count]) => count > 3)
            .map(([char, count]) => char);
            
          if (charsGt3.length === 0) {
            throw new Error("IndexError");
          }
          
          if (charsGt3[0] === this.Ganzhiwuxing(this.daygangzhi[1])) {
            if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
              findtrue = ["返吟", "元胎", [sike[2][0], sike[2][1], sike[2][0]]];
            }
            else {
              findtrue = ["返吟", "無依", [sike[3][0], sike[2][0], sike[3][0]]];
            }
          }
          else {
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["返吟", "元胎寡宿", [sike[0][1], sike[0][0], sike[0][1]]];
            }
            else {
              findtrue = ["返吟", "斫輪", [sike[0][0], sike[0][1], sike[0][0]]];
            }
          }
        }
        catch (error) {
          if (error.message === "IndexError" || error.name === "TypeError") {
            if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["返吟", "返吟", [sike[1][0], sike[0][0], sike[1][0]]];
            }
            else {
              if (dayganzhi_yy === "陰") {
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
                  findtrue = ["返吟", "元胎勵德", [sike[0][0], sike[0][1], sike[0][0]]];
                }
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                  findtrue = ["返吟", "龍戰斬關斫輪", [sike[0][1], sike[0][0], sike[0][1]]];
                }
                else {
                  findtrue = ["返吟", "無依龍戰勵德", [sike[0][1], sike[0][0], sike[0][1]]];
                }
              }
              else {
                findtrue = ["返吟", "斫輪", [sike[0][0], sike[0][1], sike[0][0]]];
              }
            }
          } else {
            throw error;
          }
        }
      }
      return findtrue;
    }
    return "不適用，或試他法";
  }

  biyung() {
    const sike = this.all_sike();
    const relation = this.find_sike_relations();
    const filter_list = this.find_sike_relations()[7];
    const filter_list_four_ke = this.find_sike_relations()[7][2];
    const filter_list_yy = this.find_sike_relations()[7][5];
    const dayganzhi_yy = this.find_sike_relations()[8];
    const hourganzhi_yy = this.gangzhi_yinyang(this.hourgangzhi[1]);
    const hourganzhi_yy0 = this.gangzhi_yinyang(this.hourgangzhi[0]);

    const countOccurrences = (arr, val) => arr.filter(x => x === val).length;

    const getCounts = (arr) => {
      const counts = {};
      for (const item of arr) {
        counts[item] = (counts[item] || 0) + 1;
      }
      return counts;
    };

    let findtrue;

    if (filter_list[0] === "試賊尅") {
      findtrue = "不適用，或試他法";
      return findtrue;
    } else if (filter_list[0] === "試涉害") {
      findtrue = "不適用，或試他法";
      return findtrue;
    } else if (filter_list[0] === "試賊尅涉害以外方法") {
      findtrue = "不適用，或試他法";
      return findtrue;
    } else if (countOccurrences(relation[0], "下賊上") === 4) {
      if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
        findtrue = ["涉害", "絕嗣", this.find_three_pass(this.all_sike()[0][0])];
        return findtrue;
      } else {
        findtrue = "不適用，或試他法";
        return findtrue;
      }
    } else if (countOccurrences(relation[0], "下賊上") === 2 && relation[9] === '天地盤返吟') {
      if (dayganzhi_yy === "陽") {
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) || this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["返吟", "無依", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
        }
        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          if (hourganzhi_yy === "陰") {
            findtrue = ["返吟", "元胎", [this.all_sike()[0][1], this.all_sike()[0][0], this.all_sike()[0][1]]];
          } else {
            findtrue = ["返吟", "元胎", [this.all_sike()[2][1], this.all_sike()[2][0], this.all_sike()[2][1]]];
          }
        }
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
          findtrue = ["返吟", "無依", [this.all_sike()[2][0], this.all_sike()[2][1], this.all_sike()[2][0]]];
        } else {
          if (hourganzhi_yy === "陰") {
            if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.daygangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["返吟", "元胎", [this.all_sike()[3][0], this.all_sike()[2][0], this.all_sike()[3][0]]];
            }
            if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["返吟", "無依", [this.all_sike()[1][0], this.all_sike()[1][1], this.all_sike()[1][0]]];
            }
            if (this.Ganzhiwuxing(this.daygangzhi[1]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
              if (hourganzhi_yy0 === hourganzhi_yy) {
                findtrue = ["返吟", "元胎贅婿", [this.all_sike()[1][1], this.all_sike()[1][0], this.all_sike()[1][1]]];
              } else {
                findtrue = ["返吟", "元胎", [this.all_sike()[1][0], this.all_sike()[1][1], this.all_sike()[1][0]]];
              }
            }
            if (this.Ganzhiwuxing(this.daygangzhi[1]) !== this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["返吟", "元胎", [this.all_sike()[1][1], this.all_sike()[1][0], this.all_sike()[1][1]]];
            }
          } else {
            let flatChars = [];
            for (const item of sike) {
              for (const char of item) flatChars.push(char);
            }
            let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
            let counts = getCounts(mappedChars);
            let filteredCounts = Object.entries(counts).filter(([char, count]) => count === 2).map(([char]) => char);

            if (filteredCounts.length > 2) {
              if (sike[0][0] === this.daygangzhi[1]) {
                findtrue = ["返吟", "元胎勵德", [this.all_sike()[0][0], this.all_sike()[1][0], this.all_sike()[0][0]]];
              } else {
                findtrue = ["返吟", "元胎", [this.all_sike()[2][1], this.all_sike()[2][0], this.all_sike()[2][1]]];
              }
            } else {
              if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                findtrue = ["返吟", "三交", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
              } else {
                findtrue = ["返吟", "無依", [this.all_sike()[0][1], this.all_sike()[1][1], this.all_sike()[0][1]]];
              }
            }
          }
        }
      }
      if (dayganzhi_yy === "陰") {
        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["返吟", "元胎", [this.all_sike()[0][1], this.all_sike()[1][1], this.all_sike()[0][1]]];
        } else {
          if (hourganzhi_yy === "陰") {
            findtrue = ["返吟", "龍戰", [this.all_sike()[0][1], this.all_sike()[1][1], this.all_sike()[0][1]]];
          } else {
            findtrue = ["返吟", "無依", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
          }
        }
      }
      return findtrue;
    } else if (countOccurrences(relation[0], "下賊上") === 3 && relation[9] === '天地盤返吟') {
      if (dayganzhi_yy === "陽") {
        if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) !== this.Ganzhiwuxing(this.daygangzhi[1])) {
          findtrue = ["返吟", "元胎", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
        }
        if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
          findtrue = ["返吟", "高蓋", [this.all_sike()[0][1], this.all_sike()[1][1], this.all_sike()[0][1]]];
        }
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["返吟", "三交", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
        } else {
          findtrue = ["返吟", "返吟", [this.all_sike()[0][1], this.all_sike()[1][1], this.all_sike()[0][1]]];
        }
      } else {
        findtrue = ["返吟", "返吟", [this.all_sike()[1][1], this.all_sike()[0][1], this.all_sike()[1][1]]];
      }
      return findtrue;
    } else if (countOccurrences(relation[0], "下賊上") >= 2 && relation[9] === '天地盤沒有返吟') {
      if (filter_list_yy[0] === dayganzhi_yy) {
        findtrue = ["比用", "比用", this.find_three_pass(this.all_sike()[1][0])];
      }
      if (this.daygangzhi === this.hourgangzhi) {
        findtrue = ["比用", "知一斫輪", this.find_three_pass(this.all_sike()[2][0])];
      } else if (filter_list_yy[1] === dayganzhi_yy) {
        if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
          findtrue = ["比用", "知一斫輪四絕鑄印", this.find_three_pass(this.all_sike()[2][0])];
        } else {
          findtrue = ["比用", "比用", this.find_three_pass(this.all_sike()[2][1])];
        }
      } else {
        try {
          if (countOccurrences(relation[0], "上尅下") === 0) {
            let sikeWuxing = sike.map(i => this.Ganzhiwuxing(i[0]));
            let daygangzhi0Wuxing = this.Ganzhiwuxing(this.daygangzhi[0]);
            let f = sikeWuxing.indexOf(daygangzhi0Wuxing);
            if (f === -1) throw new Error("IndexError/ValueError");

            if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && hourganzhi_yy === "陰") {
              findtrue = ["涉害", "極陰", this.find_three_pass(this.all_sike()[0][1])];
            } else if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && hourganzhi_yy === "陽") {
              findtrue = ["涉害", "從革", this.find_three_pass(this.all_sike()[2][0])];
            } else {
              findtrue = ["比用", "比用", this.find_three_pass(sike[f][0])];
            }
          }
          if (countOccurrences(relation[0], "上尅下") === 1) {
            if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
              findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][0])];
            } else if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
              findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[2][0])];
            } else {
              try {
                let flatChars = [];
                for (const item of sike) {
                  for (const char of item) flatChars.push(char);
                }
                let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                let counts = getCounts(mappedChars);
                let filteredCounts = Object.entries(counts).filter(([char, count]) => count > 3).map(([char]) => char);

                if (filteredCounts.length === 0) throw new Error("IndexError");
                
                if (filteredCounts[0] === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                  findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][0])];
                } else {
                  let sikeWuxing = sike.map(i => this.Ganzhiwuxing(i[0]));
                  let hourgangzhi1Wuxing = this.Ganzhiwuxing(this.hourgangzhi[1]);
                  let f = sikeWuxing.indexOf(hourgangzhi1Wuxing);
                  if (f === -1) throw new Error("IndexError");
                  findtrue = ["涉害", "涉害", this.find_three_pass(sike[f][0])];
                }
              } catch (e) {
                if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                  if (dayganzhi_yy === "陰") {
                    findtrue = ["比用", "知一鑄印", this.find_three_pass(this.all_sike()[2][0])];
                  } else {
                    findtrue = ["涉害", "度厄", this.find_three_pass(this.all_sike()[0][0])];
                  }
                }
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                  findtrue = ["比用", "知一鑄印", this.find_three_pass(this.all_sike()[2][0])];
                }
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                  findtrue = ["比用", "知一斫輪羅網", this.find_three_pass(this.all_sike()[2][0])];
                }
                if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                  findtrue = ["涉害", "間傳", this.find_three_pass(this.all_sike()[1][0])];
                } else {
                  findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][0])];
                }
              }
            }
          }
        } catch (e) {
          try {
            let fa = this.find_duplicates(sike)[0];
            const isArrayEqual = (a, b) => Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((val, index) => val === b[index]);
            let faIndex = this.all_sike().findIndex(x => isArrayEqual(x, fa));
            if (faIndex === -1) throw new Error("IndexError");

            if (relation[0][faIndex] === "下賊上") {
              findtrue = ["賊尅", "重審", this.find_three_pass(fa[0])];
            } else if (relation[0][faIndex] === "上尅下") {
              findtrue = ["賊尅", "元首", this.find_three_pass(fa[0])];
            } else if (relation[0][faIndex] !== "上尅下" && relation[0][faIndex] !== "下賊上") {
              findtrue = ["涉害", "涉害", this.find_three_pass(fa[1])];
            }
          } catch (err) {
            if (dayganzhi_yy === "陰") {
              if (hourganzhi_yy === "陰") {
                if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                  findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[2][0])];
                } else {
                  findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[3][0])];
                }
              } else {
                findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][0])];
              }
            }
            if (dayganzhi_yy === "陽") {
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                findtrue = ["涉害", "涉害", this.find_three_pass(this.all_sike()[3][0])];
              } else if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                findtrue = ["涉害", "涉害", this.find_three_pass(this.all_sike()[0][0])];
              } else if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                findtrue = ["比用", "退茹", this.find_three_pass(this.all_sike()[2][0])];
              } else {
                findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[1][1])];
              }
            }
          }
        }
        if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
          if (countOccurrences(relation[0], "上尅下") === 2 && countOccurrences(relation[0], "下賊上") === 2) {
            findtrue = ["比用", "知一三奇", this.find_three_pass(this.all_sike()[2][0])];
          }
          if (countOccurrences(relation[0], "上尅下") === 0 && countOccurrences(relation[0], "下賊上") === 3) {
            if (dayganzhi_yy === "陽") {
              findtrue = ["比用", "知一鑄印", this.find_three_pass(this.all_sike()[2][0])];
            } else {
              findtrue = ["涉害", "龍戰", this.find_three_pass(this.all_sike()[1][0])];
            }
          }
          if (countOccurrences(relation[0], "上尅下") === 0 && countOccurrences(relation[0], "下賊上") === 2) {
            findtrue = ["涉害", "見機四絕", this.find_three_pass(this.all_sike()[2][0])];
          }
          if (countOccurrences(relation[0], "上尅下") === 1 && countOccurrences(relation[0], "下賊上") === 2) {
            findtrue = ["比用", "退茹", this.find_three_pass(this.all_sike()[0][0])];
          } else {
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
              try {
                let flatChars = [];
                for (const item of sike) {
                  for (const char of item) flatChars.push(char);
                }
                let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                let counts = getCounts(mappedChars);
                let filteredCounts = Object.entries(counts).filter(([char, count]) => count > 1).map(([char]) => char);

                if (filteredCounts.length > 2) {
                  findtrue = ["比用", "四絕鑄印", this.find_three_pass(this.all_sike()[0][0])];
                } else {
                  findtrue = ["涉害", "間傳", this.find_three_pass(this.all_sike()[1][0])];
                }
              } catch (e) {
                findtrue = ["涉害", "間傳", this.find_three_pass(this.all_sike()[1][0])];
              }
            }
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["比用", "知一度厄", this.find_three_pass(this.all_sike()[0][0])];
            }
            if (this.daygangzhi[0] === this.hourgangzhi[0]) {
              findtrue = ["涉害", "從革", this.find_three_pass(this.all_sike()[2][0])];
            }
            if (this.Ganzhiwuxing(this.daygangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["涉害", "涉害", this.find_three_pass(this.all_sike()[0][0])];
            }
          }
        } else {
          try {
            let fa = this.find_duplicates(sike)[0];
            if (fa === undefined) throw new Error("IndexError");
            let faIndex = this.all_sike().indexOf(fa);
            if (faIndex === -1) throw new Error("IndexError");

            if (relation[0][faIndex] !== "上尅下" && relation[0][faIndex] !== "下賊上") {
              findtrue = ["涉害", "曲直", this.find_three_pass(this.all_sike()[0][0])];
            }
            if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
              findtrue = ["比用", "知一進茹", this.find_three_pass(this.all_sike()[2][0])];
            }
            if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) !== this.Ganzhiwuxing(this.hourgangzhi[0])) {
              findtrue = ["涉害", "間傳斬關贄婿狡童", this.find_three_pass(this.all_sike()[3][0])];
            } else {
              if (dayganzhi_yy === "陰") {
                findtrue = ["比用", "知一不備亂首驀越", this.find_three_pass(this.all_sike()[0][0])];
              } else {
                findtrue = ["比用", "知一1", this.find_three_pass(this.all_sike()[2][0])];
              }
            }
          } catch (err) {
            if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
              findtrue = ["比用", "知一進茹", this.find_three_pass(this.all_sike()[0][0])];
            }
            if (countOccurrences(relation[0], "上尅下") === 2 && countOccurrences(relation[0], "下賊上") === 2) {
              if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[2][0])];
              } else {
                findtrue = ["比用", "知一四絕", this.find_three_pass(this.all_sike()[0][0])];
              }
            }
            if (countOccurrences(relation[0], "上尅下") === 1 && countOccurrences(relation[0], "下賊上") === 3) {
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                findtrue = ["涉害", "度厄", this.find_three_pass(this.all_sike()[3][0])];
              } else {
                findtrue = ["比用", "知一鑄印", this.find_three_pass(this.all_sike()[0][0])];
              }
            }
            if (countOccurrences(relation[0], "上尅下") === 0 && countOccurrences(relation[0], "下賊上") === 3) {
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) !== this.Ganzhiwuxing(this.daygangzhi[0])) {
                findtrue = ["涉害", "度厄四絕", this.find_three_pass(this.all_sike()[2][1])];
              }
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                findtrue = ["涉害", "亂首", this.find_three_pass(this.all_sike()[1][0])];
              }
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                findtrue = ["涉害", "龍戰泆女", this.find_three_pass(this.all_sike()[1][0])];
              } else {
                findtrue = ["比用", "知一不備", this.find_three_pass(this.all_sike()[0][0])];
              }
            }
            if (countOccurrences(relation[0], "上尅下") === 1 && countOccurrences(relation[0], "下賊上") === 2) {
              let flatChars = [];
              for (const item of sike) {
                for (const char of item) flatChars.push(char);
              }
              let counts = getCounts(flatChars);
              let f = Object.entries(counts).filter(([char, count]) => count > 1).map(([char]) => char);

              if (f.length > 2) {
                if (dayganzhi_yy === "陽") {
                  if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                    findtrue = ["比用", "蕪淫", this.find_three_pass(this.all_sike()[2][0])];
                  } else {
                    findtrue = ["比用", "四絕", this.find_three_pass(this.all_sike()[0][0])];
                  }
                } else {
                  findtrue = ["比用", "連茹", this.find_three_pass(this.all_sike()[2][0])];
                }
              } else if (f.length === 2 && this.Ganzhiwuxing(f[0]) === this.Ganzhiwuxing(f[1])) {
                findtrue = ["比用", "乘軒", this.find_three_pass(this.all_sike()[0][0])];
              } else if (f.length <= 1) {
                findtrue = ["涉害", "間傳" + String(f), this.find_three_pass(this.all_sike()[1][0])];
              }
            }
            if (countOccurrences(relation[0], "上尅下") === 0 && countOccurrences(relation[0], "下賊上") === 2) {
              if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                findtrue = ["比用", "知一元胎", this.find_three_pass(this.all_sike()[2][0])];
              }
              if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                findtrue = ["比用", "知一斫輪", this.find_three_pass(this.all_sike()[0][0])];
              }
              if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                if (dayganzhi_yy === "陽") {
                  findtrue = ["比用", "進茹", this.find_three_pass(this.all_sike()[2][0])];
                } else {
                  findtrue = ["比用", "曲直", this.find_three_pass(this.all_sike()[1][0])];
                }
              } else {
                if (this.Ganzhiwuxing(this.hourgangzhi[0]) === "火") {
                  if (dayganzhi_yy === "陽") {
                    if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                      findtrue = ["比用", "龍戰", this.find_three_pass(this.all_sike()[2][0])];
                    }
                    if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) !== this.Ganzhiwuxing(this.daygangzhi[1])) {
                      findtrue = ["涉害", "斬關間傳", this.find_three_pass(this.all_sike()[3][0])];
                    }
                    if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                      let flatChars = [];
                      for (const item of sike) {
                        for (const char of item) flatChars.push(char);
                      }
                      let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                      let counts = getCounts(mappedChars);
                      let filteredCounts = Object.entries(counts).filter(([char, count]) => count > 2).map(([char]) => char);
                      if (filteredCounts.includes(this.Ganzhiwuxing(this.hourgangzhi[0]))) {
                        findtrue = ["比用", "知一元胎", this.find_three_pass(this.all_sike()[2][0])];
                      } else {
                        findtrue = ["涉害", "斬關登三天狡童", this.find_three_pass(this.all_sike()[3][0])];
                      }
                    } else {
                      findtrue = ["賊尅", "重審不備", this.find_three_pass(this.all_sike()[0][0])];
                    }
                  } else {
                    if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                      findtrue = ["比用", "知一稼穡遊子", this.find_three_pass(this.all_sike()[3][0])];
                    } else {
                      findtrue = ["比用", "知一不備四絕", this.find_three_pass(this.all_sike()[0][0])];
                    }
                  }
                } else {
                  if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                    findtrue = ["涉害", "見機順茹", this.find_three_pass(this.all_sike()[0][1])];
                  }
                  if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[1]) === "火") {
                    findtrue = ["涉害", "炎上", this.find_three_pass(this.all_sike()[0][0])];
                  }
                  if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                    findtrue = ["比用", "知一狡童", this.find_three_pass(this.all_sike()[1][0])];
                  } else {
                    if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                      findtrue = ["涉害", "從革", this.find_three_pass(this.all_sike()[1][0])];
                    }
                    if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                      let flatChars = [];
                      for (const item of sike) {
                        for (const char of item) flatChars.push(char);
                      }
                      let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                      let counts = getCounts(mappedChars);
                      let filteredCounts = Object.entries(counts).filter(([char, count]) => count >= 3).map(([char]) => char);

                      if (filteredCounts.length > 0 && filteredCounts[0] === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                        findtrue = ["涉害", "斬關登三天", this.find_three_pass(this.all_sike()[0][1])];
                      }
                      if (filteredCounts.includes(this.Ganzhiwuxing(this.hourgangzhi[1]))) {
                        findtrue = ["比用", "退茹三奇", this.find_three_pass(this.all_sike()[2][0])];
                      } else {
                        let uniqueChars = new Set(mappedChars);
                        if (uniqueChars.size === 5) {
                          findtrue = ["比同", "知一曲直" + String(), this.find_three_pass(this.all_sike()[0][0])];
                        } else {
                          findtrue = ["涉害", "炎上狡童" + String(), this.find_three_pass(this.all_sike()[3][0])];
                        }
                      }
                    } else {
                      if (dayganzhi_yy === "陽") {
                        if (hourganzhi_yy === "陽") {
                          let flatChars = [];
                          for (const item of sike) {
                            for (const char of item) flatChars.push(char);
                          }
                          let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                          let counts = getCounts(mappedChars);
                          let countGt2 = Object.entries(counts).filter(([char, count]) => count >= 2).map(([char]) => char);
                          let countGt3 = Object.entries(counts).filter(([char, count]) => count >= 3).map(([char]) => char);

                          if (countGt2.length > 0 && countGt2[0] === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                            if (countGt3.length > 0 && countGt3[0] === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                              findtrue = ["涉害", "登三天間傳", this.find_three_pass(this.all_sike()[0][0])];
                            }
                            if (countGt3.length > 0 && countGt3[0] === this.Ganzhiwuxing(this.daygangzhi[1])) {
                              findtrue = ["涉害", "炎上斬關狡童", this.find_three_pass(this.all_sike()[3][0])];
                            } else {
                              findtrue = ["比用", "退茹", this.find_three_pass(this.all_sike()[2][0])];
                            }
                          } else {
                            findtrue = ["比用", "退茹", this.find_three_pass(this.all_sike()[0][0])];
                          }
                        } else {
                          let flatChars = [];
                          for (const item of sike) {
                            for (const char of item) flatChars.push(char);
                          }
                          let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                          let counts = getCounts(mappedChars);
                          let countGt3 = Object.entries(counts).filter(([char, count]) => count >= 3).map(([char]) => char);

                          if (countGt3.length > 0 && countGt3[0] === this.Ganzhiwuxing(this.daygangzhi[1])) {
                            findtrue = ["涉害", "間傳涉三淵", this.find_three_pass(this.all_sike()[0][0])];
                          } else if (countGt3.length > 0 && countGt3[0] === this.Ganzhiwuxing(this.daygangzhi[0])) {
                            findtrue = ["賊尅", "重審炎上", this.find_three_pass(this.all_sike()[0][0])];
                          } else {
                            findtrue = ["涉害", "間傳1", this.find_three_pass(this.all_sike()[0][0])];
                          }
                        }
                      } else {
                        try {
                          let flatChars = [];
                          for (const item of sike) {
                            for (const char of item) flatChars.push(char);
                          }
                          let mappedChars = flatChars.map(char => this.Ganzhiwuxing(char));
                          let counts = getCounts(mappedChars);
                          let countGt3 = Object.entries(counts).filter(([char, count]) => count > 3).map(([char]) => char);
                          if (countGt3.length === 0) throw new Error("IndexError");
                          if (countGt3[0] === this.Ganzhiwuxing(this.daygangzhi[1])) {
                            findtrue = ["涉害", "進茹斬關", this.find_three_pass(this.all_sike()[0][0])];
                          } else {
                            findtrue = ["涉害", "間傳2", this.find_three_pass(this.all_sike()[3][0])];
                          }
                        } catch (e) {
                          findtrue = ["比用", "從革", this.find_three_pass(this.all_sike()[0][0])];
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      return findtrue;
    } else if (countOccurrences(relation[0], "上尅下") >= 2 && countOccurrences(relation[0], "下賊上") === 0 && relation[9] === '天地盤沒有返吟') {
      if (filter_list_yy[0] === dayganzhi_yy) {
        if (dayganzhi_yy === "陰") {
          let sikeChars = [];
          for (const item of sike) {
            for (const char of item) sikeChars.push(char);
          }
          if (sikeChars.includes(this.hourgangzhi[1]) || this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[1]) !== this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["涉害", "度厄四絕", this.find_three_pass(this.all_sike()[2][0])];
            }
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
              findtrue = ["比用", "知一從革", this.find_three_pass(this.all_sike()[1][0])];
            } else {
              findtrue = ["比用", "曲直", this.find_three_pass(this.all_sike()[0][0])];
            }
          } else {
            findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][1])];
          }
        }
        if (dayganzhi_yy === "陽" || this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
          findtrue = ["比用", "知一", this.find_three_pass(this.all_sike()[0][0])];
        }
        if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
          if (hourganzhi_yy === "陽") {
            findtrue = ["比用", "知一從革", this.find_three_pass(this.all_sike()[1][0])];
          } else {
            findtrue = ["比用", "元胎斬關", this.find_three_pass(this.all_sike()[0][0])];
          }
        }
      } else if (filter_list_yy[1] === dayganzhi_yy) {
        let sikeChars = [];
        for (const item of sike) {
          for (const char of item) sikeChars.push(char);
        }
        let counts = getCounts(sikeChars);
        let f = Object.entries(counts).filter(([char, count]) => count > 1).map(([char]) => char);

        if (f.length === 1) {
          findtrue = ["比用", "知一", this.find_three_pass(f)];
        } else {
          try {
            let fWuxing = f.map(i => this.Ganzhiwuxing(i));
            let hourgangzhi1Wuxing = this.Ganzhiwuxing(this.hourgangzhi[1]);
            let f1 = fWuxing.indexOf(hourgangzhi1Wuxing);
            if (f1 === -1) throw new Error("ValueError");
            findtrue = ["比用", "知一", this.find_three_pass(f[f1])];
          } catch (e) {
            findtrue = ["比用", "知一斬關", this.find_three_pass(this.all_sike()[3][0])];
          }
        }
      }
      return findtrue;
    }
    return findtrue;
  }

  fiter_four_ke() {
    const rel = this.find_sike_relations();
    const a = rel[7][2];
    const b = rel[7][4];
    if (!Array.isArray(a) || !Array.isArray(b)) return "不適用，或試他法";
    const d = this.duplicates(b, "True");
    const e = this.duplicates(b, "False");
    let ilist = [];
    let jlist = [];
    
    try {
      for (const i of d) {
        ilist.push(a[i]);
      }
      for (const g of e) {
        jlist.push(a[g]);
      }
    } catch (err) {
      if (err instanceof TypeError || (typeof d === 'number' || typeof e === 'number')) {
        ilist = "不適用，或試他法";
      } else {
        throw err;
      }
    }

    if (ilist.length === 0 && jlist.length !== 0) return Array.isArray(jlist) ? jlist.sort() : jlist;
    if (ilist.length === 0 && jlist.length === 0) return "不適用，或試他法";
    if (ilist.length === 3) return Array.from(new Set(ilist)).sort();
    return Array.isArray(ilist) ? ilist.sort() : ilist;
  }

  compare_shehai_number() {
    const a = this.fiter_four_ke();
    if (this.find_sike_relations()[9] === "天地盤返吟" || a === "不適用，或試他法") return ["不適用，或試他法"];
    if (this.find_sike_relations()[7][0] === "試涉害") {
        const c = a.map(i => i[0]);
        const t = a.map(i => i[1]);
        if (this.shigangjigong[t[t.length - 1]] !== undefined) {
            t[t.length - 1] = this.shigangjigong[t[t.length - 1]];
        }
        try {
            const khead = [];
            const earth_n_sky = this.earth_n_sky_list();
            for (let i = 0; i < a.length; i++) {
                khead.push(earth_n_sky[a[i][0]]);
            }
            const biyung_result_reorder_list3 = [];
            for (let i = 0; i < a.length; i++) {
                const biyung_result_reorder = this.new_zhigangcangong_list(khead[i]).slice(0, this.new_zhigangcangong_list(khead[i]).indexOf(a[i][0]) + 1);
                const count = biyung_result_reorder.filter(j => 
                    (this.Ganzhiwuxing(c[i]) + this.Ganzhiwuxing(j)) === (this.Ganzhiwuxing(a[i][0]) + this.Ganzhiwuxing(a[i][1]))
                ).length;
                biyung_result_reorder_list3.push(count);
            }
            const shehai_number2 = biyung_result_reorder_list3.map(s => c[biyung_result_reorder_list3.indexOf(s)]);
            const shehai_dict = Object.fromEntries(biyung_result_reorder_list3.map((s, i) => [s, shehai_number2[i]]));
            
            if (biyung_result_reorder_list3[0] === biyung_result_reorder_list3[1]) {
                return ["找孟仲季地", a, t, c];
            } else if (biyung_result_reorder_list3[0] > biyung_result_reorder_list3[1]) {
                return [shehai_dict[biyung_result_reorder_list3[0]], shehai_dict];
            } else if (biyung_result_reorder_list3[1] > biyung_result_reorder_list3[0]) {
                return [shehai_dict[biyung_result_reorder_list3[1]], shehai_dict];
            }
        } catch (e) { return ["不適用，或試他法"]; }
    }
    return ["不適用，或試他法"];
  }

  shehai() {
        const shangke = this.find_sike_relations()[0];
        const sike = this.all_sike();
        const dayganzhi_yy = this.find_sike_relations()[8];
        const hourganzhi_yy = this.gangzhi_yinyang(this.hourgangzhi[0]);
        let blist = [];
        const z = this.fiter_four_ke();
        for (let i = 0; i < z.length; i++) {
            const b = z[i][0];
            blist.push(b);
        }
        const d = new Set(blist).size;

        const count = (arr, val) => {
            return arr.filter(x => x === val).length;
        };

        if (d === 1 && this.find_sike_relations()[7][0] !== "試涉害") {
            const result = "不適用，或試他法";
            return result;
        } else if (this.compare_shehai_number()[0].length === 1) {
            const reducing = this.compare_shehai_number();
            const result = ["涉害", "涉害", this.find_three_pass(reducing[0])];
            return result;
        } else if (count(shangke, "比和") === 3) {
            const result = "不適用，或試他法";
            return result;
        } else if (count(shangke, "上尅下") === 0 && count(shangke, "下賊上") === 0) {
            const result = "不適用，或試他法";
            return result;
        } else if (this.find_sike_relations()[7][0] === "試比用" && count(shangke, "下賊上") !== 4) {
            const result = "不適用，或試他法";
            return result;
        } else if (count(shangke, "上尅下") === 1 && count(shangke, "下賊上") === 1) {
            const result = "不適用，或試他法";
            return result;
        } else if (count(shangke, "下賊上") === 4) {
            const result = ["返吟", "絕嗣", this.find_three_pass(sike[0][0])];
            return result;
        } else if (count(shangke, "比和") === 2 && count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤返吟") {
            const rel7_1 = this.find_sike_relations()[7][1];
            const chuchuan = this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))];
            const result = ["返吟", "無依", this.find_three_pass(chuchuan[0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤返吟" && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") === 0) {
            const rel7_1 = this.find_sike_relations()[7][1];
            const chuchuan = [this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))], 1];
            const result = ["返吟", "無依", this.find_three_pass(chuchuan[0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤返吟" && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") === 1) {
            const rel7_1 = this.find_sike_relations()[7][1];
            const chuchuan = this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))];
            const result = ["返吟", "涉害", this.find_three_pass(chuchuan[0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") >= 2 && count(this.find_sike_relations()[2], "被尅") === 0) {
            const rel7_1 = this.find_sike_relations()[7][1];
            const chuchuan = this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))];
            const result = ["返吟", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") >= 2 && count(this.find_sike_relations()[2], "被尅") >= 1) {
            const rel7_1 = this.find_sike_relations()[7][1];
            const chuchuan = this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))];
            const result = ["返吟", "涉害", this.find_three_pass(chuchuan[0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") === 1) {
            if (count(this.find_sike_relations()[2], "尅") === 1 && count(this.find_sike_relations()[2], "被尅") === 0) {
                if (this.find_sike_relations()[5] === "被尅") {
                    if (this.find_sike_relations()[8] === "陰") {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    } else {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                        return result;
                    }
                } else {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                }
            } else if (count(this.find_sike_relations()[2], "尅") > 1 && count(this.find_sike_relations()[2], "被尅") === 0) {
                if (this.find_sike_relations()[5] === "被尅") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                } else {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                }
            } else if (count(this.find_sike_relations()[2], "被尅") >= 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][1])];
                return result;
            } else if (count(this.find_sike_relations()[2], "被尅") >= 1 && count(this.find_sike_relations()[2], "尅") >= 1) {
                if (this.find_sike_relations()[5] !== "被尅") {
                    if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                        if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.find_sike_relations()[7][2][0][0])) {
                            const result = ["涉害", "曲直", this.find_three_pass(this.find_sike_relations()[7][2][0][1])];
                            return result;
                        } else {
                            const result = ["涉害", "從革", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                            return result;
                        }
                    } else {
                        const result = ["涉害", "涉害1", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                        return result;
                    }
                } else if (this.find_sike_relations()[5] === "被尅") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                }
            } else {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][1])];
                return result;
            }
        } else if (count(shangke, "下賊上") === 3 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "被尅") >= 1 && count(shangke, "上尅下") === 0) {
            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
            return result;
        } else if (count(shangke, "下賊上") === 3 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") === 1 && count(shangke, "上尅下") === 0) {
            if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 1) {
                if (this.find_sike_relations()[5] !== "被尅" && this.find_sike_relations()[5] !== "尅") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                } else {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                }
            } else if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                return result;
            } else if (count(this.find_sike_relations()[2], "被尅") === 0 && count(this.find_sike_relations()[2], "尅") === 1) {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][1])];
                return result;
            }
        } else if (count(shangke, "下賊上") === 3 && count(shangke, "上尅下") === 1) {
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) !== this.Ganzhiwuxing(this.daygangzhi[0])) {
                const result = ["涉害", "知一度厄", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                return result;
            }
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                const result = ["涉害", "綴瑕四絕", this.find_three_pass(sike[3][0])];
                return result;
            } else {
                if (this.shehai2()[8] === "陰") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][1])];
                    return result;
                }
                if (this.shehai2()[8] === "陽") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][2][0])];
                    return result;
                }
            }
        } else if (count(shangke, "下賊上") === 3 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 1) {
            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
            return result;
        } else if (count(shangke, "下賊上") === 3 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") >= 1) {
            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][2][0])];
            return result;
        } else if (count(shangke, "下賊上") === 4) {
            if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 1) {
                if (this.find_sike_relations()[5] === "被尅" || "尅") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                } else {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][2][0])];
                    return result;
                }
            } else if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                return result;
            } else if (count(this.find_sike_relations()[2], "被尅") === 0 && count(this.find_sike_relations()[2], "尅") === 1) {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                return result;
            } else {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                return result;
            }
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") === 0) {
            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
            return result;
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") >= 1) {
            if (this.find_sike_relations()[5] !== "尅") {
                if (count(this.find_sike_relations()[2], "被尅") > 1) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                } else if (this.find_sike_relations()[5] !== "尅") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                }
            } else if (this.find_sike_relations()[5] === "尅") {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                return result;
            } else {
                const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                return result;
            }
        } else if (count(shangke, "下賊上") === 2 && this.find_sike_relations()[9] === "天地盤沒有返吟" && count(this.find_sike_relations()[2], "尅") > 1) {
            const reducing = this.compare_shehai_number();
            if (reducing[0].length === 1) {
                const result = ["涉害", "涉害", this.find_three_pass(reducing[0])];
                return result;
            } else if (reducing[0] === "找孟仲季地") {
                const converting = this.convert_munchongji_shehai_number();
                if (converting[2][0] === converting[2][1]) {
                    const result = ["返吟", "涉害", this.find_three_pass(converting[2][0])];
                    return result;
                } else if (converting[1][0] + converting[3][0] === "季季") {
                    const result = ["涉害", "涉害", this.find_three_pass(converting[2][0])];
                    return result;
                } else if (converting[1][1] + converting[3][1] === "季季") {
                    const result = ["涉害", "涉害", this.find_three_pass(converting[2][0])];
                    return result;
                } else if (converting[1][0] + converting[3][0] === "孟仲" || "仲孟") {
                    const result = ["涉害", "涉害", this.find_three_pass(converting[2][0])];
                    return result;
                }
            }
        } else if (this.compare_shehai_number().length === 1 && this.compare_shehai_number()[0] === "不適用，或試他法" && this.find_sike_relations()[9] === '天地盤返吟') {
            let result;
            if ([this.find_sike_relations()[7][1]].length === 1) {
                let chuchuan = this.find_sike_relations()[1][1][0];
                result = ["返吟", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
            } else if (this.find_sike_relations()[7][1].length === 2) {
                const rel7_1 = this.find_sike_relations()[7][1];
                let chuchuan = this.find_sike_relations()[7][2][rel7_1.indexOf(this.Max(rel7_1))];
                result = ["返吟", "無依", this.find_three_pass(chuchuan[0])];
            } else if (this.find_sike_relations()[7][1].length >= 3) {
                let chuchuan = this.find_sike_relations()[7][2][this.find_sike_relations()[7][4].indexOf("True")];
                result = ["返吟", "無依", this.find_three_pass(chuchuan[0])];
            }
            return result;
        } else if (this.find_sike_relations()[7][0] === "試涉害") {
            const reducing = this.compare_shehai_number();
            if (JSON.stringify(this.find_sike_relations()[7][2][0]) === JSON.stringify(this.find_sike_relations()[7][2][1])) {
                const chuchuan = this.find_sike_relations()[7][2][0][0];
                const result = ["涉害", "涉害", this.find_three_pass(chuchuan)];
                return result;
            } else if (count(shangke, "上尅下") === 0 && count(shangke, "下賊上") === 0) {
                const result = "不適用，或試他法";
                return result;
            } else if (count(shangke, "上尅下") >= 0 && count(shangke, "下賊上") === 1) {
                const result = "不適用，或試他法";
                return result;
            } else if (count(shangke, "上尅下") === 2 && count(shangke, "下賊上") === 0) {
                if (count(this.find_sike_relations()[2], "尅") >= 1 && count(this.find_sike_relations()[2], "被尅") === 0) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                } else if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    return result;
                } else if (count(this.find_sike_relations()[2], "被尅") > 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                    if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                        const result = ["涉害", "涉害間傳顧祖", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    } else {
                        const result = ["涉害", "涉害間傳", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                        return result;
                    }
                } else if (count(this.find_sike_relations()[2], "被尅") > 1 && count(this.find_sike_relations()[2], "尅") === 0) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                } else if (count(this.find_sike_relations()[2], "被尅") === 1 && count(this.find_sike_relations()[2], "尅") === 1) {
                    if (this.find_sike_relations()[5] === "尅") {
                        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                            const result = ["涉害", "從革驀越", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                            return result;
                        } else {
                            const result = ["涉害", "涉害1", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                            return result;
                        }
                    } else if (this.find_sike_relations()[5] === "被尅") {
                        const allChars = [];
                        for (let item of sike) {
                            for (let char of item) {
                                allChars.push(this.Ganzhiwuxing(char));
                            }
                        }
                        const counter = {};
                        for (let char of allChars) {
                            counter[char] = (counter[char] || 0) + 1;
                        }
                        let gt2Count = 0;
                        for (let key in counter) {
                            if (counter[key] >= 2) gt2Count++;
                        }
                        
                        if (gt2Count > 2) {
                            const result = ["涉害", "間傳見機", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                            return result;
                        } else {
                            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                            return result;
                        }
                    } else if (this.find_sike_relations()[5] === "生") {
                        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                            if (hourganzhi_yy === "陽") {
                                const result = ["涉害", "見機", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                                return result;
                            } else {
                                const result = ["涉害", "見機間傳", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                                return result;
                            }
                        } else {
                            const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                            return result;
                        }
                    } else if (this.find_sike_relations()[5] === "被生") {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                        return result;
                    } else {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    }
                } else {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                }
            } else if (count(shangke, "上尅下") === 4 && count(shangke, "下賊上") === 0) {
                if (this.shehai2()[8] === "陽") {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][1])];
                    return result;
                }
                if (this.shehai2()[8] === "陰") {
                    if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                        const result = ["涉害", "無祿四絕", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    }
                    if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                        const result = ["涉害", "無祿亂首", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    } else {
                        const result = ["涉害", "涉害1", this.find_three_pass(this.find_sike_relations()[7][2][2][0])];
                        return result;
                    }
                }
            } else if (count(shangke, "上尅下") > 2 && count(shangke, "下賊上") === 0) {
                if (reducing[0].length === 1) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                    return result;
                } else if (reducing[0].length > 1 && count(this.find_sike_relations()[2], "尅") === 1) {
                    let result;
                    if (dayganzhi_yy === "陽") {
                        if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                            result = ["涉害", "斬關", this.find_three_pass(this.find_sike_relations()[1][3][0][0])];
                        } else {
                            if (this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                                result = ["比用", "知一四絕", this.find_three_pass(this.find_sike_relations()[1][3][0][0])];
                            }
                            if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[0])) {
                                result = ["涉害", "斬關", this.find_three_pass(sike[2][1])];
                            } else {
                                result = ["涉害1", "涉害", this.find_three_pass(this.find_sike_relations()[1][2][0][0])];
                            }
                        }
                    }
                    if (dayganzhi_yy === "陰") {
                        result = ["涉害1", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][1][0])];
                    }
                    return result;
                } else if (reducing[0].length > 1 && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") === 1) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[1][this.find_sike_relations()[2].indexOf("被尅")][0])];
                    return result;
                } else if (reducing[0].length > 1 && count(this.find_sike_relations()[2], "尅") === 0 && count(this.find_sike_relations()[2], "被尅") > 1) {
                    const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[1][this.find_sike_relations()[2].indexOf("被尅")][0])];
                    return result;
                } else if (reducing[0].length > 1 && count(this.find_sike_relations()[2], "尅") >= 2) {
                    if (count(this.find_sike_relations()[7][4], 'True') === 1 && count(this.find_sike_relations()[7][4], 'False') > 1) {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[1][this.find_sike_relations()[7][4].indexOf("True")][0])];
                        return result;
                    } else if (count(this.find_sike_relations()[7][4], 'True') > 1 && count(this.find_sike_relations()[7][4], 'False') === 1) {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[1][this.find_sike_relations()[7][4].indexOf("False")][0])];
                        return result;
                    } else if (count(this.find_sike_relations()[7][4], 'True') === 0) {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][0])];
                        return result;
                    } else if (count(this.find_sike_relations()[7][4], 'False') === 0) {
                        const result = ["涉害", "涉害", this.find_three_pass(this.find_sike_relations()[7][2][0][1])];
                        return result;
                    }
                } else if (reducing[0] === "不適用，或試他法") {
                    const tail = [];
                    for (let i = 0; i < this.find_sike_relations()[7][2].length; i++) {
                        tail.push(this.find_sike_relations()[7][2][i][1]);
                    }
                    if (tail[0] === this.daygangzhi[0]) {
                        const chuchuan = this.find_sike_relations()[7][2][0][0];
                        const result = ["涉害", "涉害", this.find_three_pass(chuchuan)];
                        return result;
                    } else if (tail[1] === this.daygangzhi[0]) {
                        const chuchuan = this.find_sike_relations()[7][2][1][0];
                        const result = ["涉害", "涉害", this.find_three_pass(chuchuan)];
                        return result;
                    }
                } else if (reducing[0] === "找孟仲季地") {
                    const convert = this.convert_munchongji_shehai_number();
                    const convert_dict_entries = [
                        [convert[0][0] + convert[2][0], convert[1][0] + convert[3][0]],
                        [convert[0][1] + convert[2][1], convert[1][1] + convert[3][1]]
                    ];
                    const convert_dict = {};
                    for (let [k, v] of convert_dict_entries) {
                        convert_dict[k] = v;
                    }
                    const change_daygangzhi = this.shigangjigong[this.daygangzhi[0]];
                    const convert_result_k = Object.keys(convert_dict);
                    const convert_result_v = Object.values(convert_dict);
                    let chuchuan;
                    let name;
                    const dayganzhi_yy2 = this.gangzhi_yinyang(this.daygangzhi[0]);
                    if (convert[2].length === 3) {
                        if (convert[2][0] === change_daygangzhi) {
                            chuchuan = convert[2][0];
                        } else if (convert[2][1] === change_daygangzhi) {
                            chuchuan = convert[2][1];
                        } else if (convert[2][2] === change_daygangzhi) {
                            chuchuan = convert[2][2];
                        }
                        name = "見機";
                    } else if (convert[2].length === 2) {
                        if (convert_result_v[0] === "季孟" || "仲孟") {
                            chuchuan = convert_result_k[1][1];
                            name = "見機";
                        } else if (convert_result_v[0] === "孟季" || "仲季" || "季季") {
                            chuchuan = convert_result_k[1][0];
                            name = "見機";
                        } else if (convert_result_v[0][0] === convert_result_v[0][1]) {
                            if (dayganzhi_yy2 === convert_result_k[0][0]) {
                                chuchuan = convert_result_k[0][0];
                            } else if (dayganzhi_yy2 === convert_result_k[1][0]) {
                                chuchuan = convert_result_k[1][0];
                            }
                            name = "綴瑕";
                        }
                    }
                    const result = ["涉害", name, this.find_three_pass(chuchuan)];
                    return result;
                }
            }
        } else if (count(shangke, "下賊上") >= 3) {
            const reducing = this.compare_shehai_number();
            if (reducing[0].length === 1) {
                const result = ["涉害", "涉害", this.find_three_pass(reducing[0])];
                return result;
            } else {
                const result = "不適用，或試他法";
                return result;
            }
        } else if (count(shangke, "上尅下") === 1 && count(shangke, "下賊上") === 3) {
            const reducing = this.compare_shehai_number();
            if (this.find_sike_relations()[7][0] === "試比用") {
                const result = "不適用，或試他法";
                return result;
            } else if (reducing[0].length === 1) {
                const result = ["涉害", "涉害", this.find_three_pass(reducing[0])];
                return result;
            } else if (reducing[0] === "找孟仲季地") {
                const convert = this.convert_munchongji_shehai_number();
                const convert_dict_entries = [
                    [convert[2][0] + convert[0][0], convert[3][0] + convert[1][0]],
                    [convert[2][1] + convert[0][1], convert[3][1] + convert[1][1]]
                ];
                const convert_dict = {};
                for (let [k, v] of convert_dict_entries) {
                    convert_dict[k] = v;
                }
                const convert_result_k = Object.keys(convert_dict);
                const convert_result_v = Object.values(convert_dict);
                const convert_result_tail = convert_result_k.map(i => i[1]);
                const change_daygangzhi = this.shigangjigong[this.daygangzhi[0]];
                let name;
                if (convert_result_v[0] === "孟季" || "仲季" || "季季") {
                    if (convert_result_v[1][1] === "孟") {
                        if (convert_result_tail[0] || convert_result_tail[1] === change_daygangzhi) {
                            name = "綴瑕";
                        } else {
                            name = "見機";
                        }
                    } else if (convert_result_v[1][1] === "仲") {
                        name = "察微";
                    }
                }
                const chuchuan = convert_result_k[1][0];
                const result = ["涉害", name, this.find_three_pass(chuchuan)];
                return result;
            } else {
                const result = "不適用，或試他法";
                return result;
            }
        }
    }

  yaoke() {
    const sike_relations = this.find_sike_relations();
    if (sike_relations[3] === "日干支同位") return "不適用，或試他法";
    if (sike_relations[4] === "伏吟") return "不適用，或試他法";
    const sike = this.all_sike();
    const sike_list = sike_relations[0];
    const dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);

    if (sike_list.filter(x => x === "下賊上").length === 1 && sike_list.filter(x => x === "上尅下").length === 1) return "不適用，或試他法";
    if (sike_list.filter(x => x === "下賊上").length > 0 || sike_list.filter(x => x === "上尅下").length > 0) return "不適用，或試他法";

    const rel2 = sike_relations[2];
    if (rel2.filter(x => x === "尅").length === 1 && rel2.filter(x => x === "尅").length !== 0) {
        if (sike_relations[6] === "反吟") {
            return ["返吟", "無親", [this.yima_dict[this.hourgangzhi[1]], this.sky_n_earth_list()[this.daygangzhi[1]], this.sky_n_earth_list()[this.shigangjigong[this.shigangjigong[this.daygangzhi[0]]]]]];
        } else {
            return ["遙尅", "遙尅", this.find_three_pass(sike[rel2.indexOf("尅")][0])];
        }
    } else if (rel2.filter(x => x === "尅").length > 1) {
        const d_indices = this.duplicates(rel2, "尅");
        const d_arr = Array.isArray(d_indices) ? d_indices : [d_indices];
        const filterlist = d_arr.map(i => sike[i][0]);
        const filterlist2 = filterlist.map(b => this.gangzhi_yinyang(b));
        const nn_list = filterlist2.map(n => n === dayganzhi_yy ? "True" : "False");
        if (nn_list.includes("True")) {
            return ["遙尅", "蒿矢", this.find_three_pass(sike[d_arr[nn_list.indexOf("True")]][0])];
        } else if (nn_list.includes("False")) {
            if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                return ["遙尅", "元胎", this.find_three_pass(sike[0][1])];
            } else {
                return ["遙尅", "蒿矢", this.find_three_pass(this.daygangzhi[1])];
            }
        }
    } else if (rel2.filter(x => x === "被尅").length === 1) {
        return ["遙尅", "彈射", this.find_three_pass(sike[rel2.indexOf("被尅")][0])];
    } else if (rel2.filter(x => x === "被尅").length === 2) {
        if (sike_relations[6] === "反吟") {
            return ["返吟", "無親", [this.yima_dict[this.hourgangzhi[1]], this.sky_n_earth_list()[this.daygangzhi[1]], this.sky_n_earth_list()[this.shigangjigong[this.daygangzhi[0]]]]];
        } else {
            return ["遙尅", "彈射", this.find_three_pass(sike[rel2.indexOf("被尅")][0])];
        }
    } else if (rel2.filter(x => x === "被尅").length === 0 && rel2.filter(x => x === "尅").length === 0) {
        return "不適用，或試他法";
    }
    return "不適用，或試他法";
  }

  maosing() {
    const sike = this.all_sike();
    const sike_relations = this.find_sike_relations();
    const sike_list = sike_relations[0];
    const dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    const hourganzhi_yy = this.gangzhi_yinyang(this.hourgangzhi[0]);
    const sikehead = sike.map(b => b[0]);
    
    const d = {};
    for (const k of sikehead) {
        d[k] = (d[k] || 0) + 1;
    }
    const res = Object.keys(d).filter(k => d[k] > 1);

    const getVal = (obj, key) => (obj && typeof obj.get === 'function') ? obj.get(key) : obj[key];
    const count = (arr, val) => arr.filter(x => x === val).length;

    let chuchuan;

    if (count(this.find_sike_relations()[2], "尅") > 0) {
        chuchuan = "不適用，或試他法";
        return chuchuan;
    } else if (count(this.find_sike_relations()[0], "上生下") === 4) {
        chuchuan = "不適用，或試他法";
        return chuchuan;
    } else if (count(sike_list, "下賊上") === 0 && count(sike_list, "上尅下") === 0) {
        if (dayganzhi_yy === "陽") {
            try {
                if (res.length === 0) {
                    throw new Error("IndexError");
                }
                if (res[0].length === 1) {
                    chuchuan = "不適用，或試他法";
                    return chuchuan;
                }
                if (res[0].length > 1) {
                    chuchuan = ["昴星", "虎視", [
                        getVal(this.sky_n_earth_list(), "酉"),
                        getVal(this.sky_n_earth_list(), this.daygangzhi[1]),
                        this.all_sike()[3][0]
                    ]];
                    return chuchuan;
                }
            } catch (e) {
                if (this.find_sike_relations()[6] === "反吟") {
                    chuchuan = ["返吟", "無親", [
                        getVal(this.yima_dict, this.daygangzhi[1]),
                        getVal(this.sky_n_earth_list(), this.daygangzhi[1]),
                        getVal(this.sky_n_earth_list(), getVal(this.shigangjigong, this.daygangzhi[0]))
                    ]];
                    return chuchuan;
                } else if (this.find_sike_relations()[6] === "反吟八專") {
                    chuchuan = "不適用，或試他法";
                    return chuchuan;
                } else {
                    chuchuan = ["昴星", "虎視", [
                        getVal(this.sky_n_earth_list(), "酉"),
                        getVal(this.sky_n_earth_list(), this.daygangzhi[1]),
                        this.all_sike()[3][0]
                    ]];
                    return chuchuan;
                }
            }
        }
        if (dayganzhi_yy === "陰") {
            try {
                if (res.length === 0) {
                    throw new Error("IndexError");
                }
                if (res[0].length > 1) {
                    const ganlivezhi = this.shigangjigong;
                    chuchuan = ["昴星", "冬蛇掩目", [
                        getVal(this.earth_n_sky_list(), "寅"),
                        getVal(this.sky_n_earth_list(), getVal(ganlivezhi, this.daygangzhi[0])),
                        this.all_sike()[1][0]
                    ]];
                    return chuchuan;
                }
                if (res[0].length === 1) {
                    chuchuan = "不適用，或試他法";
                    return chuchuan;
                }
            } catch (e) {
                if (this.find_sike_relations()[6] === "反吟") {
                    const ganlivezhi = this.shigangjigong;
                    if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                        if (hourganzhi_yy === "陰") {
                            chuchuan = ["返吟", "無依天網", [
                                getVal(this.earth_n_sky_list(), "亥"),
                                this.all_sike()[1][0],
                                getVal(this.sky_n_earth_list(), getVal(ganlivezhi, this.daygangzhi[0]))
                            ]];
                        } else {
                            if (hourganzhi_yy === "陽") {
                                chuchuan = ["昴星", "掩目", [
                                    getVal(this.hai, sike[0][0]),
                                    sike[3][0],
                                    sike[1][0]
                                ]];
                            } else {
                                chuchuan = ["返吟", "斬關", [
                                    getVal(this.earth_n_sky_list(), "巳"),
                                    this.all_sike()[1][0],
                                    getVal(this.sky_n_earth_list(), getVal(ganlivezhi, this.daygangzhi[0]))
                                ]];
                            }
                        }
                    }
                    if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                        chuchuan = ["返吟", "井欄射", [
                            getVal(this.earth_n_sky_list(), "巳"),
                            this.all_sike()[1][0],
                            this.all_sike()[3][0]
                        ]];
                    } else {
                        chuchuan = ["返吟", "冬蛇掩目", [
                            getVal(this.earth_n_sky_list(), "酉"),
                            getVal(this.sky_n_earth_list(), getVal(ganlivezhi, this.daygangzhi[0])),
                            this.all_sike()[1][0]
                        ]];
                    }
                    return chuchuan;
                } else if (this.find_sike_relations()[6] === "反吟八專") {
                    chuchuan = "不適用，或試他法";
                    return chuchuan;
                } else {
                    const ganlivezhi = this.shigangjigong;
                    chuchuan = ["昴星", "冬蛇掩目", [
                        getVal(this.earth_n_sky_list(), "酉"),
                        getVal(this.sky_n_earth_list(), getVal(ganlivezhi, this.daygangzhi[0])),
                        this.all_sike()[1][0]
                    ]];
                    return chuchuan;
                }
            }
        }
    } else {
        chuchuan = "不適用，或試他法";
        return chuchuan;
    }
  }

  bieze() {
    const sike_relations = this.find_sike_relations();
    const sike_list = sike_relations[0];
    const sike_arr = sike_relations[1].map(i => i[0]);
    if (new Set(sike_arr).size === 4) return "不適用，或試他法";
    if (sike_relations[3] === "日干支同位") return "不適用，或試他法";
    if (sike_relations[4] === "伏吟") return "不適用，或試他法";
    if (sike_list.filter(x => x === "下賊上").length === 0 && sike_list.filter(x => x === "上尅下").length === 0) {
        const dayganzhi_yy = sike_relations[8];
        const sky_n_earth = this.sky_n_earth_list();
        if (dayganzhi_yy === "陽") {
            const sky_ganhe = { "甲": "己", "乙": "庚", "丙": "辛", "丁": "壬", "戊": "癸" };
            const ganhe_result1 = this.shigangjigong[sky_ganhe[this.daygangzhi[0]] || this.daygangzhi[0]];
            if (sike_relations[6] === "反吟八專") return "不適用，或試他法";
            return ["別責", "別責", [sky_n_earth[ganhe_result1], sky_n_earth[this.shigangjigong[this.daygangzhi[0]]], sky_n_earth[this.shigangjigong[this.daygangzhi[0]]]]];
        } else {
            const sep = { "巳酉丑": "巳酉丑", "寅午戌": "寅午戌", "亥卯未": "亥卯未", "申子辰": "申子辰" };
            const result = this.multi_key_dict_get(sep, this.daygangzhi[1]);
            const res_arr = result ? result.split("") : [];
            const position = res_arr.indexOf(this.daygangzhi[1]);
            let a_val;
            if (position === 0) a_val = res_arr[1];
            else if (position === 1) a_val = res_arr[2];
            else if (position === 2) a_val = res_arr[0];
            
            if (sike_relations[6] === "反吟八專") return "不適用，或試他法";
            if (sike_relations[6] === "非反吟") {
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                    return ["別責", "不備", [res_arr[2], sike_arr[3], sike_arr[3]]];
                } else {
                    return ["別責", "不備", [res_arr[2], res_arr[0], res_arr[0]]];
                }
            } else {
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                    if (sike_list.filter(x => x === "比和").length === 3) return ["別責", "蕪淫", [res_arr[0], sike_arr[3], sike_arr[3]]];
                    else return ["別責", "斬關", [res_arr[0], sike_arr[0], sike_arr[0]]];
                } else {
                    if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                        return ["別責", "蕪淫", [res_arr[0], sike_arr[0], sike_arr[0]]];
                    } else {
                        const gzwx_counts = {};
                        sike_arr.forEach(char => {
                            const wx = this.Ganzhiwuxing(char);
                            gzwx_counts[wx] = (gzwx_counts[wx] || 0) + 1;
                        });
                        const majority_wx = Object.keys(gzwx_counts).find(wx => gzwx_counts[wx] > 3);
                        if (majority_wx === this.Ganzhiwuxing(this.daygangzhi[1])) {
                            if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                                return ["別責", "斬關寡宿", ["巳", this.hourgangzhi[1], this.hourgangzhi[1]]];
                            } else {
                                if (this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
                                    return ["別責", "斬關不備", ["巳", sike_arr[0], sike_arr[0]]];
                                } else {
                                    return ["返吟", "無親", [this.hourgangzhi[1], sike_arr[1], sike_arr[0]]];
                                }
                            }
                        } else {
                            return ["別責", "蕪淫", [res_arr[0], res_arr[2], res_arr[2]]];
                        }
                    }
                }
            }
        }
    }
    return "不適用，或試他法";
  }

  bazhuan() {
    const sike_relations = this.find_sike_relations();
    const sike_list = sike_relations[0];
    const sike = sike_relations[1];
    const bazhuan_dgz = "壬子,甲寅,乙卯,丁巳,己未,庚申,辛酉,癸亥".split(",");
    const dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    const sky_n_earth = this.sky_n_earth_list();
    const earth_n_sky = this.earth_n_sky_list();

    const count = (arr, val) => arr.filter(x => x === val).length;

    if (bazhuan_dgz.includes(this.daygangzhi)) {
      if (count(sike_list, "下賊上") === 1 && count(sike_list, "上尅下") === 1) {
        return "不適用，或試他法";
      } else if (count(sike_list, "下賊上") > 0 || count(sike_list, "上尅下") > 0) {
        return "不適用，或試他法";
      } else if (sike_relations[4] === "伏吟") {
        return "不適用，或試他法";
      } else if (count(sike_list, "比和") === 4) {
        const first = sky_n_earth[sky_n_earth[this.yimadict[this.daygangzhi[1]]]];
        return ["八專", "八專斬關勵德", [first, sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.shigangjigong[this.daygangzhi[0]]]]];
      } else if (count(sike_list, "下生上") === 4) {
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) !== this.Ganzhiwuxing(this.daygangzhi[1])) {
          return ["八專", "帷簿", [sky_n_earth[this.he[this.hourgangzhi[1]]], sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
        }
        if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1]) && this.Ganzhiwuxing(this.hourgangzhi[0]) === this.Ganzhiwuxing(this.daygangzhi[1])) {
          const po_val = this.po[earth_n_sky[sike[0][0]]];
          return ["八專", "帷簿勵德", [sky_n_earth[this.hai[po_val]], sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
        }
        if (this.hourgangzhi[1] === "寅") {
          return ["八專", "獨足", [sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
        }
        if (this.hourgangzhi[1] === "丑") {
          return ["八專", "帷簿寡宿", [this.hourgangzhi[1], sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
        }
        return "不適用，或試他法";
      } else if (count(sike_list, "比和") === 2 && count(sike_list, "下生上") === 2) {
        return ["八專", "帷簿", [sike[1][1], sike[1][0], sike[1][0]]];
      } else if (count(sike_list, "比和") === 2 && count(sike_list, "上生下") === 2) {
        if (this.hourgangzhi[1] === "卯") {
          return ["八專", "帷簿三奇", [sky_n_earth[sike[0][0]], sike[1][0], sike[1][0]]];
        } else {
          return ["八專", "帷簿", [this.po[sike[1][0]], sike[1][0], sike[1][0]]];
        }
      } else if (count(sike_list, "上生下") === 4) {
        if (this.hourgangzhi[1] === "巳") {
          return ["八專", "八專", [earth_n_sky[this.daygangzhi[1]], sike[1][0], sike[1][0]]];
        } else {
          return ["八專", "帷簿孤辰", [sky_n_earth[sike[0][0]], sike[1][0], sike[1][0]]];
        }
      } else if (count(sike_list, "比和") === 3) {
        const first = sky_n_earth[sky_n_earth[this.yimadict[this.daygangzhi[1]]]];
        return ["八專", "帷簿", [first, sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.shigangjigong[this.daygangzhi[0]]]]];
      } else if (sike_relations[6] === "反吟八專" && sike_relations[4] === "伏吟") {
        return ["返吟", "無親", [this.yimadict[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.shigangjigong[this.daygangzhi[0]]]]];
      } else if (sike_relations[3] === "日干支同位") {
        if (count(sike_list, "下賊上") === 0 && count(sike_list, "上尅下") === 0) {
          if (dayganzhi_yy === "陽") {
            const pos = this.Zhi[(this.Zhi.indexOf(sike[3][0]) + 2) % 12];
            return ["八專", "八專", [pos, sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
          } else {
            const pos = this.Zhi[(this.Zhi.indexOf(sike[0][0]) - 2 + 12) % 12];
            return ["返吟", "井欄射", [pos, sky_n_earth[this.daygangzhi[1]], sky_n_earth[this.daygangzhi[1]]]];
          }
        }
      }
    }
    return "不適用，或試他法";
  }

  fuyin() {
    let dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    const unique = (list1) => {
      const unique_list = [];
      for (const x of list1) {
        if (!unique_list.includes(x)) {
          unique_list.push(x);
        }
        return x;
      }
    };
    const pyIndex = (arr, val) => {
      const idx = arr.indexOf(val);
      if (idx === -1) throw new Error("ValueError");
      return idx;
    };

    const sike = this.all_sike();
    const sike_list = this.find_sike_relations();
    dayganzhi_yy = this.gangzhi_yinyang(this.daygangzhi[0]);
    let chuchuan;

    try {
      if (sike_list[4] === "非伏吟" && this.zeike().length > 2 && this.shehai().length > 2) {
        if (dayganzhi_yy === "陽") {
          chuchuan = [
            "伏吟", "自任",
            [
              this.shigangjigong[this.daygangzhi[0]],
              this.ying[this.shigangjigong[this.daygangzhi[0]]],
              this.ying[this.ying[this.shigangjigong[this.daygangzhi[0]]]]
            ]
          ];
          return chuchuan;
        }
        if (dayganzhi_yy === "陰") {
          try {
            const counts = {};
            for (const item of sike) {
              for (const char of item) {
                const w = this.Ganzhiwuxing(char);
                counts[w] = (counts[w] || 0) + 1;
              }
            }
            const gt3 = Object.entries(counts).filter(([k, v]) => v > 3).map(([k, v]) => k);
            
            if (gt3.length === 0) throw new Error("IndexError");
            
            if (gt3[0] === this.Ganzhiwuxing(this.daygangzhi[1])) {
              try {
                const gt7 = Object.entries(counts).filter(([k, v]) => v >= 7).map(([k, v]) => k);
                if (gt7.length > 0) {
                  chuchuan = ["八專", "井欄射勵德", ["巳", sike[3][0], sike[3][0]]];
                } else {
                  throw new Error("ValueError");
                }
              } catch (e) {
                if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                  chuchuan = ["八專", "帷簿斬關", ["亥", sike[3][0], sike[3][0]]];
                } else {
                  chuchuan = ["伏吟", "無依", [sike[3][0], this.shigangjigong[this.daygangzhi[0]], sike[3][0]]];
                }
              }
            } else {
              if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.hourgangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                  chuchuan = ["八專", "帷簿", ["丑", sike[1][0], sike[1][0]]];
                } else {
                  chuchuan = ["八專", "帷簿", [this.po[sike[1][0]], sike[1][0], sike[1][0]]];
                }
              } else {
                chuchuan = ["伏吟", "杜傳", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], this.ying[this.daygangzhi[1]]]];
              }
            }
          } catch (e) {
            chuchuan = ["遙尅", "蒿矢", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], this.ying[this.daygangzhi[1]]]];
          }
        }
        
        let countXiaShengShang = sike_list[0].filter(x => x === "下生上").length;
        let countBiHe = sike_list[0].filter(x => x === "比和").length;
        if (countXiaShengShang === 4) {
          chuchuan = ["八專", "獨足", [sike[1][0], sike[1][0], sike[1][0]]];
        } else if (countXiaShengShang === 2 && countBiHe === 2) {
          chuchuan = ["八專", "帷簿", [sike[1][1], sike[1][0], sike[1][0]]];
        } else {
          chuchuan = ["遙尅", "蒿矢11", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], this.ying[this.daygangzhi[1]]]];
        }
        return chuchuan;
      }
      
      if (sike_list[4] === "伏吟") {
        let countShangKeXia = sike_list[0].filter(x => x === "上尅下").length;
        let countXiaZeiShang = sike_list[0].filter(x => x === "下賊上").length;
        
        if (countShangKeXia === 1 && countXiaZeiShang === 0) {
          const u = unique(sike_list[1]);
          chuchuan = ["伏吟", "不虞", [u[0], this.ying[u[0]], this.ying[this.ying[u[0]]]]];
          return chuchuan;
        } else if (countXiaZeiShang === 1 && countShangKeXia === 0) {
          const u = unique(sike_list[1]);
          if (dayganzhi_yy === "陽") {
            chuchuan = ["伏吟", "自任", [u[0], this.ying[u[0]], this.ying[this.ying[u[0]]]]];
          }
          if (dayganzhi_yy === "陰") {
            const idx = pyIndex(sike_list[0], "下賊上");
            if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
              chuchuan = ["伏吟", "自信社傳", [sike_list[1][idx][0], u[0], this.hai[sike_list[1][idx][0]]]];
            } else {
              chuchuan = ["伏吟", "自任1", [sike_list[1][idx][0], u[0], this.ying[u[0]]]];
            }
          }
          return chuchuan;
        } else if (countShangKeXia === 0 && countXiaZeiShang === 0) {
          if (dayganzhi_yy === "陽") {
            if (this.multi_key_dict_get(this.ying_chong_dict, this.shigangjigong[this.daygangzhi[0]]) === "刑") {
              chuchuan = ["伏吟", "自任", [this.shigangjigong[this.daygangzhi[0]], this.ying[this.shigangjigong[this.daygangzhi[0]]], this.ying[this.ying[this.shigangjigong[this.daygangzhi[0]]]]]];
              return chuchuan;
            } else if (this.multi_key_dict_get(this.ying_chong_dict, this.shigangjigong[this.daygangzhi[0]]) === "自刑") {
              if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                chuchuan = ["伏吟", "元胎", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], "巳"]];
              }
              if (this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[1])) {
                chuchuan = ["伏吟", "三奇杜傳", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], this.ying[sike[0][0]]]];
              } else {
                chuchuan = ["伏吟", "三奇杜傳", [this.shigangjigong[this.daygangzhi[0]], this.daygangzhi[1], this.hai[this.hourgangzhi[1]]]];
              }
              return chuchuan;
            }
          } else if (dayganzhi_yy === "陰") {
            if (this.multi_key_dict_get(this.ying_chong_dict, this.shigangjigong[this.daygangzhi[1]]) === "刑") {
              if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.daygangzhi[0]) !== this.Ganzhiwuxing(this.hourgangzhi[0])) {
                chuchuan = ["伏吟", "三交", [this.daygangzhi[1], this.hai[sike[3][0]], this.he[sike[3][0]]]];
              } else if (this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[1]) && this.Ganzhiwuxing(this.daygangzhi[1]) === this.Ganzhiwuxing(this.hourgangzhi[0]) && this.Ganzhiwuxing(this.daygangzhi[0]) === this.Ganzhiwuxing(this.hourgangzhi[0])) {
                chuchuan = ["伏吟", "稼穡", ["未", "丑", "戌"]];
              } else {
                chuchuan = ["伏吟", "自任", [this.shigangjigong[this.daygangzhi[1]], this.ying[this.shigangjigong[this.daygangzhi[1]]], this.ying[this.ying[this.shigangjigong[this.daygangzhi[1]]]]]];
              }
              return chuchuan;
            } else if (this.multi_key_dict_get(this.ying_chong_dict, this.shigangjigong[this.daygangzhi[1]]) === "自刑") {
              if (dayganzhi_yy === "陽") {
                chuchuan = ["伏吟", "杜傳", [this.shigangjigong[this.daygangzhi[1]], this.ying[this.chong2[this.ying[this.shigangjigong[this.daygangzhi[0]]]]], this.ying[this.ying[this.chong2[this.ying[this.shigangjigong[this.daygangzhi[0]]]]]]]];
              }
              if (dayganzhi_yy === "陰") {
                chuchuan = ["伏吟", "杜傳1", [this.shigangjigong[this.daygangzhi[1]], this.shigangjigong[this.daygangzhi[0]], this.po[sike[2][0]]]];
              }
              return chuchuan;
            }
            chuchuan = ["伏吟", "自信", [this.daygangzhi[1], this.ying[this.daygangzhi[1]], this.chong2[this.daygangzhi[1]]]];
            return chuchuan;
          }
        }
      }
    } catch (e) {
      return "不適用，或試他法";
    }
    return "不適用，或試他法";
  }

  dinhorse() {
    const dinhorsedict = { "甲子": "卯", "甲戌": "丑", "甲申": "亥", "甲午": "酉", "甲辰": "未", "甲寅": "巳" };
    return this.multi_key_dict_get(dinhorsedict, this.liujiashun_dict[this.daygangzhi]);
  }

  moonhorse() {
    const moonhorsedict = { "寅申": "午", "卯酉": "申", "辰戌": "戌", "巳亥": "子", "午子": "寅", "丑未": "辰" };
    return this.multi_key_dict_get(moonhorsedict, this.daygangzhi[1]);
  }

  dayhorse() {
    return { "子": "寅", "丑": "亥", "寅": "申", "卯": "巳", "辰": "寅", "巳": "亥", "午": "申", "未": "巳", "申": "寅", "酉": "亥", "戌": "申", "亥": "巳" }[this.daygangzhi[1]];
  }

  guiren_starting_gangzhi(num) {
    const guiren_dict = {
        "甲": {"晝": "未", "夜": "丑"}, "戊庚": {"晝": "丑", "夜": "未"}, "丙": {"晝": "酉", "夜": "亥"},
        "丁": {"晝": "亥", "夜": "酉"}, "壬": {"晝": "卯", "夜": "巳"}, "癸": {"晝": "巳", "夜": "卯"},
        "乙": {"晝": "申", "夜": "子"}, "己": {"晝": "子", "夜": "申"}, "辛": {"晝": "寅", "夜": "午"}
    };
    const guiren_dict2 = {
        "甲,戊庚": {"晝": "丑", "夜": "未"}, "乙己": {"晝": "子", "夜": "申"}, "丙丁": {"晝": "亥", "夜": "酉"},
        "壬癸": {"晝": "巳", "夜": "卯"}, "辛": {"晝": "午", "夜": "寅"}
    };
    const option = { 0: guiren_dict2, 1: guiren_dict };
    const get_day = this.multi_key_dict_get(option[num], this.daygangzhi[0]);
    const find_day_or_night = this.multi_key_dict_get(this.daynight_richppl_dict, this.hourgangzhi[1]);
    return get_day ? get_day[find_day_or_night] : null;
  }

  guiren_start_earth(num) {
    return this.earth_n_sky_list()[this.guiren_starting_gangzhi(num)];
  }

  guiren_order_list(num) {
    const starting_gangzhi = this.guiren_starting_gangzhi(num);
    const rotation = { "巳午未申酉戌": "逆佈", "亥子丑寅卯辰": "順佈" };
    const new_zhi_list_guiren = this.new_zhi_list(starting_gangzhi);
    const guiren = this.guiren_start_earth(num);
    const rotation_results = this.multi_key_dict_get(rotation, guiren);
    const pai_gui = this.new_list(this.sky_generals, "貴");
    if (rotation_results === "順佈") {
        return Object.fromEntries(new_zhi_list_guiren.map((z, i) => [z, pai_gui[i]]));
    } else {
        return Object.fromEntries(new_zhi_list_guiren.map((z, i) => [z, this.new_list(this.sky_generals.slice().reverse(), "貴")[i]]));
    }
  }

  result(num) {
    const answer = [this.zeike(), this.biyung(), this.shehai(), this.yaoke(), this.maosing(), this.bieze(), this.bazhuan(), this.fuyin()];
    const ju_three_pass = answer.filter(i => i !== "不適用，或試他法");
    if (ju_three_pass.length === 0) throw new Error("無效課式");
    
    const sky_earth = this.sky_n_earth_list();
    const sky = Object.values(sky_earth);
    const earth = Object.keys(sky_earth);
    const guiren_order_list_2 = this.guiren_order_list(num);
    const guiren_order_list_3 = sky.map(i => guiren_order_list_2[i]);
    const earth_to_general = Object.fromEntries(earth.map((e, i) => [e, guiren_order_list_3[i]]));
    
    const ju = [ju_three_pass[0][0], ju_three_pass[0][1]];
    const three_pass_zhi = ju_three_pass[0][2];
    const three_pass_generals = three_pass_zhi.map(i => guiren_order_list_2[i]);
    const day_gz_vs_three_pass = three_pass_zhi.map(i => {
        const combine = (this.Ganzhiwuxing(this.daygangzhi[0]) || "") + (this.Ganzhiwuxing(i) || "");
        const rel = this.multi_key_dict_get(this.wuxing_relation_2, combine);
        return this.liuqing_dict[rel];
    });

    const three_pass = {
        "初傳": [three_pass_zhi[0], three_pass_generals[0], day_gz_vs_three_pass[0], this.shunkong(this.daygangzhi, three_pass_zhi[0])],
        "中傳": [three_pass_zhi[1], three_pass_generals[1], day_gz_vs_three_pass[1], this.shunkong(this.daygangzhi, three_pass_zhi[1])],
        "末傳": [three_pass_zhi[2], three_pass_generals[2], day_gz_vs_three_pass[2], this.shunkong(this.daygangzhi, three_pass_zhi[2])]
    };

    const sike_zhi = this.all_sike();
    const sike_generals = sike_zhi.map(i => guiren_order_list_2[i[0]]);
    const sike_formatted = {
        "四課": [sike_zhi[0], sike_generals[0]],
        "三課": [sike_zhi[1], sike_generals[1]],
        "二課": [sike_zhi[2], sike_generals[2]],
        "一課": [sike_zhi[3], sike_generals[3]]
    };

    return {
        "農曆月": this.cmonth, "節氣": this.jieqi, "日期": this.daygangzhi + "日" + this.hourgangzhi + "時",
        "格局": ju, "日馬": this.dayhorse(), "三傳": three_pass, "四課": sike_formatted,
        "天地盤": { "天盤": sky, "地盤": earth, "天將": guiren_order_list_3 },
        "地轉天盤": sky_earth, "地轉天將": earth_to_general
    };
  }

  result_d(num) {
    const res = this.result(num);
    res["日期"] = this.daygangzhi + "月" + this.hourgangzhi + "日";
    return res;
  }

  result_m(num) {
    const res = this.result(num);
    res["日期"] = this.daygangzhi + "時" + this.hourgangzhi + "分";
    return res;
  }

  jinkou(zhi) {
    return { "地分": zhi };
  }
}
