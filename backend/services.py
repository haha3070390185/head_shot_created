import asyncio
import httpx
import json
from typing import Dict, Optional
from config import get_settings
from tags import PERSONALITY_TAGS, STYLE_TAGS

DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
DASHSCOPE_TASK_URL = "https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

task_storage: Dict[str, Dict] = {}


def build_prompt(personality_tag_ids: list, style_tag_ids: list) -> str:
    personality_prompts = []
    style_prompts = []

    for tag in PERSONALITY_TAGS:
        if tag["id"] in personality_tag_ids:
            personality_prompts.append(tag["prompt_word"])

    for tag in STYLE_TAGS:
        if tag["id"] in style_tag_ids:
            style_prompts.append(tag["prompt_word"])

    personality_str = "，".join(personality_prompts) if personality_prompts else "独特个性"
    style_str = "，".join(style_prompts) if style_prompts else "现代风格"

    return f"一个{personality_str}的人物头像，{style_str}，高清，细节丰富，高质量，专业摄影，8K分辨率"


async def generate_avatar_task(personality_tags: list, style_tags: list) -> str:
    settings = get_settings()
    api_key = settings.dashscope_api_key

    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY 未配置")

    prompt = build_prompt(personality_tags, style_tags)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "wanx-v1",
        "input": {
            "prompt": prompt,
        },
        "parameters": {
            "style": "<auto>",
            "size": "1024*1024",
            "n": 1,
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            DASHSCOPE_API_URL,
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.status_code} - {response.text}")

        result = response.json()
        task_id = result.get("output", {}).get("task_id")

        if not task_id:
            raise Exception(f"未获取到任务ID: {response.text}")

        task_storage[task_id] = {
            "status": "running",
            "image_url": None,
            "error": None,
        }

        asyncio.create_task(poll_task_status(task_id, api_key))

        return task_id


async def poll_task_status(task_id: str, api_key: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    max_attempts = 60
    wait_time = 5

    for attempt in range(max_attempts):
        await asyncio.sleep(wait_time)

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    DASHSCOPE_TASK_URL.format(task_id=task_id),
                    headers=headers,
                )

                if response.status_code == 200:
                    result = response.json()
                    task_status = result.get("output", {}).get("task_status", "")

                    if task_status == "SUCCEEDED":
                        results = result.get("output", {}).get("results", [])
                        if results:
                            image_url = results[0].get("url")
                            task_storage[task_id] = {
                                "status": "succeeded",
                                "image_url": image_url,
                                "error": None,
                            }
                        break

                    elif task_status == "FAILED":
                        error_msg = result.get("output", {}).get("message", "生成失败")
                        task_storage[task_id] = {
                            "status": "failed",
                            "image_url": None,
                            "error": error_msg,
                        }
                        break

            except Exception as e:
                if attempt == max_attempts - 1:
                    task_storage[task_id] = {
                        "status": "failed",
                        "image_url": None,
                        "error": str(e),
                    }
                    break


def get_task_status(task_id: str) -> Optional[Dict]:
    return task_storage.get(task_id)
