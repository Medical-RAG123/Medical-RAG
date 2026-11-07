class RelatedTopicsService:
    def generate(self, question: str, answer: str, max_topics: int = 5) -> list[str]:

        text = f"{question} {answer}".lower()

        if "diabetes" in text:
            return [
                "Types of diabetes",
                "Symptoms of diabetes",
                "Causes of diabetes",
                "Diabetes complications",
                "Diabetes prevention",
            ][:max_topics]

        if "hypertension" in text:
            return [
                "Causes of hypertension",
                "Symptoms of hypertension",
                "Blood pressure measurement",
                "Hypertension complications",
                "Hypertension treatment",
            ][:max_topics]

        return [
            "Causes and risk factors",
            "Symptoms and signs",
            "Diagnosis",
            "Treatment options",
            "Prevention",
        ][:max_topics]
