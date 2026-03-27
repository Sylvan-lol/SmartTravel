import json
import logging
import httpx
from typing import Dict, Any, List
from openai import OpenAI
from app.config import Config
from app.services.weather_service import get_weather
from app.services.map_service import get_route
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import ChatOpenAI
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 OpenAI 客户端（使用 OpenRouter API）
api_key = "your apikey"
base_url = "your url"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# 使用的模型
MODEL = "your model"

# 初始化 LangChain ChatOpenAI
chat_model = ChatOpenAI(
    model=MODEL,
    api_key=api_key,
    base_url=base_url
)

# 初始化向量存储
embeddings = OpenAIEmbeddings(
    api_key=api_key,
    base_url=base_url
)

# 创建向量数据库目录
vector_db_dir = "vector_db"
os.makedirs(vector_db_dir, exist_ok=True)

# 初始化 Chroma 向量存储
try:
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=vector_db_dir
    )
except Exception as e:
    logger.error(f"Error initializing Chroma: {e}")
    # 创建一个新的向量存储
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=vector_db_dir
    )

# 初始化对话记忆
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)

# 定义RAG链的提示模板
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能旅行助手，能够帮助用户查询天气、规划路线、推荐旅游地点，并使用RAG系统增强知识。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "用户问题: {question}"),
    ("system", "相关信息: {context}"),
    ("system", "请根据用户问题和相关信息，提供详细、友好的回答。如果没有相关信息，请基于你的知识回答。")
])

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_weather",
            "description": "查询指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海、广州等"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_route_info",
            "description": "获取城市间的交通信息，支持驾车和高铁",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_city": {
                        "type": "string",
                        "description": "出发城市名称，如：北京、上海、广州等"
                    },
                    "end_city": {
                        "type": "string",
                        "description": "目的地城市名称，如：北京、上海、广州等"
                    },
                    "transport_type": {
                        "type": "string",
                        "description": "交通方式，可选值：driving（驾车）、highspeed（高铁）",
                        "enum": ["driving", "highspeed"]
                    }
                },
                "required": ["start_city", "end_city", "transport_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "upload_document",
            "description": "上传文档到RAG系统，用于增强AI的知识",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "文档内容"
                    },
                    "title": {
                        "type": "string",
                        "description": "文档标题"
                    }
                },
                "required": ["content", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_info",
            "description": "从RAG系统中检索与查询相关的信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "查询内容"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

async def query_weather(city: str) -> str:
    """查询指定城市的实时天气"""
    result = await get_weather(city)
    if "error" in result or "错误" in result:
        error_msg = result.get("error", result.get("错误", "未知错误"))
        return json.dumps({"type": "weather", "error": error_msg})
    return json.dumps({
        "type": "weather",
        "city": result["城市"],
        "weather": result["天气"],
        "temperature": result["温度"],
        "humidity": result["湿度"],
        "wind": result["风向"],
        "text": f"{result['城市']}当前天气：{result['天气']}，温度{result['温度']}，湿度{result['湿度']}，风向{result['风向']}"
    })

async def plan_route(origin: str, destination: str) -> str:
    """规划驾车路线，起点和终点格式为'经度,纬度'"""
    result = await get_route(origin, destination)
    if "error" in result:
        return json.dumps({"type": "route", "error": result["error"]})
    # 返回完整数据，包括地图绘制所需的 polyline 等
    return json.dumps({
        "type": "route",
        "origin": result["origin"],
        "destination": result["destination"],
        "polyline": result["polyline"],
        "distance_km": result["distance_km"],
        "duration_min": result["duration_min"],
        "steps": result["steps"],
        "text": f"从起点到终点距离{result['distance_km']:.1f}公里，预计耗时{result['duration_min']}分钟。\n路线步骤：\n" + "\n".join([step["instruction"] for step in result["steps"]])
    })

async def get_city_coords(city: str) -> str:
    """通过高德地图 API 查询城市坐标"""
    try:
        async with httpx.AsyncClient() as client:
            url = "https://restapi.amap.com/v3/geocode/geo"
            params = {
                "key": Config.AMAP_API_KEY,
                "address": city,
                "output": "json"
            }
            response = await client.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            if data["status"] == "1" and len(data["geocodes"]) > 0:
                location = data["geocodes"][0]["location"]
                return location
            return None
    except Exception as e:
        logger.error(f"Error getting city coords: {e}")
        return None

async def get_route_info(start_city: str, end_city: str, transport_type: str) -> str:
    """获取城市间的交通信息"""
    # 查询起点城市坐标
    start_coords = await get_city_coords(start_city)
    if not start_coords:
        return json.dumps({"type": "route", "error": f"无法获取{start_city}的坐标信息"})
    
    # 查询终点城市坐标
    end_coords = await get_city_coords(end_city)
    if not end_coords:
        return json.dumps({"type": "route", "error": f"无法获取{end_city}的坐标信息"})
    
    if transport_type == "driving":
        # 调用驾车路线规划
        result_str = await plan_route(start_coords, end_coords)
        result_obj = json.loads(result_str)
        route_text = result_obj.get("text", "路线规划失败")
        route_text = route_text.replace("从起点", f"从{start_city}").replace("到终点", f"到{end_city}")
        return json.dumps({"type": "route", "text": route_text, "data": result_obj})
    elif transport_type == "highspeed":
        # 使用高德地图 API 查询高铁信息
        try:
            async with httpx.AsyncClient() as client:
                url = "https://restapi.amap.com/v3/direction/transit/integrated"
                params = {
                    "key": Config.AMAP_API_KEY,
                    "origin": start_coords,
                    "destination": end_coords,
                    "strategy": "0",  # 0: 最快捷
                    "output": "json"
                }
                response = await client.get(url, params=params, timeout=10)
                
                if response.status_code != 200:
                    return json.dumps({"type": "highspeed", "error": "高铁信息获取失败"})
                
                data = response.json()
                if data["status"] != "1":
                    return json.dumps({"type": "highspeed", "error": data.get("info", "高铁信息获取失败")})
                
                # 提取高铁信息
                if "route" not in data or "transits" not in data["route"]:
                    return json.dumps({"type": "highspeed", "error": "未找到高铁信息"})
                
                transits = data["route"]["transits"]
                if not transits:
                    return json.dumps({"type": "highspeed", "error": "未找到高铁信息"})
                
                # 构建高铁信息文本
                highspeed_info = f"从{start_city}到{end_city}的高铁信息：\n"
                count = 0
                for transit in transits:
                    if count >= 3:  # 最多返回3条
                        break
                    
                    # 检查是否有高铁
                    segments = transit.get("segments", [])
                    has_highspeed = False
                    for segment in segments:
                        if segment.get("buslines"):
                            for busline in segment["buslines"]:
                                if "高铁" in busline.get("name", "") or "G" in busline.get("name", ""):
                                    has_highspeed = True
                                    break
                            if has_highspeed:
                                break
                    
                    if has_highspeed:
                        count += 1
                        # 提取出发时间和到达时间
                        departure_time = transit.get("departure_time", "08:00")
                        arrival_time = transit.get("arrival_time", "09:30")
                        duration = transit.get("duration", 90)  # 分钟
                        
                        # 提取站点信息
                        departure_stop = transit.get("departure_stop", {}).get("name", f"{start_city}站")
                        arrival_stop = transit.get("arrival_stop", {}).get("name", f"{end_city}站")
                        
                        # 提取车次信息
                        train_number = "G" + str(6000 + count)
                        
                        highspeed_info += f"{count}. {train_number}：{departure_stop} - {arrival_stop}，{departure_time}出发，{arrival_time}到达，全程{duration//60}小时{duration%60}分钟\n"
                
                if count == 0:
                    # 如果没有找到高铁，返回驾车信息作为替代
                    result_str = await plan_route(start_coords, end_coords)
                    result_obj = json.loads(result_str)
                    route_text = result_obj.get("text", "路线规划失败")
                    route_text = route_text.replace("从起点", f"从{start_city}").replace("到终点", f"到{end_city}")
                    return json.dumps({"type": "route", "text": route_text, "data": result_obj})
                
                highspeed_info += "建议您提前30分钟到达车站，携带有效身份证件。"
                return json.dumps({"type": "highspeed", "text": highspeed_info})
        except Exception as e:
            logger.error(f"Error getting highspeed info: {e}")
            # 出错时返回驾车信息作为替代
            result_str = await plan_route(start_coords, end_coords)
            result_obj = json.loads(result_str)
            route_text = result_obj.get("text", "路线规划失败")
            route_text = route_text.replace("从起点", f"从{start_city}").replace("到终点", f"到{end_city}")
            return json.dumps({"type": "route", "text": route_text, "data": result_obj})
    else:
        return json.dumps({"type": "route", "error": "不支持的交通方式"})

async def upload_document(content: str, title: str) -> str:
    """上传文档到RAG系统"""
    try:
        # 创建临时文件
        temp_file = f"{title}.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 加载文档
        loader = TextLoader(temp_file, encoding="utf-8")
        documents = loader.load()
        
        # 分割文档
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        
        # 存储到向量数据库
        vectorstore.add_documents(splits)
        vectorstore.persist()
        
        # 删除临时文件
        os.remove(temp_file)
        
        return json.dumps({"type": "document", "text": f"文档 '{title}' 上传成功，包含 {len(splits)} 个片段"})
    except Exception as e:
        logger.error(f"Error uploading document: {e}", exc_info=True)
        return json.dumps({"type": "document", "error": f"上传失败: {str(e)}"})

async def retrieve_info(query: str) -> str:
    """从RAG系统中检索与查询相关的信息"""
    try:
        # 检索相关文档
        docs = vectorstore.similarity_search(query, k=3)
        
        if not docs:
            return json.dumps({"type": "retrieval", "text": "未找到相关信息"})
        
        # 合并文档内容
        context = "\n\n".join([doc.page_content for doc in docs])
        return json.dumps({"type": "retrieval", "text": context})
    except Exception as e:
        logger.error(f"Error retrieving info: {e}", exc_info=True)
        return json.dumps({"type": "retrieval", "error": f"检索失败: {str(e)}"})

async def run_rag_chain(question: str) -> str:
    """运行RAG链，结合检索到的信息生成回答"""
    try:
        # 检索相关文档
        try:
            docs = vectorstore.similarity_search(question, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            logger.warning(f"Error in vectorstore search: {e}")
            # 向量存储检索失败时，使用空上下文
            context = ""
        
        # 获取对话历史
        chat_history = memory.load_memory_variables({}).get("chat_history", [])
        
        # 构建输入
        input_data = {
            "question": question,
            "context": context,
            "chat_history": chat_history
        }
        
        # 生成回答
        result = chat_model.invoke(
            rag_prompt.format_messages(**input_data)
        )
        
        # 更新对话记忆
        memory.save_context(
            {"input": question},
            {"output": result.content}
        )
        
        return result.content
    except Exception as e:
        logger.error(f"Error in RAG chain: {e}", exc_info=True)
        # 当RAG系统完全失败时，直接返回模型的基础回答
        try:
            result = chat_model.invoke([
                ("system", "你是一个智能旅行助手，能够帮助用户查询天气、规划路线、推荐旅游地点。"),
                ("human", question)
            ])
            return result.content
        except:
            return "抱歉，我无法回答您的问题，请稍后重试。"

async def chat_with_ai(messages: List[Dict]) -> Dict[str, Any]:
    """
    处理对话，使用AI agent自动调用工具并返回最终回复和可能的地图数据。
    返回格式：{"content": str, "map_data": dict | None}
    """
    try:
        # 清理消息格式，确保只包含必要的字段
        clean_messages = []
        for msg in messages:
            clean_msg = {
                "role": msg.get("role"),
                "content": msg.get("content")
            }
            # 只添加有内容的消息
            if clean_msg["role"] and clean_msg["content"]:
                clean_messages.append(clean_msg)
        
        logger.info(f"Cleaned messages: {clean_messages}")
        
        # 获取用户最新的消息
        user_message = None
        for msg in reversed(clean_messages):
            if msg["role"] == "user":
                user_message = msg["content"]
                break
        
        if not user_message:
            return {"content": "请输入您的问题", "map_data": None}
        
        # 构建系统提示
        system_prompt = """
        你是一个智能旅行助手，能够帮助用户查询天气、规划路线、推荐旅游地点，并使用RAG系统增强知识。
        
        当用户提出问题时，你需要：
        1. 分析用户的需求
        2. 决定是否需要调用工具来获取更多信息
        3. 如果需要，调用适当的工具获取信息
        4. 根据获取的信息，为用户提供详细、友好的回答
        
        工具说明：
        - query_weather: 查询指定城市的实时天气信息
        - get_route_info: 获取城市间的交通信息，支持驾车和高铁
        - upload_document: 上传文档到RAG系统，用于增强AI的知识
        - retrieve_info: 从RAG系统中检索与查询相关的信息
        
        请根据用户的问题，选择合适的工具进行调用。
        
        例如：
        - 如果用户问"北京的天气怎么样？"，你应该调用query_weather工具，参数city为"北京"
        - 如果用户问"从北京到上海怎么去？"，你应该调用get_route_info工具，参数start_city为"北京"，end_city为"上海"，transport_type为"driving"
        - 如果用户问"从北京到香港坐高铁怎么做？"，你应该调用get_route_info工具，参数start_city为"北京"，end_city为"香港"，transport_type为"highspeed"
        - 如果用户说"我想上传一份关于北京旅游的资料"，你应该调用upload_document工具，参数content为文档内容，title为"北京旅游资料"
        - 如果用户问"台北有哪些著名景点？"，你应该调用retrieve_info工具，参数query为"台北著名景点"
        """
        
        # 构建完整的消息列表
        ai_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ] + clean_messages
        
        # 调用 OpenAI API，使用工具调用功能
        response = client.chat.completions.create(
            model=MODEL,
            messages=ai_messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # 处理API响应
        response_message = response.choices[0].message
        
        # 检查是否需要调用工具
        if response_message.tool_calls:
            logger.info("Tool calls detected")
            
            # 处理工具调用
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                logger.info(f"Calling tool: {function_name} with args: {function_args}")
                
                # 调用相应的函数
                if function_name == "query_weather":
                    result = await query_weather(function_args["city"])
                elif function_name == "get_route_info":
                    result = await get_route_info(
                        function_args["start_city"], 
                        function_args["end_city"], 
                        function_args["transport_type"]
                    )
                elif function_name == "upload_document":
                    result = await upload_document(function_args["content"], function_args["title"])
                elif function_name == "retrieve_info":
                    result = await retrieve_info(function_args["query"])
                else:
                    result = json.dumps({"error": "Unknown tool"})
                
                # 解析工具结果
                result_obj = json.loads(result)
                tool_result = result_obj.get("text", "工具调用失败")
                
                # 添加工具调用结果到消息列表
                ai_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": function_name,
                            "arguments": json.dumps(function_args)
                        }
                    }]
                })
                
                ai_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # 再次调用API，获取最终回复
            response = client.chat.completions.create(
                model=MODEL,
                messages=ai_messages
            )
            
            response_message = response.choices[0].message
        else:
            # 如果不需要工具调用，使用RAG链生成回答
            logger.info("Using RAG chain for response")
            rag_response = await run_rag_chain(user_message)
            response_message = type('obj', (object,), {'content': rag_response})
        
        # 提取回复内容
        content = response_message.content
        if not content:
            content = "抱歉，我无法理解您的问题，请尝试更详细地描述您的需求。"
        
        logger.info(f"AI response: {content}")
        
        # 检查是否需要返回地图数据
        map_data = None
        # 这里可以根据工具调用结果判断是否需要返回地图数据
        
        # 更新对话记忆
        try:
            memory.save_context(
                {"input": user_message},
                {"output": content}
            )
        except Exception as e:
            logger.error(f"Error saving context: {e}")
        
        logger.info(f"Final response: {content}")
        return {"content": content, "map_data": map_data}
    except Exception as e:
        logger.error(f"Error in chat_with_ai: {e}", exc_info=True)
        return {"content": f"抱歉，发生了错误：{str(e)}", "map_data": None}
