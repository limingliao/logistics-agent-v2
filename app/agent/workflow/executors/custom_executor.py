from app.agent.workflow.executors.base_executor import BaseExecutor


class CustomExecutor(BaseExecutor):

    def execute(self, step, context):

        if not callable(step.action):
            raise RuntimeError(
                "Custom action must be callable."
            )

        return step.action(context)