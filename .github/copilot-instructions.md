# Copilot Instructions for smartpredict_stock

This repository is a tiny single-script data fetcher. Use these notes to be immediately productive when editing or extending the project.

- **Big picture:** `fetch_stock.py` downloads historical price data via `yfinance` and writes `stock_data.csv` to the repository root. There is no service boundary or server: it's a command-line script intended for data retrieval.

- **Key file:** `fetch_stock.py` — change `TICKER` (uppercase config) and `period` to alter behavior. Example: `TICKER = "TSLA"`, `period="5y"`.

- **Dependencies & install:** the script requires `yfinance` and `pandas`. Install with:

```bash
pip install yfinance pandas
```

- **Run / debug:**
  - Run normally: `python fetch_stock.py` (writes `stock_data.csv`).
  - If you see no output, try unbuffered mode: `python -u fetch_stock.py`.
  - Quick checks: `python -c "import yfinance,pandas; print('ok')"` to verify packages.

- **Project-specific patterns:**
  - Single-file script, minimal structure. Configuration is inline (uppercase constants). Prefer small edits over heavy refactors when adding quick data tasks.
  - Output is a CSV in the current working directory — downstream scripts/readers will expect `stock_data.csv` in repo root.

- **Integration points & caveats:**
  - `yfinance` scrapes Yahoo Finance; it requires network access and can fail silently when rate-limited or when ticker is invalid.
  - No retries or backoff are implemented — if adding production use, add retry logic and explicit error handling.

- **Troubleshooting checklist (when `fetch_stock.py` shows no output):**
  1. Confirm the script ran: check exit code in the terminal (0 = ran without uncaught exceptions).
  2. Verify packages: run `pip show yfinance pandas` or `pip list`.
  3. Confirm network/remote access: `python -c "import socket; print(socket.gethostbyname('finance.yahoo.com'))"`.
  4. Run with unbuffered stdout: `python -u fetch_stock.py`.
  5. Add quick instrumentation to `fetch_stock.py`:

```python
print('starting')
try:
    df = yf.download(TICKER, period="1y")
    print('downloaded rows', getattr(df, 'shape', None))
except Exception as e:
    print('error', e)
```

  6. If `df` is empty, print `df.shape` and `df.columns` to inspect what's returned.

- **If you modify files:** keep changes small and add a short comment header noting why. There are no tests in this repo — run the script locally to validate behavior.

If you'd like, I can add a small `requirements.txt`, wrap `fetch_stock.py` in a `main()` with better diagnostics, and run it here to debug the "no output" case. What should I do next?