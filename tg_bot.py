import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from group_perms import GROUPS
from bot import SERVERS, check_permission, send_rcon

# Telegram user mapping
USERS_TG = {
    6339466530: {  # Telegram user id
        "group": "FullRcon",
        "mc_nick": "SALIEVVS",
        "servers": ["hub1", "surv1"]
    },
    6339466530: {
        "group": "moderator",
        "mc_nick": "1dle0ne",
        "servers": ["hub1"]
    },
    # ...другие пользователи...
}

TG_TOKEN = "7758014618:AAFF1VzzJvWq5nFNFQAnbdXDFB8DSDozAS0"
TARGET_CHAT_ID = 2412764674

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

def get_tg_user(user_id):
    return USERS_TG.get(user_id)

@dp.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer("Привет! Используй команды:\ncmd <сервер> <команда>\ncmds\nпрофиль")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user = get_tg_user(user_id)
    text = message.text.strip()
    # Позволяем работать и в группах, и в личке
    if not (text.startswith("cmd ") or text == "cmds" or text == "профиль"):
        return
    if not user:
        await message.reply("Вы не являетесь администратором")
        return
    if text.startswith("cmd "):
        parts = text.split(" ", 2)
        if len(parts) < 3:
            await message.reply("Использование: cmd <сервер> <команда>")
            return
        server_key, command = parts[1], parts[2]
        allowed_servers = user.get("servers", [])
        if allowed_servers and server_key not in allowed_servers:
            await message.reply("У вас нет доступа к этому серверу.")
            return
        if not check_permission(user_id, command):
            await message.reply("У вас нет прав на выполнение этой команды.")
            return
        result = send_rcon(server_key, command)
        if not result:
            result = "Ответ от сервера: "
        await message.reply(result)
    elif text == "cmds":
        group = user["group"]
        allowed = GROUPS.get(group, {}).get("allowed_cmds", [])
        msg = f"Ваша группа: {group}\n"
        if "*" in allowed:
            msg += "Доступны все команды."
        elif allowed:
            msg += "Доступные команды:\n" + "\n".join(f"- {cmd}" for cmd in allowed if cmd)
        else:
            msg += "Нет доступных команд."
        await message.reply(msg)
    elif text == "профиль":
        mc_nick = user["mc_nick"]
        group = user["group"]
        msg = f"Группа доступа: {group}\nНик в игре: {mc_nick}"
        await message.reply(msg)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))


