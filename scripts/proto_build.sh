#!/bin/bash

cd "$(dirname "$0")/.." || {
  echo "Failed to navigate to the project root"
  exit 1
}

cd app/service/grpc/_proto || {
  echo "Failed to navigate to app/service/grpc/proto"
  exit 1
}

WORKER_PROTO_DIR="worker_proto"
MAIN_PROTO_DIR="main_proto"
WORKER_PROTO_DIST="dist_worker"
MAIN_PROTO_DIST="dist_main"

mkdir $WORKER_PROTO_DIST
mkdir $MAIN_PROTO_DIST

poetry run python -m grpc_tools.protoc \
  -I $WORKER_PROTO_DIR/ \
  --python_out=$WORKER_PROTO_DIST/ \
  --grpc_python_out=$WORKER_PROTO_DIST/ \
  --mypy_out=$WORKER_PROTO_DIST/ \
  ./$WORKER_PROTO_DIR/*._proto

protol \
  --create-package \
  --in-place \
  --python-out $WORKER_PROTO_DIST/ \
  protoc --_proto-path=$WORKER_PROTO_DIR/ WorkerTradingService._proto

echo "Worker protos files generated successfully"

poetry run python -m grpc_tools.protoc \
  -I $MAIN_PROTO_DIR/ \
  --python_out=$MAIN_PROTO_DIST/ \
  --grpc_python_out=$MAIN_PROTO_DIST/ \
  --mypy_out=$MAIN_PROTO_DIST/ \
  ./$MAIN_PROTO_DIR/*._proto

protol \
  --create-package \
  --in-place \
  --python-out $MAIN_PROTO_DIST/ \
  protoc --_proto-path=$MAIN_PROTO_DIR/ MainTradingService._proto

echo "Main protos files generated successfully"