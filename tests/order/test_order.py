import pytest

async def test_create_orders(test_cli, session):
    res = await test_cli.post('/api/v1/orders', headers=session, json=[])
    assert res.status == 200
    data = (await res.json())['orders']
    assert len(data) == 0


    res = await test_cli.post('/api/v1/orders', headers=session, json=[{'book_id': 1, 'shop_id': 1, 'amount': 1}])
    assert res.status == 200
    data = (await res.json())['orders']
    assert len(data) == 1
    assert data[0]['book']['id'] == 1
    # 2, because order already exists (see init_db)
    assert data[0]['amount'] == 2
    
    res = await test_cli.post('/api/v1/orders', headers=session, json=[
        {'book_id': 1, 'shop_id': 1, 'amount': 1},
        {'book_id': 3, 'shop_id': 1, 'amount': 5}
    ])
    assert res.status == 200
    data = (await res.json())['orders']
    assert len(data) == 2
    assert data[0]['book']['id'] == 1
    assert data[0]['amount'] == 3
    assert data[1]['amount'] == 5
