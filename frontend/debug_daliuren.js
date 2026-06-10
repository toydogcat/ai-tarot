import { Liuren } from './src/engines/daliurenEngine.js';

const jieqi = "小雪";
const cmonth = "十二";
const day_gz = "辛卯";
const hour_gz = "甲戌";

const lr = new Liuren(jieqi, cmonth, day_gz, hour_gz);
console.log("Sike:", lr.all_sike());
const rel = lr.find_sike_relations();
console.log("Relations[0]:", rel[0]);
console.log("biyung:", JSON.stringify(lr.biyung()));
