# 前端部署

在 CharacterAI\front 路径下：<br>

1. 修改“/CharacterAI/front/src/plugins”路径下的 global.js 文件中的后端部署 IP 和端口 <br>

2. 修改 nginx.conf 中的 server_name 为你的服务器 IP <br>

3. 创建前端的 docker 镜像，其中 agent_ai 是设置的镜像名称：

```
docker build . -t agent_ai
```

4. 在后台运行前端，其中 8900 是主机端口，80 是容器内部端口

```
docker run -d -p 8900:80 agent_ai
```

### 参考资料

https://cli.vuejs.org/guide/deployment.html#docker-nginx
