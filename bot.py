import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from mcrcon import MCRcon
from group_perms import GROUPS
import time

class UserManager:
    USERS = {
        1074907636: {"group": "FullRcon", "mc_nick": "SALIEVVS", "servers": ["hub1", "surv1"]},
        1050553053: {"group": "FullRcon", "mc_nick": "1dle0ne", "servers": ["hub1", "surv1"]},
        634566442: {"group": "FullRcon", "mc_nick": "Igaseyt", "servers": ["hub1", "surv1"]},
        831395934: {"group": "FullRcon", "mc_nick": "Kind_lion", "servers": ["hub1", "surv1"]},
        738262320: {"group": "FullRcon", "mc_nick": "dimas2030", "servers": ["surv1"]},
        740769275: {"group": "FullRcon", "mc_nick": "MrLopstar", "servers": ["hub1", "surv1"]},
        # ...другие пользователи...
    }

    @classmethod
    def get(cls, user_id):
        return cls.USERS.get(user_id)

    @classmethod
    def get_profile(cls, user_id):
        user = cls.get(user_id)
        if not user:
            return "Вы не зарегистрированы в системе."
        return f"Группа доступа: {user['group']}\nНик в игре: {user['mc_nick']}"

class RconManager:
    SERVERS = {
        "surv1": {"host": "157.180.4.105", "port": 41343, "password": "b3eguyrgy56754gazscw"},
        "hub1": {"host": "157.180.4.105", "port": 41311, "password": "by3uegdsdcxhgd73"},
        # ...другие сервера...
    }

    @classmethod
    def send(cls, server_key, command):
        server = cls.SERVERS.get(server_key)
        if not server:
            return "Сервер не найден"
        try:
            with MCRcon(server["host"], server["password"], port=server["port"]) as mcr:
                resp = mcr.command(command)
            return resp
        except Exception as e:
            return f"Ошибка RCON: {e}"

class VKBot:
    LOG_FILE = "command_log.txt"

    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)

    def log_command(self, user_id,command, result):
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"Пользователь {user_id} : команда {command} -> Ответ на команду от сервера-> {result}\n")

    def check_permission(self, user_id, command):
        user = UserManager.get(user_id)
        if not user:
            return False
        group = user["group"]
        allowed = GROUPS.get(group, {}).get("allowed_cmds", [])
        if "*" in allowed:
            return True
        cmd_name = command.split()[0]
        return cmd_name in allowed

    def run(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        user_id = event.user_id
                        text = event.text.strip()
                        user = UserManager.get(user_id)
                        if not (text.startswith("cmd ") or text == "cmds" or text == "профиль"):
                            continue
                        if not user:
                            self.vk.messages.send(user_id=user_id, message="Вы не являетесь администратором", random_id=0)
                            continue
                        if text.startswith("cmd "):
                            parts = text.split(" ", 2)
                            if len(parts) < 3:
                                self.vk.messages.send(user_id=user_id, message="Использование: cmd <сервер> <команда>", random_id=0)
                                continue
                            server_key, command = parts[1], parts[2]
                            allowed_servers = user.get("servers", [])
                            if allowed_servers and server_key not in allowed_servers:
                                self.vk.messages.send(user_id=user_id, message="У вас нет доступа к этому серверу.", random_id=0)
                                continue
                            if not self.check_permission(user_id, command):
                                self.vk.messages.send(user_id=user_id, message="У вас нет прав на выполнение этой команды.", random_id=0)
                                continue
                            result = RconManager.send(server_key, command)
                            self.log_command(user_id, command, result)
                            if not result:
                                result = "Ответ от сервера: "
                            self.vk.messages.send(user_id=user_id, message=result, random_id=0)
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
                            self.vk.messages.send(user_id=user_id, message=msg, random_id=0)
                        elif text == "профиль":
                            profile = UserManager.get_profile(user_id)
                            self.vk.messages.send(user_id=user_id, message=profile, random_id=0)
            except Exception as e:
                print(f"Ошибка longpoll: {e}")
                time.sleep(5)

if __name__ == "__main__":
    vk_token = "vk1.a.o3D1eRdVhe4Rycg4XFPvPgFkGRdi4vUEXMfeyxwVf0EXoO_GgCXyiLb2-9wLXzMttdmRJhPlEGyhw_i4hRyIJkaV0XqKvwHUv1EYbAOUV6Oe0nNYcLYINvadCME0608jyLyFMjmdCFMCCcRqX_bDEKLVyKl7CMOuRYX2VK8ySWFLDkGm7wY75UIymMHB1oTzk62W8OGh6yBW0bzowWXXng"
    bot = VKBot(vk_token)
    bot.run()