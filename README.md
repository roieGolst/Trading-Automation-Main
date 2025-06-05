# Trading Automation

This repository contains the main server component for a trading automation platform. The project coordinates multiple worker nodes via gRPC while exposing a REST API for management tasks. Account information is persisted in Redis.

## Features

- **FastAPI** HTTP API with endpoints for creating groups, activating users, deactivating accounts and making transactions.
- **gRPC** service used to communicate with worker processes.
- **Redis** database implementation for storing groups and accounts.

## Directory Structure

- `app/main.py` – Application entry point. Bootstraps services and attaches API routes.
- `app/bootstarp.py` – (typo in file name) Initializes the Redis layer, the group handler singleton and the gRPC service.
- `app/api/` – FastAPI routers and request models.
- `app/db/` – Redis backed `IDatabase` implementation.
- `app/data/` – `DefaultGroupHandler` that manages stubs to worker nodes.
- `app/service/grpc/` – gRPC server, stubs and protobuf definitions.
- `scripts/proto_build.sh` – Helper script to compile protobuf files into Python modules.

## Getting Started

1. **Install dependencies**

   ```bash
   poetry install
   ```

2. **Generate gRPC code**

   ```bash
   ./scripts/proto_build.sh
   ```

   This populates `app/service/grpc/proto/dist_main` and `dist_worker` with the generated modules.

3. **Run a local Redis instance**

   The server expects Redis to be available on `localhost:6379` by default.

4. **Start the application**

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Running Tests

Tests are located under the `test/` directory and can be executed with:

```bash
pytest
```

## Notes

The worker side of the trading system is not included in this repository. Only the gRPC interfaces are defined here.
