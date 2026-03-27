from zai import ZhipuAiClient
import inspect

# 查看ZhipuAiClient的构造函数参数
print("ZhipuAiClient.__init__ signature:")
print(inspect.signature(ZhipuAiClient.__init__))

# 查看类的文档
print("\nZhipuAiClient docstring:")
print(ZhipuAiClient.__doc__)
