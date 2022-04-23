#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="${DIR}/../src"

gcloud functions \
  deploy "tweet-news" \
  --source="/" \
  --runtime=python39 \
  --trigger-topic="tweet"