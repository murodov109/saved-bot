import os

def read_list(filename):
    if not os.path.exists(filename):
        open(filename, "w").close()
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_list(filename, data):
    with open(filename, "w") as f:
        f.write("\n".join(data))

def add_user(user_id, username=None):
    users = read_list("users.txt")
    if str(user_id) not in users:
        users.append(str(user_id))
        write_list("users.txt", users)

def get_users():
    return read_list("users.txt")

def add_admin(admin_id):
    admins = read_list("admins.txt")
    if str(admin_id) not in admins:
        admins.append(str(admin_id))
        write_list("admins.txt", admins)

def get_admins():
    return [int(a) for a in read_list("admins.txt")]

def add_channel(channel):
    channels = read_list("channels.txt")
    if channel not in channels:
        channels.append(channel)
        write_list("channels.txt", channels)

def remove_channel(channel):
    channels = read_list("channels.txt")
    channels = [c for c in channels if c != channel]
    write_list("channels.txt", channels)

def get_channels():
    return read_list("channels.txt")
