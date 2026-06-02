from app.services.auth import AuthService

def test_hash_password():
    auth = AuthService()

    hashed = auth.hash_password("123456")

    assert hashed != "123456"


def test_verify_password_valid():
    auth = AuthService()

    hashed = auth.hash_password("123456")

    assert auth.verify_password(hashed, "123456") is True


def test_verify_password_invalid():
    auth = AuthService()

    hashed = auth.hash_password("123456")

    assert auth.verify_password(hashed, "senha_errada") is False