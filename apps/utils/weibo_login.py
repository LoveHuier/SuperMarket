# _*_coding: utf-8_*_


def get_auth_url():
    """
    用户授权，获取code
    :return:
    """
    client_id = "548743674"
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_uri = 'http://127.0.0.1:8000'
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}" \
        .format(client_id=client_id, redirect_uri=redirect_uri)
    print(auth_url)


def get_access_token(code=''):
    """
    获取access_token
    :param code:
    :return:
    """
    client_id = "548743674"
    client_secret = '67ecdc8739355c4b144499725675f016'
    redirect_uri = 'http://127.0.0.1:8000'
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    })
    """
    '{"access_token":"2.00aoLHWD07STIb2c5dffb2e20rCMFd",
    "remind_in":"157679999",
    "expires_in":157679999,
    "uid":"3222954964",
    "isRealName":"true"}'
    """
    pass


def get_user_info(access_token=''):
    """

    :return:
    """
    user_url = "https://api.weibo.com/2/users/show.json"
    uid = '3222954964'
    user_info_url = user_url + "?access_token={access_token}&uid={uid}" \
        .format(access_token=access_token, uid=uid)
    print(user_info_url)


if __name__ == "__main__":
    # get_auth_url()
    # get_access_token("413b973d4228fd52b02b97ee60d46919")
    get_user_info("2.00aoLHWD07STIb2c5dffb2e20rCMFd")