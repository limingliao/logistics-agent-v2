from app.agent.reflection.answer_checker import AnswerChecker
from app.agent.reflection.retry_strategy import RetryStrategy
from app.agent.reflection.base_reflection import ReflectionResult


class ReflectionManager:
    """
    Reflection管理器
    """

    def __init__(self):

        self.answer_checker = AnswerChecker()

        self.retry_strategy = RetryStrategy()

    def reflect(

        self,

        prompt: str,

        answer: str

    ) -> ReflectionResult:

        result = self.answer_checker.check(answer)

        return result

    def should_retry(

        self,

        answer: str

    ) -> bool:

        result = self.reflect(answer)

        return self.retry_strategy.should_retry(result)