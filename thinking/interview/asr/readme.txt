
docker buildx build --platform linux/amd64,linux/arm64 -t kylin-cn-shanghai.cr.volces.com/poc/asr:0.1.1 --push .
docker run -it --rm --name test -p 5000:5000 kylin-cn-shanghai.cr.volces.com/poc/asr:0.1.1

curl -s -X POST http://alb-3vtxmniggcirk6096psm9wchy.cn-shanghai.volcalb.com/citic/asr -H "Content-Type: application/json" -d '{"appid": "", "access_token": "", "file_url": "https://pub-kylin.tos-cn-beijing.volces.com/0001/201.mov"}' 

curl -X POST http://127.0.0.1:5000/asr -H "Content-Type: application/json" -d '{"appid": "your_appid", "access_token": "your_access_token", "file_url": "https://example.com/your_video_file.mov"}'



