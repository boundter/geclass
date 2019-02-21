
def test_only_registered(client, auth):
    # non logged in user redirected to log in
    response = client.get('/')
    assert 'http://localhost/auth/login' == response.headers['Location']

    # logged in user can acces their overview
    auth.login()
    response = client.get('/')
    print(response.data)
    print(response.headers)
    assert b'Your courses' in response.data
