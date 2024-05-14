from typing import Any


class Tool:
    AVAILABLE_TOOLS = []  # 存储可用工具信息
    ZHIPUAI_TOOLS = []  # 存储工具信息

    @classmethod
    def dispatch(
        cls, func_name: str, params: dict[str, Any], raise_exception: bool = False
    ) -> Any:
        # 在ZHIPUAI_TOOLS中查找具有给定名称的函数
        for tool in cls.ZHIPUAI_TOOLS:
            if tool["meta"]["function"]["name"] == func_name:
                # 检查所有必需的参数是否都已提供
                required_params = tool["meta"]["function"]["parameters"]["required"]
                for param in required_params:
                    if param not in params:
                        if raise_exception:
                            raise ValueError(f"Missing required parameter: {param}")
                        else:
                            return f"Missing required parameter: {param}"

                # 执行找到的函数并返回结果
                try:
                    return tool["func"](**params)
                except Exception as e:
                    if raise_exception:
                        raise
                    else:
                        return str(e)

        # 如果没有找到函数，则根据raise_error的值决定是否抛出异常或返回提示
        if raise_exception:
            raise ValueError(f"Function '{func_name}' not found in ZHIPUAI_TOOLS")
        else:
            return f"Function '{func_name}' not found in ZHIPUAI_TOOLS"

    @classmethod
    def get_tools(cls) -> list[dict[str, Any]]:
        return [tool["meta"] for tool in cls.ZHIPUAI_TOOLS]

    @classmethod
    def load_tool(cls, tool_name: str):
        # 检查工具是否已经加载
        for tool in cls.ZHIPUAI_TOOLS:
            if tool["meta"]["function"]["name"] == tool_name:
                return f"Tool '{tool_name}' is already loaded."
        # 如果工具未加载，则从AVAILABLE_TOOLS中查找并添加到ZHIPUAI_TOOLS
        for tool in cls.AVAILABLE_TOOLS:
            if tool["meta"]["function"]["name"] == tool_name:
                cls.ZHIPUAI_TOOLS.append(tool)
                return f"Tool '{tool_name}' loaded successfully."
        return f"Tool '{tool_name}' not found in AVAILABLE_TOOLS."

    @classmethod
    def unload_tool(cls, tool_name: str):
        # 在ZHIPUAI_TOOLS中查找名为tool_name的工具并删除
        for tool in cls.ZHIPUAI_TOOLS:
            if tool["meta"]["function"]["name"] == tool_name:
                cls.ZHIPUAI_TOOLS.remove(tool)
                return f"Tool '{tool_name}' unloaded successfully."
        return f"Tool '{tool_name}' not found in ZHIPUAI_TOOLS."

    @classmethod
    def list_available_tools(cls):
        # 列出所有的AVAILABLE_TOOLS中的函数名称和函数描述。
        return [
            (tool["meta"]["function"]["name"], tool["meta"]["function"]["description"])
            for tool in cls.AVAILABLE_TOOLS
        ]

    def __init__(self, name=None, description="", params=None, required_params=None):
        self.name = name
        self.description = description
        self.params = params or {}
        self.required_params = required_params or []

    def __call__(self, func):
        # 使用`self`中的参数创建参数的meta信息
        params_meta = {}
        for param_name, param_info in self.params.items():
            param_type = param_info.get("type", "string")
            param_desc = param_info.get("description", "")
            params_meta[param_name] = {
                "type": param_type,
                "description": param_desc,
            }

        # 创建函数的meta信息
        meta = {
            "type": "function",
            "function": {
                "name": self.name or func.__name__,
                "description": self.description or func.__doc__,
                "parameters": {
                    "type": "object",
                    "properties": params_meta,
                    "required": self.required_params,
                },
            },
        }

        # 将meta信息和函数本身加入到AVAILABLE_TOOLS列表中
        Tool.AVAILABLE_TOOLS.append({"meta": meta, "func": func})

        # 返回原函数
        return func
