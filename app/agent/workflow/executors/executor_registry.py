class ExecutorRegistry:

    def __init__(self):

        self._executors = {}

    def register(self, step_type, executor):

        self._executors[step_type.lower()] = executor

    def get(self, step_type):

        executor = self._executors.get(step_type.lower())

        if executor is None:
            raise RuntimeError(
                f"Executor [{step_type}] not found."
            )

        return executor

    def has(self, step_type):

        return step_type.lower() in self._executors

    def remove(self, step_type):

        self._executors.pop(step_type.lower(), None)

    def clear(self):

        self._executors.clear()

    @property
    def executors(self):

        return self._executors