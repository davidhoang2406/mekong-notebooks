# mekong-notebooks

JupyterLab notebooks for exploring and reporting on Mekong market data.

## Structure

```
notebooks/
  exploration/   # ad-hoc data exploration (Avro, raw snapshots)
  reporting/     # structured analysis (Parquet OHLCV, indicators)
  onboarding/    # walkthroughs for new team members
model/
  minio_store.py # read-only MinIO wrapper
  spark.py       # SparkSession factory (S3A/MinIO pre-wired)
docker/
  jupyter.Dockerfile
```

## Quick start

```bash
cp .env.example .env          # adjust if not using default Docker stack
docker build -f docker/jupyter.Dockerfile -t mekong-notebooks .
docker run --rm -p 8888:8888 \
  --env-file .env \
  -v $(pwd)/notebooks:/opt/project/notebooks \
  mekong-notebooks
# → http://localhost:8888
```

Or point at the shared `mekong-infra` Docker Compose stack which includes a `jupyter` service.

## Rules

- **Never write back to MinIO** — notebooks are read-only consumers.
- **No cell outputs committed** — enforced by the `nbstripout` pre-commit hook.
- **Production logic** extracted from a notebook belongs in `mekong-jobs`, not here.

## Pre-commit setup

```bash
pip install pre-commit nbstripout
pre-commit install
```

## Dependencies

See `requirements.txt`. Install locally with:

```bash
pip install -r requirements.txt
```
