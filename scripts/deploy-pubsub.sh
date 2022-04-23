#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

gcloud functions \
  deploy "tweet-news" \
  --source="${DIR}/.." \
  --runtime=python39 \
  --trigger-topic="tweet"