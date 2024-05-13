## 部署微调后的 chatglm2-6b

### 部署微调后的模型文件在 tuned_model 文件夹中

1. conda create -n glm2 python=3.10
2. conda activate glm2
3. install pytorch
   Please select the corresponding version based on the actual situation.
   e.g. conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
4. pip installrequirements.txt
5. export no_proxy="211.81.248.218"
6. nohup python character_llm_api.py > character_llm_api.log 2>&1 &
