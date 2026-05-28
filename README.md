# mekong-notebooks

JupyterLab notebooks for exploring and reporting on Mekong market data.
**Read-only consumer** of MinIO — notebooks never write back to production
buckets.

## Layout

```
notebooks/
  exploration/   # ad-hoc data exploration (Avro snapshots, recent ticks)
  reporting/     # structured analysis (Parquet OHLCV, indicators, screener)
  onboarding/    # walkthroughs for new contributors
model/
  minio_store.py # MinIO read wrapper
  spark.py       # SparkSession factory (S3A/MinIO pre-wired, local[*] mode)
Dockerfile       # Jupyter image (built by CI)
```

## Run inside the K8s cluster

Once `mekong-infra` is deployed, JupyterLab is reachable at:

```
http://jupyter.mekong.local
```

The pod definition lives in `mekong-infra/k8s/mekong-dev/jupyter-deployment.yaml`.
It mounts the notebooks directory and has MinIO credentials wired in via
the `minio-credentials` secret.

## Run standalone (local Docker)

```bash
cp .env.example .env          # adjust if not pointing at the K8s stack
docker build -t mekong-notebooks .
docker run --rm -p 8888:8888 \
  --env-file .env \
  -v $(pwd)/notebooks:/opt/project/notebooks \
  mekong-notebooks
# → http://localhost:8888
```

## Rules

- **Never write back to MinIO** — notebooks are read-only consumers.
- **No cell outputs committed** — enforced by the `nbstripout` pre-commit hook.
- **Production logic** extracted from a notebook belongs in `mekong-jobs`,
  not here.

## Pre-commit setup

```bash
pip install pre-commit nbstripout
pre-commit install
```

## Dependencies

See `requirements.txt` for notebook-side packages (matplotlib, plotly, pandas,
pyarrow, s3fs). Install locally with:

```bash
pip install -r requirements.txt
```

## Depends on

- [`mekong-data-models`](https://github.com/davidhoang2406/mekong-data-models) — schemas + topic constants for reading
- `mekong-infra` — running Kafka + MinIO stack
