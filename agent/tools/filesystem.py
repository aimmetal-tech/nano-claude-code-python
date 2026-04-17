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


def newEditFileTool() -> Tool:
    def editFileLogic(input: dict[str, Any]) -> str:
        path = input["path"]
        old_string = input["old_string"]
        new_string = input["new_string"]

        if not path:
            return "path不能为空"

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return f"读取文件失败: {e}"

        count = content.count(old_string)
        if count == 0:
            return f"未找到匹配的文本: {old_string}"
        if count > 1:
            return f"找到 {count} 处匹配，请提供更多上下文以精确定位"

        new_content = content.replace(old_string, new_string, 1)

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return f"编辑文件成功: {path}"
        except Exception as e:
            return f"写入文件失败: {e}"

    return newTool(
        name="edit_file",
        description="通过替换指定文本来编辑文件,old_string必须在文件中唯一匹配",
        properties={
            "path": ToolPropertyDetail(type="string", description="文件路径"),
            "old_string": ToolPropertyDetail(type="string", description="要被替换的原文本"),
            "new_string": ToolPropertyDetail(type="string", description="替换后的新文本"),
        },
        required=["path", "old_string", "new_string"],
        func=editFileLogic,
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
