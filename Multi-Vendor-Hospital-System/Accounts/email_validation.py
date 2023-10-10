import requests

api_key = "ab94318200074509bde56c4e37081464"  # https://app.abstractapi.com/api/email-validation
api_url = "https://emailvalidation.abstractapi.com/v1/?api_key=" + api_key


def email_validation(email):
    response = requests.get(api_url + f"&email={email}")
    data = response.json()

    if (
        data["is_valid_format"]["value"]
        and data["is_mx_found"]["value"]
        and data["is_smtp_valid"]["value"]
        and not data["is_catchall_email"]["value"]
        and not data["is_role_email"]["value"]
        and data["is_free_email"]["value"]
    ):
        return True
    else:
        return False
