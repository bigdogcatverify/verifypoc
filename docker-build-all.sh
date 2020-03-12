#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd ${DIR}/verify-core > /dev/null
  docker build -t verify-core .
popd > /dev/null

pushd ${DIR}/verify-block > /dev/null
  docker build -t verify-block .
popd > /dev/null

pushd ${DIR}/verify-block/frontend > /dev/null
  docker build -t verify-block-frontend .
popd > /dev/null
