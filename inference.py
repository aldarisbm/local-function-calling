import time

from llama_cpp import Llama


def inference(llm: Llama, inference_params: dict, q: str) -> (str, any, float):
    t0 = time.perf_counter()
    raw_output = llm(q, **inference_params)
    answer = raw_output["choices"][0]["text"]
    return answer, raw_output, time.perf_counter() - t0
