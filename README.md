# Trading Automation Main

Central control plane for the Trading Automation platform. The main service exposes a FastAPI REST interface, manages trading groups and accounts in Redis, and orchestrates gRPC connections to 
distributed [Trading-Automation-Worker](https://github.com/roieGolst/Trading-Automation-Worker) nodes.

## System Architecture

- **FastAPI REST API** (`app/api/app.py`) – handles group creation, account activation/deactivation, and transaction requests.
- **gRPC Orchestrator** (`app/service/grpc/GrpcService.py`) – listens for worker ping requests, spins up bidirectional channels, and wraps each worker in a trading stub.
- **Redis Persistence** (`app/db/RedisDB.py`) – stores groups, account state, and credential metadata.
- **Logging Layer** (`app/logger.py`) – streams structured logs to stdout and rotates them into `trading_automation.log`.

```
┌────────────────────────┐      Ping/Pong + Task Streams      ┌─────────────────────────┐
│ Trading-Automation-Main│◀──────────────────────────────────▶│Trading-Automation-Worker│
├────────────────────────┤                                    ├─────────────────────────┤
│ FastAPI REST API       │      Activation / Transaction      │   AutoRSA task runner   │
│ Redis group registry   │◀──────┬────────────────────────────┤   gRPC task handlers    │
│ gRPC connection hub    │       │                            │                         │
└────────────────────────┘    Clients                         └─────────────────────────┘
        ▲
        │ JSON HTTP
        │
   REST Consumers
```

<details>
<summary>Worker Communication Flow (ASCII)</summary>

```
                             ┌────────────────────────────┐
                             │        REST Clients        │
                             └────────────┬───────────────┘
                                          │ JSON/HTTPS
                                          ▼
                   ┌────────────────────────────────────────────┐
                   │        Trading Automation Main             │
                   │────────────────────────────────────────────│
                   │    FastAPI Layer                           │
                   │                                            │
                   │   ┌────────────────────────────────────┐   │
                   │   │  Router (/createGroup,/activate)   │   │
                   │   └────────────────┬───────────────────┘   │
                   │                    │ look up group stub    │
                   │   ┌────────────────▼───────────────────┐   │
                   │   │      DefaultGroupHandler           │   │
                   │   │  • queues new groups               │   │
                   │   │  • maps groups → worker stubs      │   │
                   │   │  • replays tasks on reconnect      │   │
                   │   └────────────────┬───────────────────┘   │
                   │                    │ persist metadata      │
                   │   ┌────────────────▼───────────────────┐   │
                   │   │             RedisDB                │   │
                   │   │  • group registry                  │   │
                   │   │  • account creds & status          │   │
                   │   └────────────────┬───────────────────┘   │
                   │                    │ worker lifecycle      │
                   │    gRPC Control Plane                      │
                   │   ┌────────────────▼───────────────────┐   │
                   │   │   MainTradingService (Ping)        │   │
                   │   │  • waits for worker Ping           │   │
                   │   │  • extracts worker callback addr   │   │
                   │   └────────────────┬───────────────────┘   │
                   │                    │ host:port             │
                   │   ┌────────────────▼───────────────────┐   │
                   │   │   Trading Stub (per worker)        │   │
                   │   │  • holds gRPC channel              │   │
                   │   │  • forwards activation/txn RPCs    │   │
                   │   │  • watches channel health          │   │
                   │   └────────────────┬───────────────────┘   │
                   └────────────────────┼───────────────────────┘
                                        │ secure gRPC
                                        ▼
             ┌────────────────────────────────────────────────────────┐
             │              Trading Automation Worker                 │
             │────────────────────────────────────────────────────────│
             │  Ping Client  → sends Ping with callback port          │
             │  gRPC Server  ← receives activation/deactivation/etc   │
             │  Strategy Runtime → executes trading logic             │
             │  Trading Adapter → talks to brokerage/exchange         │
             └────────────────────────────────────────────────────────┘
```

</details>

## Capabilities

- Orchestrates worker registration and reconnection via gRPC keepalive.
- Provides REST operations for group lifecycle (`POST /createGroup`), account activation/deactivation, and sample transaction triggers.
- Persists account credentials and status to Redis; rebuilds activation queues when workers disconnect.
- Converts REST payloads into strongly typed protobuf tasks with brokerage-specific credential validation.
- Supports containerized deployment with Docker/Docker Compose and includes a starter AWS ECS Terraform stack.

## Prerequisites

- Python 3.9+
- Redis 5.0+ (development and production data store)
- uv (recommended Python package manager) or pip
- Docker & Docker Compose for containerized runs
- Matching worker image deployed and reachable over gRPC

## Getting Started (Local)

1. **Clone**
   ```bash
   git clone <repository-url>
   cd Trading-Automation-Main
   ```

2. **Install uv** (if needed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```
   This creates `.venv` (if missing) and installs the locked dependencies from `uv.lock`.

4. **Generate protobuf stubs**
   ```bash
   uv run bash scripts/proto_build.sh
   ```

5. **Run Redis locally** (Docker example):
   ```bash
   docker run -d --name redis -p 6379:6379 redis:alpine
   ```

6. **Launch the API server**
   ```bash
   uv run fastapi run app/main.py --reload
   ```
   - REST API available on `http://127.0.0.1:8000`
   - gRPC server listens on `0.0.0.0:50052` (from `app/main.py` bootstrap parameters)

## Docker & Compose

- **Build image**
  ```bash
  docker build -t trading-main .
  ```

- **Prebuild worker image** (from [Trading-Automation-Worker](https://github.com/roieGolst/Trading-Automation-Worker))
  ```bash
  docker build -t ta-worker:latest .
  ```
  The compose stack depends on this tag, so build the worker image before `docker compose up`.

- **Run with workers + Redis**
  ```bash
  docker compose up --build
  ```
  Exposes REST (8000), gRPC (50052), and Redis (6379). The compose file expects a `ta-worker:latest` image.

## Configuration

- Update default bootstrap settings (Redis host/port, gRPC bind address) in `app/main.py`.
- `app/logger.py` writes structured logs to stdout and `trading_automation.log`. Rotate or relocate that file for production.
- Environment variables are not wired yet—extend `BootstrapParams` or introduce a config layer before production use.

## REST API Reference

### `POST /createGroup`
- Body: `group_name` (query or JSON string)
- Response: "Group created" or 400 if duplicate.

### `POST /activate`
```json
{
  "group_name": "growth-club",
  "account_name": "acct-42",
  "brokerage": "Robinhood",
  "cred": {
    "USERNAME": "user@example.com",
    "PASSWORD": "••••••",
    "TOTP_OR_NA": "123456"
  }
}
```
- Validates brokerage-specific fields, forwards to active worker, persists account metadata in Redis, returns 200 on success.

### `POST /deactivate`
- Parameters: `group_name`, `account_name`
- Marks account inactive in Redis and instructs worker to disable it.

### `POST /transaction`
- Parameters: `group_name`
- Sends a sample buy order (`AAPL`, qty 1). Extend the payload for production workflows.

Swagger UI: `http://127.0.0.1:8000/docs` (when running with `fastapi run --reload`).

## gRPC Worker Lifecycle

1. Worker container starts and sends `Ping` to main server (`MainTradingService`).
2. Main server parses peer address, dials worker’s gRPC endpoint, and constructs `_Stub` wrapper.
3. Stub exposes activation/deactivation/transaction RPCs with credential casting safeguards.
4. Connectivity watchers handle idle/failed connections and trigger task replay on reconnect.

## Development Tasks

- **gRPC protos**: `uv run bash scripts/proto_build.sh`
- **Tests**: `uv run pytest` (ensure Redis is running locally)
- **Linting**: Introduce `ruff`/`flake8`/`black` as needed; not yet defined in `pyproject.toml`.

## Project Layout

```
app/
├── main.py                  # FastAPI app bootstrap
├── bootstarp.py             # Redis + gRPC initialization
├── api/                     # REST routers & models
├── db/RedisDB.py            # Redis-backed persistence layer
├── data/DefaultGroupHandler.py # Worker allocation & reconnection logic
├── service/grpc/            # gRPC server, stubs, and generated code
├── common/Response.py       # Generic response wrapper
scripts/proto_build.sh       # Protobuf compilation script
docker-compose.yml           # Local stack (main, worker, redis)
terraform-aws/              # ECS sample deployment definitions
test/db/test_RedisDB.py      # RedisDB unit tests
```

## Observability & Ops

- Logs stream to stdout and `trading_automation.log` (rotate in production).
- gRPC keepalive tuned via `GrpcOptions` defaults (10s ping interval, 5s timeout).
- Ensure TLS, secrets management, and credential storage hardening before production usage.
