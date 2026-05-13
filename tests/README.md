# API Smoke Tests

These tests are small scripts for checking that the official `millionaire_client`
package can talk to the PoliMillionaire server before running the full notebook.

They make real API calls. Use them sparingly.

## Run

From the project root:

```powershell
python tests/test_api_smoke.py
```

By default the script logs in, lists competitions, starts one text game, and
prints the current question shape. It does not submit an answer unless you pass
`--answer-first-option`.

## Environment Variables

The script has defaults matching the starter notebook, but you can override them:

```powershell
$env:POLI_MILLIONAIRE_URL = "http://131.175.15.22:51111/"
$env:POLI_MILLIONAIRE_USERNAME = "MarianoAkaMery"
$env:POLI_MILLIONAIRE_PASSWORD = "Test1234!"
python tests/test_api_smoke.py
```
