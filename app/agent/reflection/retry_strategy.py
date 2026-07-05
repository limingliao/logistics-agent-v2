from app.agent.reflection.base_reflection import ReflectionResult


class RetryStrategy:
    """
    重试策略
    """

    def should_retry(

        self,

        result: ReflectionResult

    ) -> bool:

        return result.retry