# Model Server

## Development server

Start the API with autoreload:

```bat
run_dev_server.bat
```

Or run it manually:

```bash
uv run uvicorn model:app --host 127.0.0.1 --port 8001 --reload
```