from jinja2 import Environment, FileSystemLoader, Template

environment: Environment = Environment(loader=FileSystemLoader('prompts/'))

ptpl: Template = environment.get_template('select+function.ptpl')

query = input()
