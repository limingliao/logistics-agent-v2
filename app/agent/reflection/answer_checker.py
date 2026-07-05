from app.agent.reflection.base_reflection import (
    BaseReflection,
    ReflectionResult
)


class AnswerChecker(BaseReflection):
    """
    回答质量检查
    """

    BAD_WORDS = [

        "不知道",

        "不清楚",

        "无法回答",

        "抱歉",

        "可能",

        "应该",

        "大概",

        "猜测"
    ]

    def check(self, answer: str) -> ReflectionResult:

        if not answer:

            return ReflectionResult(

                passed=False,

                retry=True,

                score=0,

                reason="Empty Answer"
            )

        score = 100

        for word in self.BAD_WORDS:

            if word in answer:

                score -= 20

        passed = score >= 60

        return ReflectionResult(

            passed=passed,

            retry=not passed,

            score=score,

            reason="OK" if passed else "Low Confidence"
        )