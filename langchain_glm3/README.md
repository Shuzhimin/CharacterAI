## 部署 chatglm3-6b

1. conda create -n glm3 python=3.12
2. conda activate glm3
3. install pytorch
   Please select the corresponding version based on the actual situation.
   e.g. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
4. pip installrequirements.txt
5. export no_proxy="211.81.248.218"
6. nohup python api_server.py > glm3.log 2>&1 &
