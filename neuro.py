#Hi this is my first project in python. I wanna be honest the IA helped me a lot in this code, but i never let it do all the work and i always try to understand the code and make it by myself, so i can learn. 
import pymem
import time
import os
import threading 
import neuro_api
import trio
import pyautogui 

#The process name of the game and offsets should be the same for the version 1.0.0.1051
PROCESS_NAME = "PlantsVsZombies.exe" 
BASE_POINTER = 0x006A9EC0  
OFFSET_BOARD = 0x768       
OFFSET_SUN = 0x5560 
OFFSET_SEEDBANK = 0x144
OFFSET_SEED_COUNT = 0x24
OFFSET_SEED_ARRAY = 0x28

# Seed Bank       
SEEDPACKET_SIZE = 0x50
PACKET_COOLDOWN = 0x24
PACKET_COOLDOWN_MAX = 0x28
PACKET_PLANT_ID = 0x34

# ZOMBIES 
OFFSET_ZOMBIE_ARRAY = 0x90
ZOMBIE_STRUCT_SIZE = 0x15C 
ZOMBIE_HP_OFFSET = 0xC8    
ZOMBIE_ROW_OFFSET = 0x1C  
ZOMBIE_X_OFFSET = 0x2C 
ZOMBIE_EATING = 0x51    
# Auto taker (Takes sun and coins automatically)
def Auto_Taker(pm):
    while True:
        try:
            pm.write_bytes(0x0043158F, b'\xEB', 1)
            time.sleep(1.0)
            pm.write_bytes(0x0043158F, b'\x75', 1)
            time.sleep(2.0)
        except pymem.exception.MemoryWriteError:
            time.sleep(1)

def main():
    print("Starting...")
    try:
        pm = pymem.Pymem(PROCESS_NAME)
    except Exception:
        print(f"Error:{PROCESS_NAME} not found.")
        return
    #Auto Taker start
    hilo = threading.Thread(target=Auto_Taker, args=(pm,), daemon=True)
    hilo.start()
    
    base_address = BASE_POINTER 

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            app_ptr = pm.read_int(base_address)
            if app_ptr == 0:
                print("Waiting the game...")
                time.sleep(1)
                continue
                
            board_ptr = pm.read_int(app_ptr + OFFSET_BOARD)
            if board_ptr == 0:
                print("Start the level...")
                time.sleep(1)
                continue
            #sun reader  
            Sun = pm.read_int(board_ptr + OFFSET_SUN)
            
            print("PvZ Info")
            print(f"Sun: {Sun}")
            
        except pymem.exception.MemoryReadError:
            print("Searching Pointer...")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()