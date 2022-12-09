#!/usr/bin/env bash
docker run -v $(pwd):/app --workdir=/app --rm -it $(docker build -q .) "$@"