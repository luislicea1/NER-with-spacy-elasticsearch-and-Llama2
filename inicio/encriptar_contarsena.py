from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

contrasena = "luis"

contrasena_encriptada = pwd_context.hash(contrasena)

print(contrasena_encriptada)
