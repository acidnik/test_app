import pytest
from app.application import create_app

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
    res = await test_cli.get('/api/v1/user/logout')
    assert res.status == 403
    
    res = await test_cli.get('/api/v1/user/logout', headers={'Authorization': 'xxx'})
    assert res.status == 403

    res = await test_cli.get(f'/api/v1/user/login?login={TEST_USER}&password={TEST_PASS}')
    assert res.status == 200
    data = await res.json()
    session_key = data['session']
    # session_key = ''

    res = await test_cli.get('/api/v1/user/logout', headers={'Authorization': session_key})
    assert res.status == 200
    
    res = await test_cli.get('/api/v1/user/logout', headers={'Authorization': session_key})
    assert res.status == 403



