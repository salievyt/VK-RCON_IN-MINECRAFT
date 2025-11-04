GROUPS = {
    "FullRcon": {
        "allowed_cmds": ["*"],  # все команды
        "required_rights": "Полные права администратора сервера"
    },
    "moderator": {
        "allowed_cmds": [
            "ban", "unwarn", "banip", "kick", "mute", "kill", "give", "ban-ip", "say", "bc", "broadcast",
            "tempmute", "tp", "eban", "ekick", "ebanip", "etempmute", "exp", "gc", "tps", "eunban",
            "unban", "unbanip", "eunbanip", "tempban", "deop", "xp", "burn", "tempbanip", "banlist",
            "staffhistory", "list", "checkmute", "checkban", "seen", "unmute", "effect", "fly", "warn",
            "realname", "day", "night", "pardon-ip"
        ],
        "required_rights": "Команды: ban, unwarn, banip, kick, mute, kill, give, ban-ip, say, bc, broadcast, tempmute, broadcast, say, tp, eban, ekick, ebanip, banip, etempmute, exp, gc, tps, eunban, unban, unbanip, eunbanip, tempban, deop, xp, burn, tempbanip, banlist, staffhistory, list, checkmute, checkban, seen, unmute, effect, fly, warn, realname, day, night, pardon-ip"
    },
    "curator": {
        "allowed_cmds": [
            "ban", "unwarn", "banip", "kick", "mute", "kill", "give", "ban-ip", "say", "bc", "broadcast",
            "tempmute", "tp", "eban", "ekick", "ebanip", "etempmute", "exp", "gc", "tps", "eunban",
            "unban", "unbanip", "eunbanip", "tempban", "deop", "xp", "burn", "tempbanip", "banlist",
            "staffhistory", "list", "checkmute", "checkban", "seen", "unmute", "effect", "fly", "warn",
            "realname", "day", "night", "pardon-ip", "lp"
        ],
        "required_rights": "Права куратора: доступ к LuckPerms cmd surv1 lp ,а также  команды: ban, unwarn, banip, kick, mute, kill, give, ban-ip, say, bc, broadcast, tempmute, broadcast, say, tp, eban, ekick, ebanip, banip, etempmute, exp, gc, tps, eunban, unban, unbanip, eunbanip, tempban, deop, xp, burn, tempbanip, banlist, staffhistory, list, checkmute, checkban, seen, unmute, effect, fly, warn, realname, day, night, pardon-ip"
    }
}
