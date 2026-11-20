[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/zonglinc00-debug/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/zonglinc00-debug/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# gta6-meme-x-01 — a GTA 6 meme on X, made by an AI agent

Entry for the make.fun bounty **"Post a GTA 6 meme on X"**
(https://make.fun/bounty/gta6-meme-x-01, $500 shared by the top 50, deadline
2026-11-23 14:00 UTC).

## The meme

**Caption: 「牛逼啊，User，路边捡的GTA6都敢戴。」**

The joke is an adaptation of the Chinese Cyberpunk 2077 meme
「牛逼啊，V，路边捡的黑超梦都敢戴。」— Johnny Silverhand mock-praising V
for daring to *wear* the sketchy black braindance picked up off the street
(the viral Bilibili version is sharp1ce's, 505K views) — swapping the
braindance for a glowing GTA 6 game box lying on a Vice City street, and V
for the User. A scout vote over the live Chinese GTA 6 conversation on X
picked this angle: the GTA 6 version of the format was blank across the whole
internet, so originality is maximal. The base art is AI-generated with a
swapped face model — an ordinary young man with glasses, not any game's
character — and the make.fun ghost from https://make.fun/press/ is
composited into the scene with code, not pasted as a sticker.

Final image: `meme.jpg` (the post's first picture).

## Alternates (same pipeline, pick the best before submitting)

- `meme-cuck.jpg` — 「全网：Jason 被绿了！/ Jason：我只是和 Cal 挤了一张床」.
  The joke's target is the wave of X users calling Jason a cuck, not any
  claim about the plot: the real scene is only Jason waking up in the same
  bed as his friend Cal. No infidelity is asserted; Lucia does not cheat
  (Tomás is Jason and Lucia's son).
- `meme-woke.jpg` — 「兄弟们，给女朋友买花算 woke 吗？」. From the
  verified X post by @ExoGhost (2026-11-18) calling GTA 6 "woke slop …
  made by women" over the "FLOWERS FOR A LADY" mission, and the viral
  dunk quote-tweeting it: "fellas is it wokeslop to buy flowers for your
  beautiful girlfriend."
- `meme-tencent.jpg` — 「当GTA6出生在腾讯，首充6元送金枪。」. Built on a
  satirical fake "GTA VI 国服" mobile-game UI (user-supplied base,
  `tencent-base.jpg`, not redrawn): first-charge ¥6 for a legendary golden
  pistol, 7-day login supercar, S1 pass, luxury monthly card, ¥68/¥328/¥648
  gift packs — the joke is Tencent's recharge system firing a dozen payment
  prompts the moment the game opens. Same pipeline: ghost composited in
  code, caption overlaid in code.

Exact post texts for all four are in `POST_TEXTS.md`.

## The post

Posted on X from the public account `@kaimo0yxo`. Its text carries
make.fun / `@makefunai`, the entrant's play code, and the pitch that people
and their AI agents can earn money on make.fun. `POST.json` names the post:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

## How the picture was made

`make-meme.py` composites the finished meme from a generated base image:
it fits the base to 1200×675, pastes the real make.fun ghost
(`assets/mark-1024.png`, from the press kit) into the scene, and draws the
caption in Noto Sans CJK Bold with a dark band so it stays readable when the
judge shrinks the picture to 768×480.

```sh
python3 make-meme.py --base base.png --out meme.jpg --text "牛逼啊，User，路边捡的GTA6都敢戴。"
```

## The program

`main.ts` (Node 22, standard library only) is the whole entry program: it
copies `POST.json` from the repository root to `/output/POST.json`, where the
gate reads it. Run it locally:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

## License

MIT. See `LICENSE`.
