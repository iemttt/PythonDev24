#!/usr/bin/env python3
import asyncio
import cowsay

class Client():
    def __init__(self, peername):
        self.peername = peername
        self.queue = asyncio.Queue()
        self.login = None

    def __repr__(self):
        return f"{self.peername} {self.login}"

clients = {}

def all_logins():
    return [c.login for c in clients.values() if c.login is not None]

def check_login(peer, login):
    if clients[peer].login == login:
        return False, f"You are already logged as \"{login}\""
    if login in cowsay.list_cows():
        if login not in all_logins():
            return True, None
        return False, f"\"{login}\" is already taken"
    return False, "login must be cow's name"


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = Client(me)
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                command = q.result().decode().strip().split()
                match command[0]:
                    case "login":
                        if len(command) != 2:
                            await clients[me].queue.put("ERROR: login command need only one argument: cow's name")
                            continue
                        login = command[1]
                        ok, err = check_login(me, login)
                        if not ok:
                            await clients[me].queue.put(f"ERROR: {err}")
                            continue
                        clients[me].login = login
                        print(clients)
                        for peer in clients:
                            await clients[peer].queue.put(f"{login} is connected")
                    case "who":
                        if len(command) != 1:
                            await clients[me].queue.put("ERROR: \"who\" command doesn't need arguments")
                            continue
                        await clients[me].queue.put(f"Logged users: {', '.join(all_logins())}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
