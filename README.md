# Sakuya Izayoi

Sakuya Izayoi is a multiple purpose Discord bot written in python3 using MySQL. [Click here to invite](https://discord.com/oauth2/authorize?client_id=808385152601817169&scope=bot&permissions=8)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install discord.py, psutil, mysql.connector

```bash
pip install discord.py
```

```bash
pip install psutil
```

```bash
pip install mysql.connector
```

## Usage

```
Clone this project.
```

```
Get your bots token and edit bot.py's client.run('TOKEN') part.  
```

```
You need MySQL on your system (If you don't know how to install look https://www.mysql.com/)
```

```
Create a database called sakuya
Needed tables on this database;


prefixes (prefix, serverid),

log (channelid, guildid),

afk (isafk, memberid, guildid),

autorole (roleid, serverid),

disabledcommands (commandname, guildid),

leavech (chid, serverid),

leavemsg (msg, serverid),

mutedroles (role, guildid),

warns (warnreason, memberid, guildid),

welcomech (chid, serverid),

welcomemsg (msg, serverid)
```

```
Type "python bot.py" on terminal (if you are using Windows type python3 bot.py)
```

## Author

[Reviath](https://discord.com/users/770218429096656917/)

## License
[GNU GPLv3](LICENSE)
