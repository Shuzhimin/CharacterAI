# CharacterAI

AI虚拟角色养成系统

## 后端部署

1. cd to project root dir
2. `cp example-conf.toml conf.toml` and configure it correctly
3. `export PYTHONPATH=.`
4. `export no_proxy="211.81.248.213"`
5. conda create -n character_ai python=3.12
6. conda activate character_ai
7. `pip install -r requirements.txt`
8. run all unit test to make sure everything is ok: `pytest .`, you should see no errors.
9. `python app/main.py`, you should see fastapi correctly start and show its url.
