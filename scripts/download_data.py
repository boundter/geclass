import os
import sys

from bs4 import BeautifulSoup
import requests

from config import username, password

landing_page = "https://survey.uni-potsdam.de/admin.html"
data_page = "https://survey.uni-potsdam.de/admin/export/data/c21d6139/data/0/0.html"


def GetCSRFToken(html):
    field_id = "login__csrf_token"
    soup = BeautifulSoup(html, "html.parser")
    token = soup.find(id=field_id)["value"]
    return token


def main():
    username = os.environ['QUAMP_USER']
    password = os.environ['QUAMP_PASSWD']
    # TODO: Delte after download
    with requests.Session() as session:
        homepage = session.get(landing_page)
        token = GetCSRFToken(homepage.text)
        response = session.post(
            landing_page,
            data={
                "login[user]": username,
                "login[password]": password,
                "login[_csrf_token]": token,
                "comit": "Anmelden",
            },
        )
        if not "GEClass" in response.text:
            print("Error: Could not log in to QUAMP", file=sys.stderr)
            sys.exit(1)
        data = session.get(data_page, allow_redirects=True)
        if "GEClass" in data.text:
            print("Error: Could not download data", file=sys.stderr)
            sys.exit(1)
        with open("data.zip", "wb") as data_file:
            data_file.write(data.content)


if __name__ == "__main__":
    main()
