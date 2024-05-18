# 2024/4/10
# zhangzhong

from zhipuai import ZhipuAI

from app.common import conf


def generate_image(description: str) -> str:
    client = ZhipuAI(api_key=conf.get_zhipuai_cog_view_key())

    response = client.images.generations(
        model="cogview-3",
        prompt=description,
    )

    url = response.data[0].url
    if url is None:
        raise ValueError(f"Avatar generation failed. response: {response}")
    return url
