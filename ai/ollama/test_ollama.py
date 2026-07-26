import json
import logging

from ollama import chat


def test1(model, content):
    """一次输出"""
    response = chat(
        model=model,
        messages=[{"role": "user", "content": content}],
    )
    print(response["message"]["content"])


def test2(model, content):
    """流式分块输出"""
    stream = chat(
        model=model,
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)


def test3(model, content):
    """控制结果格式，为json"""
    response = chat(
        model=model,
        messages=[{"role": "user", "content": content}],
        # stream=True,
        format="json",
        options={"temperature": 0},
    )

    response_content = response["message"]["content"]
    json_response = json.loads(response_content)
    print(json_response)
    return json_response


DEFAULT_FORMAT = (
    "%(asctime)s [%(process)d] %(filename)s:%(lineno)s [%(levelname)s]: %(message)s"
)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format=DEFAULT_FORMAT)

    model = "qwen3:1.7b"
    # model = "deepseek-r1:7b"

    content = "为什么天空是蓝色的？"
    # test1(model, content)
    # test2(model, content)

    content = "请随机举出10个国家的首都、人口、占地面积，并以 JSON 格式返回"
    test3(model, content)
