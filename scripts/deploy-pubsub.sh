#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="${DIR}/../src"

source "${DIR}/.env.local"

gcloud functions \
  deploy ${_FUNCTION_NAME_PUBSUB} \
  --source=${_SOURCE_DIR} \
  --runtime=python39 \
  --trigger-topic=${_PUBSUB_TOPIC}