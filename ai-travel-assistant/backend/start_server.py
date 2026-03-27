import uvicorn
from app.main import app

if __name__ == "__main__":
    # 使用Python的内置方式启动服务
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=False,
        workers=1
    )
