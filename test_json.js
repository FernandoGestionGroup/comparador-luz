const strings = [
  "1Error",
  "0Error",
  "1a",
  " 1a",
  "{}x",
  "[]a",
  "\"\"a",
  "1",
  "413 Request Entity Too Large",
  "500 Internal Server Error",
  "502 Bad Gateway",
  "504 Gateway Timeout",
  "A error occurred",
  "<!DOCTYPE html>",
  "<html>"
];

for (const s of strings) {
  try {
    JSON.parse(s);
  } catch (e) {
    if (e.message.includes("position 1")) {
      console.log(`MATCHED position 1: ${s} -> ${e.message}`);
    }
  }
}
