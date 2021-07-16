import pytest

from pyupgrade._data import Settings
from pyupgrade._main import _fix_plugins


@pytest.mark.parametrize(
    ('s', 'version'),
    (
        pytest.param(
            'six.moves.range(3)',
            (2, 7),
            id='Not Python3+',
        ),
        pytest.param(
            'foo.range(3)',
            (3,),
            id='Range, but not from six.moves',
        ),
    ),
)
def test_fix_six_range_noop(s, version):
    assert _fix_plugins(s, settings=Settings(min_version=version)) == s


@pytest.mark.parametrize(
    ('s', 'expected'),
    (
        pytest.param(
            'six.moves.range(3)\n',

            'range(3)\n',

            id='six.moves.range',
        ),
        pytest.param(
            'six.moves.xrange(3)\n',

            'range(3)\n',

            id='six.moves.xrange',
        ),
    ),
)
def test_six_moves_range(s, expected):
    ret = _fix_plugins(s, settings=Settings(min_version=(3,)))
    assert ret == expected
