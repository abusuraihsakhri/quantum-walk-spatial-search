# Quantum Walk Spatial Search

Exact continuous-time quantum-walk search on **complete graphs**, with a local browser simulator, Python CLI, and a FastAPI endpoint. The repository also retains a separate legacy threshold-audit framework.

## Browser simulator

Use the GitHub Pages deployment when available. To run locally from the repository root:

```bash
python -m http.server 8080
```

Open http://localhost:8080/web/ in a modern browser.

Set the number of vertices, marked-vertex index, hopping rate, and simulation duration. The application plots marked-vertex measurement probability against time and exports the sampled curve as CSV. The interface works without a Python server, account, network request, external JavaScript library, or Pyodide.

## Mathematical model

For the complete graph K_N, the model starts from the uniform superposition and evolves under

`H = −γA − |w⟩⟨w|`

where A is the zero-diagonal adjacency matrix and w is the marked vertex. Complete-graph symmetry gives an exact two-dimensional reduction. With γ = 1/N, ideal success probability reaches 1 at t = π√N/2 (ℏ = 1). This models an ideal closed system only: no noise, readout effects, or hardware performance claims. **Arbitrary graphs and discrete-time coined walks are not implemented.**

The peak shown in the user interface is the maximum among sampled points, not a continuously optimized maximum. Node count is limited to 2–100,000, hopping rate to (0, 10,000], sample count to 2–2,001, and time to (0, 100,000].

## Python CLI

Requires Python 3.9 or newer. The numerical search itself uses only the standard library.

```bash
python -m pip install -e .
quantum-walk-search --nodes 64 --marked 0 --samples 401
quantum-walk-search --nodes 64 --csv probabilities.csv
```


For REST API and legacy audit commands, install the optional server dependencies:

```bash
python -m pip install -e '.[server]'
python cli.py serve --host 127.0.0.1 --port 8000
```


Send JSON to `POST /api/quantum/search`:

```bash
curl -s -X POST http://127.0.0.1:8000/api/quantum/search \
  -H 'Content-Type: application/json' \
  -d '{"node_count":64,"marked_vertex":0,"samples":201}'
```


Both FastAPI implementations also expose this endpoint. The established legacy commands (`python cli.py audit`, `batch`, `chat`, `verify-audit`) remain available, as does the installed `quantum-walk-spatial-search` command for the separate `quantum_walk` threshold-audit CLI. Those audit modules evaluate configurable generic thresholds; they **do not** implement quantum-walk algorithms or validate clinical/cryptographic standards.

## Testing

```bash
python -m pip install -e '.[server,test]'
python -m pytest -q
node --test tests/test_web.mjs
```


CI tests Python 3.10–3.12, checks the browser-engine equations with Node.js, and runs a dependency vulnerability audit. The repository includes a GitHub Actions Pages workflow publishing only the `web/` directory; the repository's Pages source must be configured for GitHub Actions.

## Docker

Generate a distinct random key before running the API container:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```


The container runs as a non-root user and binds port 8000 to localhost by default. Do not use the formerly committed example audit key; change it if it was ever deployed.

## Privacy, scope and limitations

- The static browser simulator performs calculations entirely in the browser, does not persist inputs, and does not send them to a backend.
- REST API requests go to the server you choose to run. The legacy audit framework keeps an in-process HMAC-chained audit ledger; it is not durable across restarts.
- Legacy mock-LLM and regular-expression PHI guard components are demonstrations, not clinical decision support, HIPAA compliance certification, NIST conformance, or real connections to third-party LLM providers.
- The browser application needs a modern browser supporting JavaScript ES modules and SVG. No Python-in-browser runtime is needed.

## License

MIT — see [LICENSE](LICENSE).
