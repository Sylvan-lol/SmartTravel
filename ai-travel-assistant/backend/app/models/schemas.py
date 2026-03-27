from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str  # user, assistant, tool
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None

class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: str = "default"

class ToolResult(BaseModel):
    tool_name: str
    result: Dict[str, Any]

class ChatResponse(BaseModel):
    message: str
    tool_results: Optional[List[ToolResult]] = None
    map_data: Optional[Dict[str, Any]] = None  # 导航专用数据