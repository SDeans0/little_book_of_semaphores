import pytest
from ch_3.code.mutex import main

@pytest.mark.parametrize("n_threads", [1,2,3,4,100])
def test_mutex(n_threads):
    assert main(n_threads=n_threads) == n_threads