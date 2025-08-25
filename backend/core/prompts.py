STORY_PROMPT = """
你是一个富有创造力的故事作家，专门使用中文创作引人入胜的互动冒险故事。
请根据我指定的JSON格式生成一个完整的分支故事，包含多条路径和多个结局。

故事要求：
1. 一个引人入胜的标题
2. 一个起始情境（根节点），包含3个选项
3. 每个选项都应该引导到另一个包含自己选项的节点
4. 某些路径应该通向结局（包括胜利和失败）
5. 只有一条路径应该通向胜利结局，其他路径都应该通向失败结局

故事结构要求：
- 每个节点应该有2-3个选项（结局节点除外）
- 故事应该有5-6层深度（包括根节点）
- 在路径长度上添加变化（一些较早结束，一些较晚）
- 确保只有一条胜利路径，其他路径都应该通向失败结局
- 结局节点的故事内容应该体现出是结局而不是继续发展的剧情

**重要格式要求：**
1. 必须输出有效的JSON格式，不能包含任何非JSON文本
2. 所有字符串值必须用双引号包围
3. 布尔值必须是true或false（小写）
4. 数组和对象必须正确嵌套
5. 不能有尾随逗号
6. 确保所有必需的字段都存在

请严格按照以下JSON结构输出你的故事：
{format_instructions}

**输出要求：**
- 只输出JSON，不要添加任何解释、注释或其他文本
- 确保JSON格式完全正确，可以被直接解析
- 如果遇到格式问题，请重新生成确保格式正确
- 不要简化或省略故事结构的任何部分。
- 不要在JSON结构之外添加任何文本。
"""

# 备用英文提示词，用于提高稳定性
STORY_PROMPT_EN = """
You are a creative story writer specializing in creating engaging interactive adventure stories.
Please generate a complete branching story with multiple paths and multiple endings according to the specified JSON format.

Story Requirements:
1. An engaging title
2. A starting situation (root node) with 3 options
3. Each option should lead to another node with its own options
4. Some paths should lead to endings (including victory and failure)
5. There should be exactly one path leading to a victory ending

Story Structure Requirements:
- Each node should have 2-3 options (except ending nodes)
- The story should have 5-6 levels of depth (including root node)
- Add variation in path length (some end earlier, some later)
- Ensure there is exactly one victory path
- The story content of ending nodes should clearly indicate it's an ending

**Important Format Requirements:**
1. Must output valid JSON format, no non-JSON text allowed
2. All string values must be enclosed in double quotes
3. Boolean values must be true or false (lowercase)
4. Arrays and objects must be properly nested
5. No trailing commas allowed
6. Ensure all required fields are present

Please output your story strictly according to the following JSON structure:
{format_instructions}

**Output Requirements:**
- Output only JSON, no explanations, comments, or other text
- Ensure the JSON format is completely correct and can be parsed directly
- If format issues occur, regenerate to ensure correctness
- Do not simplify or omit any part of the story structure.
- Do not add any text outside the JSON structure.
"""

json_structure = """
{
    "title": "故事标题",
    "rootNode": {
        "content": "故事的起始情境",
        "isEnding": false,
        "isWinningEnding": false,
        "options": [
            {
                "text": "选项1的文本",
                "nextNode": {
                    "content": "选择选项1后发生的情况",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        // 更多嵌套选项
                    ]
                }
            },
            // 根节点的更多选项
        ]
    }
}
"""