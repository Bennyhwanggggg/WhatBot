# Authenticator
The authenticator class is responsible for authentication and setting authority level.  

## How it works
The authenticator is token based so it generates tokens using the secret key setup in `config.py` and also gives it a `TOKEN_EXPIRE_TIME` to give the token generated an expire time. So when user logs into the system, if they have a token stored on their side, the token is first checked then if valid, user are automatically authenticated. Otherwise, they will be required to log in again.  