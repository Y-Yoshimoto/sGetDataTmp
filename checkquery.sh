#!/bin/bash
## Check pipeline query ShellScript
if [ $# -ne 1 ]; then
  echo "usage: checkquery.sh PipelinequeryName" 1>&2
  exit 1
fi
Pipelinequery="./accessormongo/code/piplineQuery/"$1".json"
if [ ! -e $Pipelinequery ]; then
  echo "Pipelinequery not exists."
  exit 1
fi
upDataJq=$1"_result.json"
upDataPath="./uploadvolume/"$upDataJq
# MongoDBへのクエリー発行
curl --noproxy "*" -sS -L -X GET -o upDataPath http://localhost:35000/data/pipeline/$1 > $upDataPath
# Boxに取得結果を保存
curl --noproxy "*" -sS -L -X POST -o /dev/null http://localhost:35001/upload/pipelinedata/$upDataJq 
