from pydantic import BaseModel
from typing import List, Optional


class PersonalityTag(BaseModel):
    id: str
    label: str
    prompt_word: str


class StyleTag(BaseModel):
    id: str
    label: str
    prompt_word: str


class GenerateAvatarRequest(BaseModel):
    personality_tags: List[str]
    style_tags: List[str]


class GenerateAvatarResponse(BaseModel):
    task_id: str
    status: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    image_url: Optional[str] = None
    error: Optional[str] = None
