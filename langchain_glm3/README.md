## 部署 chatglm3-6b

在 langchain_glm3 路径下执行下列命令:

1. git lfs install
2. git clone git clone https://huggingface.co/THUDM/chatglm3-6b
3. git clone https://huggingface.co/BAAI/bge-m3
4. conda create -n glm3 python=3.12
5. conda activate glm3
6. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
7. pip installrequirements.txt
8. export no_proxy="211.81.248.218" 修改成你自己的服务器 IP
9. nohup python api_server.py > glm3.log 2>&1 &
