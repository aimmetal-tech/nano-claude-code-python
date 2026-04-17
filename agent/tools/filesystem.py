import os
from typing import Any

from claude.call_tool import Tool, ToolPropertyDetail, newTool


def newReadFileTool() -> Tool:
    # 处理逻辑函数, 相比 lambda 更健壮
    def readFileLogic(input: dict[str, Any]) -> str:
        path = input["path"]

        if not path:
            return "path不能为空"

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                return content
        except Exception as e:
            return f"读取文件失败: {e}"

    return newTool(
        name="read_file",
        description="读一个文件，返回该文件的全部内容",
        properties={"path": ToolPropertyDetail(type="string", description="文件目录")},
        required=["path"],
        func=readFileLogic,
    )


def newWriteFileTool() -> Tool:
    def writeFileLogic(input: dict[str, Any]) -> str:
        path = input["path"]
        content = input["content"]

        if not path:
            return "path不能为空"

        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"写入文件成功: {path}"
        except Exception as e:
            return f"写入文件失败: {e}"

    return newTool(
        name="write_file",
        description="将内容写入指定文件,如果文件已经存在则覆盖,如果父目录不存在则自动创建",
        properties={
            "path": ToolPropertyDetail(type="string", description="文件目录"),
            "content": ToolPropertyDetail(type="string", description="要写入的内容"),
        },
        required=["path", "content"],
        func=writeFileLogic,
    )
