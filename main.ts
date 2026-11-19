// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself: an AI agent made a GTA 6 meme, it was posted
// on X from a public account, and POST.json at this repository's root names
// the post's address. All this program has to do is hand that address to the
// gate, by writing POST.json into /output/POST.json.
//
// It reads the file as bytes and writes the same bytes out, so the copy is
// exact. It also parses the JSON to make sure the post address is really
// there, and prints the post's host so the run log shows what was handed in.
// A placeholder address is only warned about, never rejected here: the gate
// itself decides whether an address is a real post.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// then out/POST.json is byte for byte this directory's POST.json.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const SOURCE = join(BOT_DIR, 'POST.json');
const TARGET = join(OUTPUT_DIR, 'POST.json');

function fail(message: string): never {
  console.error(`gta6-meme-x-01: ${message}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });

let raw: Buffer;
try {
  raw = readFileSync(SOURCE);
} catch (err) {
  fail(`could not read ${SOURCE}: ${(err as Error).message}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(raw.toString('utf8'));
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}

if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  fail('POST.json must be a JSON object like {"url": "https://x.com/..."}');
}
const url = (parsed as { url?: unknown }).url;
if (typeof url !== 'string' || url.length === 0) {
  fail('POST.json must carry a "url" string naming the X post');
}

if (url.includes('<handle>') || url.includes('<id>')) {
  console.warn('gta6-meme-x-01: warning: POST.json still holds the placeholder address');
} else {
  try {
    console.log(`gta6-meme-x-01: handing in post ${new URL(url).host}${new URL(url).pathname}`);
  } catch {
    console.log(`gta6-meme-x-01: handing in post ${url}`);
  }
}

try {
  writeFileSync(TARGET, raw);
} catch (err) {
  fail(`could not write ${TARGET}: ${(err as Error).message}`);
}
