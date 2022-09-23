from lark import Tree

from .types import FormattedLine, FormattedLines, Outcome
from .context import Context, ExpressionContext
from .expression import format_concrete_expression
from .expression_to_str import expression_to_str

STANDALONE_ANNOTATIONS = ["tool", "icon"]


def is_non_standalone_annotation(statement: Tree) -> bool:
    if statement.data != "annotation":
        return False
    name = statement.children[0].value
    return name not in STANDALONE_ANNOTATIONS


def prepend_annotations_to_formatted_line(
    line_to_prepend_to: FormattedLine, context: Context
) -> FormattedLines:
    assert len(context.annotations) > 0
    whitelineless_line = line_to_prepend_to[1].strip()
    annotations_string = " ".join(
        [format_annotation_to_string(annotation) for annotation in context.annotations]
    )
    single_line_length = (
        context.indent + len(annotations_string) + len(whitelineless_line)
    )
    if single_line_length <= context.max_line_length:
        single_line = "{}{} {}".format(
            context.indent_string, annotations_string, whitelineless_line
        )
        context.annotations = []
        return [(line_to_prepend_to[0], single_line)]
    formatted_lines: FormattedLines = []
    for annotation in context.annotations:
        lines, _ = format_standalone_annotation(annotation, context)
        formatted_lines += lines
    formatted_lines.append(line_to_prepend_to)
    context.annotations = []
    return formatted_lines


def format_standalone_annotation(annotation: Tree, context: Context) -> Outcome:
    return format_concrete_expression(
        annotation, ExpressionContext("", -1, "", -1), context
    )


def format_annotation_to_string(annotation: Tree) -> str:
    return expression_to_str(annotation)
