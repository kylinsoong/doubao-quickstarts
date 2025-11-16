
Setup below services before execute the scripts:

- 云数据库 PostgreSQL
- 缓存数据库 Redis 
- 云向量数据库 Milvus 
- 应用型负载均衡
- TOS 


Exwcute the following step by step(The last one need create on UI):

kubectl apply -f dify-common.yaml
kubectl apply -f dify-sandbox-ssrf.yaml
kubectl apply -f dify-api.yaml
kubectl apply -f dify-worker.yaml
kubectl apply -f dify-web.yaml
kubectl apply -f dify-ingress.yaml
