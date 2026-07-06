from app.agent.workflow.executors.base_executor import BaseExecutor


class ConditionExecutor(BaseExecutor):

    def execute(self, step, context):

        return eval(
            step.action,
            {},
            {
                "context": context
            },
        )