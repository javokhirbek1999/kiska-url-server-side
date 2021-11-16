from hashlib import md5


def hash_the_url(user, url):

    user_id = user.id

    str_user_id = str(user_id)
    url = list(str(url))

    url.insert(1, str_user_id[:len(str_user_id)//2])
    url.insert(-2, str_user_id[len(str_user_id)//2:])
    
    url = "".join(url)

    hashed_url = list(md5(url.encode()).hexdigest())

    return "".join(hashed_url[:6])
