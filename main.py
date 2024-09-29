import numpy as np
import pandas as pd
from langchain_community.llms import LlamaCpp

from agents import LLMAgent
from prompt_factory import (
    CODE_CORRECTOR_PROMPT,
    GRAPH_GENERATOR_PROMPT,
    SYSTEM_CODE_CORRECTOR_PROMPT,
    SYSTEM_GRAPH_GENERATOR_PROMPT,
)
from tester import TestModule
from utils import try_correction


def run(df, graph_type="bar chart"):
    error_state = 0
    llm = LlamaCpp(
        model_path="models/cpp_models/llama_3.1_FP16.gguf",
        n_ctx=2048,
        max_tokens=2000,
        repeat_last_n=20,
        stop=["END CODE"],
        top_k=3,
        n_gpu_layers=33,
        best_of_n=2,
        verbose=0,
    )
    Code_Generator_Agent = LLMAgent(llm, SYSTEM_GRAPH_GENERATOR_PROMPT, GRAPH_GENERATOR_PROMPT)
    Code_Corrector_Agent = LLMAgent(llm, SYSTEM_CODE_CORRECTOR_PROMPT, CODE_CORRECTOR_PROMPT)
    out = Code_Generator_Agent({"dataframe": df, "graph": graph_type})
    tester = TestModule()
    output = tester.exec_code(out)
    if output["return_code"] == 1:
        error_state = try_correction(Code_Corrector_Agent, tester=tester, output=output, nb_try=3)
    return error_state


if __name__ == "__main__":
    n = 10
    data = {
        "ID": np.arange(1, n + 1),
        "Name": [f"Employee_{i}" for i in range(1, n + 1)],
        "Age": np.random.randint(22, 65, size=n),
        "Salary": np.random.randint(35000, 120000, size=n),
        "Department": np.random.choice(["IT", "HR", "Finance", "Marketing"], size=n),
        "Start Date": pd.date_range("2020-01-01", periods=n, freq="M"),
    }

    # Create the DataFrame
    df = pd.DataFrame(data)

    error_state = run(df, graph_type="pie chart")

    if error_state != 0:
        print("Unfortunatly LLM failed to generate the plot, maybe try an other plot type")
