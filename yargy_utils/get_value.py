from yargy import Parser
from yargy.rule import Rule

from yargy_utils import ID_TOKENIZER, TOKENIZER


def get_field_value(my_rule: Rule, text: str, all_match: bool = False, remainder: bool = False,
                    lines: bool = True):
    parser = Parser(my_rule)
    result = []

    if not lines:
        match = list(parser.findall(text.replace('\n', '')))
        if match:
            if all_match:
                return [m.fact for m in match]
            return match[0].fact
        return result

    for line in text.split('\n'):
        line = line.strip()
        match = list(parser.findall(line))

        if match:
            m_fact = match[0].fact

            if remainder:
                m_fact.value = line.replace(m_fact.field_name, '').strip()

            if all_match:
                result.append(m_fact)
            else:
                return m_fact

    return result


def is_inside_span(token, span) -> bool:
    token_span = token.span
    return span.start <= token_span.start and token_span.stop <= span.stop


def select_span_tokens(tokens, spans):
    for token in tokens:
        if any(is_inside_span(token, _) for _ in spans):
            yield token.value


def get_field_value_with_skip(
        my_rule: Rule, text: str, lines: bool = True, first_value: bool = True
) -> list[str] | list[list[str]] | str:
    parser = Parser(my_rule, tokenizer=ID_TOKENIZER)

    if not lines:
        tokens = list(TOKENIZER(text.replace('\n', '')))
        matches = parser.findall(tokens)
        spans = [_.span for _ in matches]
        tokens_values = list(select_span_tokens(tokens, spans))
        return ' '.join(tokens_values)

    results = []

    for line in text.split('\n'):
        tokens = list(TOKENIZER(line))
        matches = parser.findall(tokens)
        spans = [_.span for _ in matches]
        tokens_values = list(select_span_tokens(tokens, spans))
        if tokens_values:
            if first_value:
                return tokens_values
            results.append(tokens_values)

    if not first_value:
        value = sum(results, [])
        return ''.join([s + ' ' for s in value])

    return results
