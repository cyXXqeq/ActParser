import json

from ipymarkup import show_span_ascii_markup as show_markup
from yargy import Parser
from yargy.rule import Rule


# подчёркивает конструкции, соответствующие правилу
def show_matches(my_rule, lines):
    parser = Parser(my_rule)
    for line in lines:
        matches = parser.findall(line)
        spans = [_.span for _ in matches]
        show_markup(line, spans)


# выводит атрибуты сущности
def show_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def show_from_act(my_rule: Rule, text: str) -> None:
    parser = Parser(my_rule)
    matches = list(parser.findall(text))
    if matches:
        match = matches[0]
        m_fact = match.fact
        show_json(m_fact.as_json)
