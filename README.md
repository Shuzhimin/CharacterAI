# CharacterAI

AI 虚拟角色养成系统 V1.0

## 后端环境搭建

1. 安装 Qdrant、PostgreSQL 和 Minio

```
docker-compose -f docker-compose.yaml up -d
```

2. 部署 chatglm3-6b, 详细部署进入 langchain_glm3 文件夹内查看
3. 部署微调后的模型, 详细部署进入 ptuning 文件夹内查看

## 后端部署

1. 进入工程根目录/CharacterAI
2. 执行下面命令创建配置文件，并按照实际情况修改 conf.toml 内的信息

```
cp example-conf.toml conf.toml
```

3. 设置 Python 解释器搜索模块的路径为当前目录

```
export PYTHONPATH=.
```

4. 设置 部署后端的服务器 IP 不走代理

```
   export no_proxy="211.81.248.218"
```

5. 创建 conda 环境，character_ai 是环境名称

```
   conda create -n character_ai python=3.12
```

6. 进入创建好的环境

```
conda activate character_ai
```

7. 安装需要的包

```
pip install -r requirements.txt
```

8. 在服务器后台运行后端

```
nohup python app/main.py > app.log 2>&1 &
```
