import time


def inference(llm, q):
    t0 = time.perf_counter()
    raw_output = llm(q)
    answer = raw_output["choices"][0]["text"]
    return answer, raw_output, time.perf_counter() - t0
