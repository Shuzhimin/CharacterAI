# CharacterAI

AI虚拟角色养成系统

## 后端部署

1. cd to project root dir
2. `cp example-conf.toml conf.toml` and configure it correctly
3. `export PYTHONPATH=.`
4. conda create -n character_ai python=3.12
5. conda activate character_ai
6. `pip install -r requirements.txt`
7. run all unit test to make sure everything is ok: `pytest .`, you should see no errors.
8. `python app/main.py`, you should see fastapi correctly start and show its url.
