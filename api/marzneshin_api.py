import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MARZNESHIN_API_URL = os.getenv("MARZNESHIN_API_BASE_URL")


async def get_admin_token(username: str, password: str) -> str:
    url = f"{MARZNESHIN_API_URL}/api/admins/token"
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": "string",
        "client_secret": "string"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            if response.status != 200:
                raise Exception("❌ نام کاربری یا رمز عبور اشتباه است")
            result = await response.json()
            return result["access_token"]


async def check_sudo_by_username(token: str, username: str) -> bool:
    url = f"{MARZNESHIN_API_URL}/api/admins"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                admins = data.get("items", [])
                for admin in admins:
                    if admin["username"] == username and admin.get("is_sudo"):
                        return True
    return False


async def get_admins(username: str, password: str):
    token = await get_admin_token(username, password)
    url = f"{MARZNESHIN_API_URL}/api/admins"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def get_total_used_traffic(admin_username: str, login_username: str, login_password: str):
    token = await get_admin_token(login_username, login_password)
    url = f"{MARZNESHIN_API_URL}/api/admins/{admin_username}/users"
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"❌ دریافت کاربران ادمین شکست خورد: {response.status}")

            data = await response.json()
            users = data.get("items", [])
            total_traffic_bytes = 0

            for user in users:
                used = user.get("used_traffic", 0)
                try:
                    used = float(used)
                except (ValueError, TypeError):
                    used = 0
                total_traffic_bytes += used

            return format_bytes(total_traffic_bytes)


def format_bytes(size):
    try:
        size = float(size)
    except (ValueError, TypeError):
        return "نامعتبر"
    power = 2 ** 10
    n = 0
    units = ['بایت', 'کیلوبایت', 'مگابایت', 'گیگابایت', 'ترابایت', 'پتابایت']
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"
