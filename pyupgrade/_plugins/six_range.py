import ast
from typing import Iterable
from typing import List
from typing import Tuple

from tokenize_rt import Offset
from tokenize_rt import Token

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import find_token


def _rewrite_six_moves_range(i: int, tokens: List[Token]) -> None:
    j = find_token(tokens, i, 'range')
    del tokens[i:j]


def _rewrite_six_moves_xrange(i: int, tokens: List[Token]) -> None:
    j = find_token(tokens, i, 'xrange')
    tokens[j] = tokens[j]._replace(src='range')
    del tokens[i:j]


@register(ast.Call)
def visit_Call(
        state: State,
        node: ast.Call,
        parent: ast.AST,
) -> Iterable[Tuple[Offset, TokenFunc]]:
    if (
        state.settings.min_version >= (3,) and
        isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Attribute) and
        isinstance(node.func.value.value, ast.Name) and
        node.func.value.value.id == 'six' and
        node.func.value.attr == 'moves' and
        node.func.attr in {'xrange', 'range'}
    ):
        if node.func.attr == 'range':
            yield ast_to_offset(node), _rewrite_six_moves_range
        else:
            yield ast_to_offset(node), _rewrite_six_moves_xrange
