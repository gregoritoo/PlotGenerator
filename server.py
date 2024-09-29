import os
import sys

import pandas as pd
from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer
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

sys.path.append(os.path.abspath("./model"))


sys.path.append("../")


UPLOAD_FOLDER = os.path.join("static", "uploaded")

app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/generate_plot", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame(data.get("dataframe"))
    graph_type = data.get("graph_type")
    try:

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
            error_state = try_correction(
                Code_Corrector_Agent, tester=tester, output=output, nb_try=3
            )

    except Exception as e:
        print("error", e)

    return jsonify({"msg": f"{error_state}"})


if __name__ == "__main__":

    # app.run()
    http_server = WSGIServer(("", int(sys.argv[1])), app)
    http_server.serve_forever()
