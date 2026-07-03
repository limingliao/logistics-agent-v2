from app.agent.prompts.system_prompt import SYSTEM_PROMPT
from app.agent.prompts.prompt_template import PROMPT_TEMPLATE


class PromptManager:

    def build(
        self,
        memory,
        history,
        user_input
    ):

        return PROMPT_TEMPLATE.format(
            system_prompt=SYSTEM_PROMPT,
            memory=memory,
            history=history,
            user_input=user_input,
        )