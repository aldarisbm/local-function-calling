from jinja2 import Environment, FileSystemLoader, Template


def get_functions():
    return {
        "get_weather": "get_weather(zipcode: str) -> str",
        "get_zipcode": "get_zipcode(city:str, state:str) -> str"
    }


def functionality():
    environment: Environment = Environment(loader=FileSystemLoader('prompts/'))
    ptpl: Template = environment.get_template('select_function.ptpl')
    query = "testing"
    functions = get_functions()
    tpl = ptpl.render(query=query, functions=functions)
    print(tpl)


functionality()
