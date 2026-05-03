from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    GenerateAvatarRequest,
    GenerateAvatarResponse,
    TaskStatusResponse,
    PersonalityTag,
    StyleTag,
)
from services import generate_avatar_task, get_task_status
from tags import PERSONALITY_TAGS, STYLE_TAGS

app = FastAPI(title="头像生成器 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tags/personality", response_model=list[PersonalityTag])
async def get_personality_tags():
    return PERSONALITY_TAGS


@app.get("/api/tags/style", response_model=list[StyleTag])
async def get_style_tags():
    return STYLE_TAGS


@app.post("/api/generate", response_model=GenerateAvatarResponse)
async def generate_avatar(request: GenerateAvatarRequest):
    try:
        task_id = await generate_avatar_task(
            request.personality_tags,
            request.style_tags,
        )
        return GenerateAvatarResponse(task_id=task_id, status="running")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/task/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str):
    task = get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return TaskStatusResponse(
        task_id=task_id,
        status=task["status"],
        image_url=task["image_url"],
        error=task["error"],
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
