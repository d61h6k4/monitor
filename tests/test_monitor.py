
import pytest
import monitor


@pytest.mark.parametrize('name', [0, 1, 'wow'])
def test_greet(name):
    assert type(monitor.greet(name)) == str
