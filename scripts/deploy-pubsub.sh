#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="${DIR}/../src"

gcloud functions \
  deploy ${_FUNCTION_NAME_PUBSUB} \
  --source=${_SOURCE_DIR} \
  --runtime=python39 \
  --trigger-topic=${_PUBSUB_TOPIC}