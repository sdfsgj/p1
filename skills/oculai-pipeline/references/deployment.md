# Oculai Deployment Reference

## Local

Run:

```powershell
python server.py
```

Open:

```text
http://localhost:8000
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## GitHub

Expected flow:

```powershell
git status --short --branch
git add .
git commit -m "Describe change"
git push
```

If no remote exists:

```powershell
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## Render

The repo should include:

- `render.yaml`
- `Procfile`
- `requirements.txt`

`server.py` should read `PORT` and bind to `0.0.0.0`.

## Environment

Use `.env.example` as the template for:

- `OCULAI_DATABASE_URL`
- `OCULAI_GITHUB_TOKEN`
- `OCULAI_SEMANTIC_SCHOLAR_KEY`
- `OCULAI_HTTP_TIMEOUT_SECONDS`
- `OCULAI_EMBEDDING_MODEL`

Do not commit real secrets.

