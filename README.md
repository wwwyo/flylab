# flylab

Playground for poking at the fruit fly connectome (MaleCNS v1.0, 166,700 neurons) as a spiking network, via the [`flybrain`](https://pypi.org/project/flybrain/) package.

## Getting Started

```bash
mise install
uv sync
uv run loom-escape/main.py   # looming -> giant-fiber escape circuit
```

Each PoC lives in its own directory, with a matching `docs/<poc>/` note on what it builds and what it checks. The brain files (~260 MB) download to `~/fly-data` on first run.
