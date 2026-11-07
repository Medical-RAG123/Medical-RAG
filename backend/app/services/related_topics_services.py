class RelatedTopicsService:
    def generate(self, question: str, answer: str, max_topics: int = 5) -> list[str]:
        """
        Generate simple related medical topics from the question and answer.
        """

        text = f"{question} {answer}".lower()

        topic_map = {
            "diabetes": [
                "Types of diabetes",
                "Symptoms of diabetes",
                "Causes of diabetes",
                "Diabetes complications",
                "Diabetes prevention",
            ],
            "hypertension": [
                "Causes of hypertension",
                "Symptoms of hypertension",
                "Blood pressure measurement",
                "Hypertension complications",
                "Hypertension treatment",
            ],
            "heart": [
                "Heart disease symptoms",
                "Causes of heart disease",
                "Heart disease risk factors",
                "Heart disease prevention",
                "Heart disease treatment",
            ],
            "asthma": [
                "Asthma symptoms",
                "Asthma triggers",
                "Asthma diagnosis",
                "Asthma treatment",
                "Asthma prevention",
            ],
        }

        for keyword, topics in topic_map.items():
            if keyword in text:
                return topics[:max_topics]

        # Generic fallback
        return [
            "Causes and risk factors",
            "Symptoms and signs",
            "Diagnosis",
            "Treatment options",
            "Prevention",
        ][:max_topics]
