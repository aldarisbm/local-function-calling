import json

from jinja2 import Template

from function_map import fns_map
from helpers import load_template, load_llm


def run():
    user_query: str = input('What is your query?:')

    ptpl: Template = load_template('functions')
    query: str = ptpl.render(query=user_query)
    llm = load_llm()

    output = llm(query)
    json_result = output['choices'][0]['text']
    res = json_result.strip()
    fns = json.loads(res)['functions_to_call']
    for fn in fns:
        fn_name = fn['function_name']
        print(fns_map[fn_name](**fn['parameters']))
