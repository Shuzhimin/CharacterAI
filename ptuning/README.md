## 部署微调后的 chatglm2-6b

微调后的模型文件在 tuned_model 文件夹中

在 ptuning 路径下执行下列命令：

1. git lfs install
2. git clone https://huggingface.co/THUDM/chatglm2-6b
3. conda create -n glm2 python=3.10
4. conda activate glm2
5. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
6. pip installrequirements.txt
7. export no_proxy="211.81.248.218" 修改成你自己的服务器 IP
8. nohup python character_llm_api.py > character_llm_api.log 2>&1 &
