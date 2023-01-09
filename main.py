import pymem
import win32api
import time

# Hazedumper Offsets
LOCAL_PLAYER_OFFSET = 0xDEA964
FORCE_JUMP_OFFSET = 0x52BBC9C
HEALTH_OFFSET = 0x100
FLAGS_OFFSET = 0x104


def main():
    pm = pymem.Pymem("csgo.exe")
    client_module = next(module for module in pm.list_modules() if module.name == "client.dll")
    client_base_address = client_module.lpBaseOfDll

    while True:
        time.sleep(0.01)
        if not win32api.GetAsyncKeyState(0x20):
            continue

        local_player_address = pm.read_uint(client_base_address + LOCAL_PLAYER_OFFSET)

        if not local_player_address or not pm.read_int(local_player_address + HEALTH_OFFSET):
            continue

        flags = pm.read_uint(local_player_address + FLAGS_OFFSET)

        if flags & (1 << 0):
            pm.write_uint(client_base_address + FORCE_JUMP_OFFSET, 6)
            time.sleep(0.01)
            pm.write_uint(client_base_address + FORCE_JUMP_OFFSET, 4)


if __name__ == "__main__":
    main()
