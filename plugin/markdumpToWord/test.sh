#!/bin/bash

MD_CONTENT=$(cat sample.md)  # 或直接赋值： MD_CONTENT="## Hello\nThis is a test."

response=$(jq -n --arg md "$MD_CONTENT" '{md: $md}' | \
  curl -s -w "\nHTTP_STATUS:%{http_code}\n" -X POST \
    http://alb-3vtxmniggcirk6096psm9wchy.cn-shanghai.volcalb.com/convert \
    -H "Content-Type: application/json" \
    -d @-)

body=$(echo "$response" | sed -n '1,/HTTP_STATUS:/p' | sed '$d')
status=$(echo "$response" | grep HTTP_STATUS | cut -d':' -f2)

if [ "$status" -eq 200 ]; then
  echo "✅ 请求成功："
  echo "$body"
else
  echo "❌ 请求失败，HTTP 状态码：$status"
  echo "响应内容："
  echo "$body"
fi

