from app.agent.workflow.executors.base_executor import BaseExecutor


class PythonExecutor(BaseExecutor):

    def execute(self, step, context):

        local_vars = {
            "context": context,
            "result": None,
        }

        exec(step.action, {}, local_vars)

        return local_vars.get("result")