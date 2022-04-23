#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="${DIR}/../src"

source "${DIR}/.env.local"

gcloud functions \
  deploy ${FUNCTION_NAME_PUBSUB} \
  --source=${SOURCE_DIR} \
  --runtime=python39 \
  --trigger-topic=${PUBSUB_TOPIC}