from langchain_core.prompts import ChatPromptTemplate


class LLMAgent:
    def __init__(self, llm, system_prompt: str, user_prompt: str) -> None:
        self.llm = llm
        self.prompt_template = ChatPromptTemplate(
            [
                ("system", system_prompt),
                (
                    "user",
                    user_prompt,
                ),
            ]
        )
        self.chain = self.prompt_template | self.llm

    def __call__(self, args: dict) -> str:
        return self.chain.invoke(args)
