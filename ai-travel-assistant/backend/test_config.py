from app.config import Config

print("测试配置加载...")
print(f"LLM_API_KEY: {Config.LLM_API_KEY}")
print(f"LLM_BASE_URL: {Config.LLM_BASE_URL}")
print(f"LLM_MODEL: {Config.LLM_MODEL}")
print("配置加载测试完成！")