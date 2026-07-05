from app.agent.prompts.system_prompt import SYSTEM_PROMPT
from app.agent.prompts.prompt_template import PROMPT_TEMPLATE


class PromptManager:
    """
    企业级 Prompt Manager

    职责：
    1. 统一构建 Prompt
    2. 拼接 Memory
    3. 拼接 History
    4. 后续扩展：
        - Knowledge
        - Tool Description
        - Few-shot
    """

    def build(
        self,
        user_input: str,
        history: str = "",
        memory: str = "",
        knowledge: str = "",
        tool_desc: str = "",
        examples: str = "",
    ) -> str:

        return PROMPT_TEMPLATE.format(
            system_prompt=SYSTEM_PROMPT,
            memory=memory,
            history=history,
            knowledge=knowledge,
            tool_desc=tool_desc,
            examples=examples,
            user_input=user_input,
        )