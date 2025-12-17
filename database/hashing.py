import hashlib

from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def _normalize(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @classmethod
    def bcrypt(cls, password: str):
        return pwd_cxt.hash(cls._normalize(password))

    @classmethod
    def verify(cls, hashed_password, plain_password):
        return pwd_cxt.verify(cls._normalize(plain_password), hashed_password)
