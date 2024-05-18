# # 2024/2/6
# # zhangzhong


class InternalException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"InternalException: code={self.code}, message={self.message}"
