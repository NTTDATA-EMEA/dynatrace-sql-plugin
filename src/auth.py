from connexion.exceptions import OAuthProblem
import config
TOKEN_DB = {
    config.DTAPITOKEN : {
        'uid': 100
    }
}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info