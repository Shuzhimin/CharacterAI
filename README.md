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

# TODO

最后一个分支，完成系统的所有功能，因为系统的需求已经固定

1. 先重点测试一下两个admin/select接口，剩下的应该都没啥大问题
2. 重构所有的测试，添加一个本地测试选项，或者使用mock，主要目的是为了方便本地测试，但是部署起来也不应该需要修改代码
3. 重构测试完成之后，重构整个项目，并保证测试一直是通过的，接口不变, 比如添加日志，model模块拆分等
4. 完善部署文档，考虑新手验证
