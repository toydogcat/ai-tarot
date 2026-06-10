import { Liuren } from './src/engines/daliurenEngine.js';

const [jieqi, cmonth, day_gz, hour_gz] = process.argv.slice(2);
if (!jieqi || !cmonth || !day_gz || !hour_gz) {
  console.error("Missing arguments: jieqi cmonth day_gz hour_gz");
  process.exit(1);
}

try {
  const lr = new Liuren(jieqi, cmonth, day_gz, hour_gz);
  const res = lr.result(0);
  console.log(JSON.stringify(res));
} catch (e) {
  console.log(JSON.stringify({ error: e.message, stack: e.stack }));
}
