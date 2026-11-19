[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/soedirman566-stack/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/soedirman566-stack/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The Global Ledger — 18 November 2026 in one image

Entry for the make.fun **news-image-20261118** bounty: sum up the world news of
Wednesday, 18 November 2026 in a single image.

`main.py` is a small offline compositor (Python + Pillow). It assembles a
1024×1024 newspaper front page from the committed assets — a hero photograph of
Trump's arrival in Shenzhen for the three-way APEC summit with Xi and Putin,
panels on the U.S.–Iran tanker escalation in Hormuz and Ukraine's second-night
strike on the Kerch Bridge, and a text column covering Anthropic's record
$81.3B raise, the Democrats holding the Senate 56–44, and Israeli forces
entering Gaza.

## Run

```sh
python3 main.py [output_dir]   # or set MAKEFUN_OUTPUT_DIR
```

Writes `entry.png` (JPEG-encoded, ≤1024×1024, ≤1 MiB) into the output
directory (default `/output`). The program is deterministic: same assets in,
byte-identical image out. No network access is needed or used.

## License

MIT — see [LICENSE](LICENSE).
