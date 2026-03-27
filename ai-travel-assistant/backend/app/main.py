from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import ChatRequest, ChatResponse, ToolResult
from app.services.ai_service import chat_with_ai
import uuid

app = FastAPI(title="AI Travel Assistant API")

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """对话接口，支持工具调用"""
    try:
        # 转换消息格式（简化）
        messages = [msg.dict() for msg in request.messages]
        result = await chat_with_ai(messages)
        return ChatResponse(
            message=result["content"],
            map_data=result.get("map_data")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok"}