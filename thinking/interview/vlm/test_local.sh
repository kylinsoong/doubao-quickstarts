#!/bin/bash

# 检查必要的环境变量是否已设置
if [ -z "$ARK_API_KEY" ] || [ -z "$ARK_API_ENGPOINT_ID" ]; then
    echo "错误: 需要设置 ARK_API_KEY 和 ARK_API_ENGPOINT_ID 环境变量"
    echo "示例: export ARK_API_KEY=your_api_key ARK_API_ENGPOINT_ID=your_endpoint_id"
    exit 1
fi

# 使用优化的 curl 命令调用 API
curl -X POST -H "Content-Type: application/json" -d "{
    \"api_key\": \"$ARK_API_KEY\",
    \"endpoint\": \"$ARK_API_ENGPOINT_ID\",
    \"prompt\": \"分析视频内容\",
    \"video_url\": \"https://pub-kylin.tos-cn-beijing.volces.com/0001/201.mov\"
}" http://127.0.0.1:5000/avlm
