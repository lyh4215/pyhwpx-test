📁 전체 디렉토리 구조
project/
 ├─ queue/
 │   ├─ pending/
 │   ├─ processing/
 │   ├─ done/
 │   ├─ failed/
 │   └─ workers/
 ├─ tasks.py
 ├─ worker.py
 ├─ supervisor.py
 └─ api.py

1️⃣ 작업 정의 (tasks.py)
```python
import time
import random

def heavy_task(x):
    time.sleep(3)
    if random.random() < 0.2:
        raise RuntimeError("random failure")
    return x * x
```


2️⃣ 파일 큐 유틸 (queue_utils 개념 – worker 안에 포함)

핵심 포인트:

os.replace → atomic

lock ❌

3️⃣ Worker (worker.py)
```python
import os, json, time, argparse, traceback
from tasks import heavy_task

BASE = "queue"
PENDING = f"{BASE}/pending"
PROCESSING = f"{BASE}/processing"
DONE = f"{BASE}/done"
FAILED = f"{BASE}/failed"
WORKERS = f"{BASE}/workers"

TIMEOUT = 10  # seconds


def heartbeat(worker_id, status, job_id=None):
    path = f"{WORKERS}/{worker_id}.json"
    with open(path, "w") as f:
        json.dump({
            "worker_id": worker_id,
            "pid": os.getpid(),
            "status": status,
            "job_id": job_id,
            "ts": time.time()
        }, f)


def dequeue():
    files = os.listdir(PENDING)
    if not files:
        return None

    job = files[0]
    src = f"{PENDING}/{job}"
    dst = f"{PROCESSING}/{job}"

    try:
        os.replace(src, dst)  # atomic
        return dst
    except FileNotFoundError:
        return None


def process_job(path):
    with open(path) as f:
        job = json.load(f)

    job_id = job["id"]
    heartbeat(WORKER_ID, "busy", job_id)

    try:
        result = heavy_task(*job["args"])
        job["result"] = result
        os.replace(path, f"{DONE}/{job_id}.json")
    except Exception:
        job["error"] = traceback.format_exc()
        with open(f"{FAILED}/{job_id}.json", "w") as f:
            json.dump(job, f)
        os.remove(path)


def worker_loop():
    heartbeat(WORKER_ID, "idle")
    while True:
        job_path = dequeue()
        if not job_path:
            heartbeat(WORKER_ID, "idle")
            time.sleep(1)
            continue

        process_job(job_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    WORKER_ID = args.id

    os.makedirs(WORKERS, exist_ok=True)
    worker_loop()
```


4️⃣ Supervisor (supervisor.py)

worker 생성 / 감시 / 재시작
```python
import subprocess, time, os, json

NUM_WORKERS = 3
WORKER_CMD = ["python", "worker.py"]

workers = {}


def start_worker(i):
    wid = f"worker-{i}"
    p = subprocess.Popen(WORKER_CMD + ["--id", wid])
    workers[wid] = p
    print(f"[supervisor] started {wid} (pid={p.pid})")


def reap_dead_workers():
    for wid, p in list(workers.items()):
        if p.poll() is not None:
            print(f"[supervisor] {wid} died, restarting...")
            start_worker(wid.split("-")[1])


def requeue_stale_jobs():
    now = time.time()
    for f in os.listdir("queue/processing"):
        path = f"queue/processing/{f}"
        if now - os.path.getmtime(path) > 15:
            print(f"[supervisor] requeue stale job {f}")
            os.replace(path, f"queue/pending/{f}")


if __name__ == "__main__":
    for i in range(NUM_WORKERS):
        start_worker(i)

    while True:
        reap_dead_workers()
        requeue_stale_jobs()
        time.sleep(5)
```

5️⃣ 작업 enqueue + 상태 조회 API (api.py)
```python
import os, json, uuid, time
from fastapi import FastAPI

BASE = "queue"
PENDING = f"{BASE}/pending"

app = FastAPI()

os.makedirs(PENDING, exist_ok=True)


@app.post("/enqueue/{x}")
def enqueue(x: int):
    job = {
        "id": str(uuid.uuid4()),
        "task": "heavy_task",
        "args": [x],
        "created_at": time.time()
    }
    path = f"{PENDING}/{job['id']}.json"
    with open(path, "w") as f:
        json.dump(job, f)

    return {"job_id": job["id"]}


@app.get("/status")
def status():
    return {
        "pending": len(os.listdir("queue/pending")),
        "processing": len(os.listdir("queue/processing")),
        "done": len(os.listdir("queue/done")),
        "failed": len(os.listdir("queue/failed")),
        "workers": list(os.listdir("queue/workers")),
    }
```


실행:

uvicorn api:app --port 8000

6️⃣ 이 시스템이 뭘 보장하나

✔ 다중 worker 병렬 처리
✔ worker 죽으면 자동 재시작
✔ 중간에 죽은 job은 requeue
✔ lock-free (atomic rename)
✔ Windows / 폐쇄망 OK

👉 사실상 간이 Celery + Redis 대체