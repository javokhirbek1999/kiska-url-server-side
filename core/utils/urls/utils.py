from hashlib import md5


def hash_the_url(user, url):

    """Hashing function for hasing the URL"""

    user_id = user.id   # get the user id (USER IDs are always UNIQUE)

    # User ID needs to be converted to str to mix it with url
    str_user_id = str(user_id)  

    # Convert the URL into list in order to insert USER ID
    url = list(str(url))

    # Insert User ID into the URL
    url.insert(1, str_user_id[:len(str_user_id)//2])
    url.insert(-2, str_user_id[len(str_user_id)//2:])
    
    # Convert it back to str
    url = "".join(url)

    # Encode the URL with MD5 hashing algorithm and return it as HEX value
    hashed_url = list(md5(url.encode()).hexdigest())

    # As hashed url is pretty long, we need to get only first 5 characters
    # as the hash value
    return "".join(hashed_url[:6])
