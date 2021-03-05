from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash('Super_password')
check_password_hash(password_hash, 'password')


def generate_password_hash(password: str) -> str:
    return


print(check_password_hash('sha256$3iZ6cBRm$362f8e3b3d8e99518d277ef9856ab1f5e5539e462cb4a8bb9bf532afcabccf31'))
