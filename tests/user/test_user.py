import pytest

TEST_USER = 'user1'
TEST_PASS = 'test@pass'

async def test_user_login(loop, test_cli):
    res = await test_cli.get('/api/v1/user/login')
    assert res.status == 403

    res = await test_cli.get(f'/api/v1/user/login?login={TEST_PASS}&password=wrong')
    assert res.status == 403
    
    res = await test_cli.get(f'/api/v1/user/login?login={TEST_USER}&password={TEST_PASS}')
    assert res.status == 200

async def test_user_logout(loop, test_cli):
    res = await test_cli.post('/api/v1/user/logout')
    assert res.status == 403
    
    res = await test_cli.post('/api/v1/user/logout', headers={'Authorization': 'xxx'})
    assert res.status == 403

    res = await test_cli.get(f'/api/v1/user/login?login={TEST_USER}&password={TEST_PASS}')
    assert res.status == 200
    data = await res.json()
    session_key = data['session']

    res = await test_cli.post('/api/v1/user/logout', headers={'Authorization': session_key})
    assert res.status == 200
    
    res = await test_cli.post('/api/v1/user/logout', headers={'Authorization': session_key})
    assert res.status == 403


async def test_user_get(loop, test_cli, session):
    res = await test_cli.get('/api/v1/user/42')
    assert res.status == 403
    
    res = await test_cli.get('/api/v1/user/42', headers=session)
    assert res.status == 404
    
    res = await test_cli.get('/api/v1/user/1', headers=session)
    assert res.status == 200
    data = (await res.json())['user']
    assert data['email'] is not None

async def test_user_orders(loop, test_cli, session):
    res = await test_cli.get('/api/v1/orders')
    assert res.status == 403

    res = await test_cli.get('/api/v1/orders', headers=session)
    assert res.status == 200

    data = (await res.json())['orders']
    assert len(data) == 2
    
    res = await test_cli.get(f'/api/v1/user/login?login=user2&password=test@pass2')
    assert res.status == 200
    data = await res.json()
    session_key = data['session']
    
    res = await test_cli.get('/api/v1/orders', headers={'Authorization': session_key})
    assert res.status == 200

    data = (await res.json())['orders']
    assert len(data) == 0


