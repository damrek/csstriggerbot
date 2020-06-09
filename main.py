from hackManager.hack import Hack  # Absolute memory address
from ReadWriteMemory import rwm
import time
import win32api
import win32con
import struct

target = "hl2.exe"
instance = Hack(target)

ProcID = rwm.GetProcessIdByName("hl2.exe")
hProcess = rwm.OpenProcess(ProcID)

Player_Base = 0x53BFC8

bind_key = 0x25
b_ShotNow = False
dw_teamOffset = 0x98



NumOfPlayers = 32
dw_PlayerCountOff = 0x5C817C
dw_crosshairOffs = 0x14DC


dw_entityBase = 0x5495B4
dw_EntityLoopDistance = 0x10
dw_IDOff = 0x50
Xoff = 0x274
Yoff = 0x278
Zoff = 0x27C

dw_radarBase = 0x581A30
dw_RadarEntityLoopDistance = 0x140
dw_NameOff = 0x38
dw_HealthOff = 0x5C
dw_posx = 0x60
dw_posy = 0x64

class MyPlayer():

    def __init__(self, CLocalPlayer=0,Team =0, CrosshairEntityID =0, position =None):
        self.CLocalPlayer = CLocalPlayer
        self.Team = Team
        self.CrosshairEntityID = CrosshairEntityID
        self.Position = position

    def ReadInformation(self):
        global NumOfPlayers
        clientDLLba = instance.module_base_dict["client.dll"]
        engineDLLba = instance.module_base_dict["engine.dll"]
        BaseAddress = rwm.getPointer(hProcess, clientDLLba + Player_Base, offsets=[0x0])
        self.CLocalPlayer = BaseAddress

        #team
        self.Team = rwm.getPointer(hProcess, self.CLocalPlayer + dw_teamOffset, offsets=[0x0])

        #crosshair
        self.CrosshairEntityID = rwm.getPointer(hProcess, self.CLocalPlayer + dw_crosshairOffs, offsets=[0x0])

        #num of players
        NumOfPlayers = rwm.getPointer(hProcess, engineDLLba + dw_PlayerCountOff, offsets=[0x0])

        #position
        self.Positionx = instance.read_float(self.CLocalPlayer + Xoff)
        x = self.Positionx[0]

        self.Positiony = instance.read_float(self.CLocalPlayer + Yoff)
        y = self.Positiony[0]

        self.Positionz = instance.read_float(self.CLocalPlayer + Zoff)
        z = self.Positionz[0]

        global MyPos
        MyPos = []
        MyPos.append(x)
        MyPos.append(y)
        MyPos.append(z)
        self.Position = MyPos

class PlayerList():

    def __init__(self, CBaseEntity=0,Team =0,Health=0,CrosshairPlayerEntityID=0,position =None, radarbase=0,name="",rhealth=0,rx=0,ry=0):
        self.CBaseEntity = CBaseEntity
        self.Team = Team
        self.Health = Health
        self.CrosshairPlayerEntityID = CrosshairPlayerEntityID
        self.Position = position
        self.RadarBase = radarbase
        self.Name = name
        self.RHealth = rhealth
        self.posx = rx
        self.posy = ry

    def ReadInformation(self, Player=0):
        clientDLLba = instance.module_base_dict["client.dll"]
        engineDLLba = instance.module_base_dict["engine.dll"]
        BaseAddress = rwm.getPointer(hProcess, clientDLLba + dw_entityBase + (Player * dw_EntityLoopDistance), offsets=[0x0])
        self.CBaseEntity = BaseAddress

        #team
        self.Team = rwm.getPointer(hProcess, self.CBaseEntity + dw_teamOffset, offsets=[0x0])

        #health -> los muertos tienen 1 de vida | los que no existen tienen 0 de vida
        self.Health = rwm.getPointer(hProcess, self.CBaseEntity + 0x90, offsets=[0x0])

        #id
        self.CrosshairPlayerEntityID = rwm.getPointer(hProcess, self.CBaseEntity + dw_IDOff, offsets=[0x0])

        #position
        self.Positionx = instance.read_float(self.CBaseEntity + Xoff)
        x = self.Positionx[0]

        self.Positiony = instance.read_float(self.CBaseEntity + Yoff)
        y = self.Positiony[0]

        self.Positionz = instance.read_float(self.CBaseEntity + Zoff)
        z = self.Positionz[0]

        global PyPos
        PyPos = []
        PyPos.append(x)
        PyPos.append(y)
        PyPos.append(z)
        self.Position = PyPos

        #radar_name
        self.RadarBase = rwm.getPointer(hProcess, clientDLLba + dw_radarBase, offsets=[0x00])
        self.Name = instance.read_string(self.RadarBase + dw_NameOff + (Player * dw_RadarEntityLoopDistance),32)
        self.Name = self.Name[0]

        #radar_health
        self.RHealth = instance.read_int(self.RadarBase + dw_HealthOff + (Player * dw_RadarEntityLoopDistance))
        self.RHealth = self.RHealth[0]

        #radar_posx_posy
        self.posx = instance.read_float(self.RadarBase + dw_posx + (Player * dw_RadarEntityLoopDistance))
        self.posx = self.posx[0]

        self.posy = instance.read_float(self.RadarBase + dw_posy + (Player * dw_RadarEntityLoopDistance))
        self.posy = self.posy[0]



def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)

print "Game found! Running Triggerbot"
MyPlayer = MyPlayer()
while 1:
    MyPlayer.ReadInformation()

    def Trigger():
        list_of_players = [PlayerList() for i in range(0, NumOfPlayers,1)]
        for i in range(len(list_of_players)):
            list_of_players[i] = PlayerList()
            list_of_players[i].ReadInformation(i)
            print list_of_players[i].Name, list_of_players[i].RHealth, list_of_players[i].Team, "||", list_of_players[i].posx, list_of_players[i].posy


            if MyPlayer.CrosshairEntityID > 0 and MyPlayer.CrosshairEntityID < 32 and list_of_players[i].Team != MyPlayer.Team and list_of_players[i].Health > 1 and MyPlayer.CrosshairEntityID == list_of_players[i].CrosshairPlayerEntityID:
                #print ("Pum")
                click()
        print "\n"
        time.sleep(1)
    Trigger()


