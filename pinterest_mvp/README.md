# Pinterest Python MVP (v2)

This toolkit helps you run a repeatable Pinterest workflow:

1. Generate pin copy variants
2. Render pin images (optional, requires Pillow)
3. Create a publish queue CSV
4. Clone high-performing title variants

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r pinterest_mvp/requirements.txt
```

## Run the workflow

### 1) Generate copy

```bash
python3 pinterest_mvp/main.py generate-copy \
  --url "https://example.com/post" \
  --topic "small balcony garden" \
  --keyword "balcony garden ideas"
```

### 2) Render pins (optional)

```bash
python3 pinterest_mvp/main.py render --copy-file pinterest_mvp/output/pin_copy.json
```

If Pillow is unavailable, skip render and continue with queueing.

### 3) Build publish queue

```bash
python3 pinterest_mvp/main.py queue \
  --copy-file pinterest_mvp/output/pin_copy.json \
  --board "Balcony Garden" \
  --publish-start "2026-05-06T12:00:00"
```

### 4) Clone winners from metrics

Create a metrics file with columns: `title,ctr,save_rate`

```bash
python3 pinterest_mvp/main.py clone-winners \
  --metrics-file pinterest_mvp/output/metrics.csv \
  --ctr-threshold 0.03 \
  --save-threshold 0.05 \
  --variants 5
```

## Tests

```bash
python3 -m unittest discover -s pinterest_mvp/tests -p 'test_*.py'
```
