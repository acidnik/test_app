import pytest

async def test_list_shop(test_cli):
    res = await test_cli.get('/api/v1/shop/1')
    assert res.status == 200
    data = (await res.json())['books']
    assert len(data) == 3
