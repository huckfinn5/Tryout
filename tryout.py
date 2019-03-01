import random
import kivy
import glob
import os
kivy.require('1.10.1')
#640,1136
from kivy.config import Config
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '568')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.boxlayout import BoxLayout
cwd = os.getcwd()
o_list = []
d_list = []
o_backup = []
d_backup = []
s_list = []
s_backup = []

class PlayerListButton(ListItemButton):
    def __init__(self, **kwargs):
        super(PlayerListButton, self).__init__(**kwargs)
        self.height = self.size[1]*1.75
        self.selected_color= 1, 0, 0, 1
        self.deselected_color = 1,1, .2, .42
        self.color= 0, 0, 0, 1
        self.background_color = 1,1, .2, .42


class OpenIntro(Screen):
    image1 = cwd + '/Logo.png'
    pass

class HomePage(Screen):
    pass


class ScreenManagment(ScreenManager):
    pass

class How_To_Use(Screen):
    text0 = '\nTryout Instructions\n'
    text1 = "\nHello, and welcome to tryout, an easy to use playtime manager. Tryout takes away the pain of remembering whose played and who you want to see, and lets you focus on how your potential players are performing. To keep it simple, here are the basic mechanisms of how Tryout works, enjoy! \n"
    text2 = '1) Insert players you want rotated evenly at each position as a list separated by ","s between the players names.\n'
    text3 = "2) When setting each squad, fill each position with people who you want to cycle through that position. For instance, if I wanted two defenders, Joe and John, to split reps, I would put \'\'Joe,John\'\' in one position. \n"
    text4 = "3) If you want someone to remain on the field constantly, list only their name in the position.\n"
    text5 = "4) Note that complete duplicate names are not allowed, this can easily be avoided by inserting a players last initial. For instance \'\'Joe, Tim, Joe\'\' would not be allowed, but \'\'Joe, Tim, Joe P\'\' would be fine.\n"
    text6 = "5) All positions must be filled before you can proceed to calling lines.\n"
    text7 = "6) Positions can be edited at any time to account for injuries, wanting to see certain individuals more, etc.\n\n\n\n\n"

class Set_OLine(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name !='' and self.positions <7:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1=''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 =[]
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2=[]
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions+=1
                self.ids.oline_pos.text = "O Line: Positions: " + str(self.positions) + "/7"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global  o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions-=1
            self.ids.oline_pos.text = "O Line: Positions: " + str(self.positions) + "/7"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "O Line Positions: " + str(self.positions) + "/7"


class Set_DLine(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    d_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name!='' and self.positions<8:
            global d_list
            global d_backup
            var1 = ''
            temp = []
            temp2 = []
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 =[]
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2=[]
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                d_list.append(temp)
                d_backup.append(temp2)
                self.d_line_list.adapter.data.extend([player_name])
                self.d_line_list._trigger_reset_populate()
                self.name_text_input.text = ''
                self.positions+=1
                self.ids.dline_pos.text = "D Line: Positions: " + str(self.positions) + "/7"
            print(d_list)
            print(self.have)

    def delete(self):
        if self.d_line_list.adapter.selection:
            global d_list
            global d_backup
            selection = self.d_line_list.adapter.selection[0].text
            self.d_line_list.adapter.data.remove(selection)
            temp = []
            var1=''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in d_list:
                    if x in y:
                        d_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            d_backup.remove(temp)
            self.positions-=1
            self.ids.dline_pos.text = "D Line: Positions: " + str(self.positions) + "/7"
            print(d_list)

    def show(self):
        new = pop_up_dline()
        new.open()

    def length(self):
        global d_list
        return len(d_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Defense Positions: " + str(self.positions) + "/7"


class Point_On(Screen):
    pass

class Football_Point_On(Screen):
    pass

class Player_Line_D(Screen):
    global d_list
    global d_backup
    temp_list = ["X","X X X X X","X X X X X X X X X","X X X X X X X X X X X X X","X X X X X X X X X","X X X X X","X"]


    def create(self):
        for x in range(0,len(d_list)):
            random.shuffle(d_list[x])
        for x in range(0,len(d_list)):
            temp1 = ""
            if len(d_list[x])!=0:
                temp1 = d_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0,len(d_list)):
            if len(d_list[x]) == 0:
                for els in range(0,len(d_backup[x])):
                    d_list[x].append(d_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

    def reset(self):
        self.temp_list = ["X","X X X X X","X X X X X X X X X","X X X X X X X X X X X X X","X X X X X X X X X","X X X X X","X"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

class Player_Line_O(Screen):
    global o_list
    global o_backup
    temp_list = ["O","O O O O O","O O O O O O O O O","O O O O O O O O O O O O O","O O O O O O O O O","O O O O O","O"]


    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(d_list)):
            if len(o_list[x]) == 0:
                for els in range(0,len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

    def reset(self):
        self.temp_list = ["O","O O O O O","O O O O O O O O O","O O O O O O O O O O O O O","O O O O O O O O O","O O O O O","O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

class Set_FootballD(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    d_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 11:
            global d_list
            global d_backup
            var1 = ''
            temp = []
            temp2 = []
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x]!=' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                d_list.append(temp)
                d_backup.append(temp2)
                self.d_line_list.adapter.data.extend([player_name])
                self.d_line_list._trigger_reset_populate()
                self.name_text_input.text = ''
                self.positions += 1
                self.ids.dline_pos.text = "Defense: Positions: " + str(self.positions) + "/11"
            print(d_list)
            print(self.have)

    def delete(self):
        if self.d_line_list.adapter.selection:
            global d_list
            global d_backup
            selection = self.d_line_list.adapter.selection[0].text
            self.d_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in d_list:
                    if x in y:
                        d_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            d_backup.remove(temp)
            self.positions -= 1
            self.ids.dline_pos.text = "Defense: Positions: " + str(self.positions) + "/11"
            print(d_list)

    def show(self):
        new = pop_up_dline()
        new.open()

    def length(self):
        global d_list
        return len(d_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.d_line_list.adapter.data = []
        self.d_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Defense Positions: " + str(self.positions) + "/11"


class Set_FootballO(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 11:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Offense: Positions: " + str(self.positions) + "/11"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Offense: Positions: " + str(self.positions) + "/11"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Offense Positions: " + str(self.positions) + "/11"

class Set_SpecialTeams(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    s_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 11:
            global s_list
            global s_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                s_list.append(temp)
                s_backup.append(temp2)
                print(o_list)
                self.s_line_list.adapter.data.extend([player_name])
                self.s_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.sline_pos.text = "Special Teams: Positions: " + str(self.positions) + "/11"
                self.name_text_input.text = ''

    def delete(self):
        if self.s_line_list.adapter.selection:
            global s_list
            global s_backup
            selection = self.s_line_list.adapter.selection[0].text
            self.s_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in s_list:
                    if x in y:
                        s_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            s_backup.remove(temp)
            self.positions -= 1
            self.ids.sline_pos.text = "Special Teams: Positions: " + str(self.positions) + "/11"
            print(s_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global s_list
        global s_backup
        global d_list
        global d_backup
        s_list = []
        s_backup=[]
        d_list=[]
        d_backup=[]
        self.s_line_list.adapter.data = []
        self.s_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"

class Set_Soccer(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 11:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"

class Set_Lacrosse(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 10:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/10"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/10"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/10"

class Set_FieldHockey(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 11:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/11"

class Set_Rugby15(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 15:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Offense: Positions: " + str(self.positions) + "/15"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/15"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/15"

class Set_Rugby7(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 7:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/7"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/7"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions = 0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/7"

class Set_Basketball(Screen):
    positions = 0
    name_text_input = ObjectProperty()
    o_line_list = ObjectProperty()
    have = {}

    def add(self):
        ok = True
        player_name = self.name_text_input.text
        if player_name != '' and self.positions < 5:
            global o_list
            global o_backup
            temp = []
            temp2 = []
            var1 = ''
            for x in range(0, len(player_name)):
                if player_name[x] == '\n':
                    ok = False
                    break
                elif player_name[x] == ',':
                    if var1 not in self.have:
                        temp.append(var1)
                        temp2.append(var1)
                        var1 = ''
                    else:
                        ok = False
                        break
                        temp = []
                        temp2 = []
                elif player_name[x] != ' ':
                    var1 += player_name[x]
            if var1 != '' and ok == True:
                if var1 not in self.have:
                    temp.append(var1)
                    temp2.append(var1)
                else:
                    ok = False
                    temp = []
                    temp2 = []
            if ok == True:
                for x in temp:
                    self.have[x] = 0
                o_list.append(temp)
                o_backup.append(temp2)
                print(o_list)
                self.o_line_list.adapter.data.extend([player_name])
                self.o_line_list._trigger_reset_populate()
                self.positions += 1
                self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/5"
                self.name_text_input.text = ''

    def delete(self):
        if self.o_line_list.adapter.selection:
            global o_list
            global o_backup
            selection = self.o_line_list.adapter.selection[0].text
            self.o_line_list.adapter.data.remove(selection)
            temp = []
            var1 = ''
            for x in range(0, len(selection)):
                if selection[x] == ',':
                    temp.append(var1)
                    var1 = ''
                else:
                    var1 += selection[x]
            if var1 != '':
                temp.append(var1)
            for x in temp:
                for y in o_list:
                    if x in y:
                        o_list.remove(y)
                        for xy in temp:
                            del self.have[xy]
            o_backup.remove(temp)
            self.positions -= 1
            self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/5"
            print(o_list)

    def show(self):
        new = pop_up_oline()
        new.open()

    def length(self):
        global o_list
        return len(o_list)

    def revert(self):
        global o_list
        global o_backup
        global d_list
        global d_backup
        o_list = []
        o_backup=[]
        d_list=[]
        d_backup=[]
        self.o_line_list.adapter.data = []
        self.o_line_list._trigger_reset_populate()
        self.positions=0
        self.ids.oline_pos.text = "Positions: " + str(self.positions) + "/5"



class Lacrosse_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O O","O O O O O O O O O O", "O O O O O O O", "O O O O O","O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O O", "O O O O O O O O O O","O O O O O O O", "O O O O O","O O O",
                 "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]


class FootballD_Show(Screen):
    global d_list
    global d_backup
    temp_list = ["X", "X X X" ,"X X X X X", "X X X X X X X", "X X X X X X X X X","X X X X X X X X X X X", "X X X X X X X X X", "X X X X X X X",
                 "X X X X X", "X X X", "X"]

    def create(self):
        for x in range(0, len(d_list)):
            random.shuffle(d_list[x])
        for x in range(0, len(d_list)):
            temp1 = ""
            if len(d_list[x]) != 0:
                temp1 = d_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(d_list)):
            if len(d_list[x]) == 0:
                for els in range(0, len(d_backup[x])):
                    d_list[x].append(d_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

    def reset(self):
        self.temp_list = ["X", "X X X" ,"X X X X X", "X X X X X X X", "X X X X X X X X X","X X X X X X X X X X X", "X X X X X X X X X", "X X X X X X X",
                 "X X X X X", "X X X", "X"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]


class FootballO_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O", "O O O O O O O O O O O ", "O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O", "O O O O O O O O O O O ", "O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

class FootballS_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                 "O O O O O O O O O O O ", "O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(s_list)):
            random.shuffle(s_list[x])
        for x in range(0, len(s_list)):
            temp1 = ""
            if len(s_list[x]) != 0:
                temp1 = s_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(s_list)):
            if len(s_list[x]) == 0:
                for els in range(0, len(s_backup[x])):
                    s_list[x].append(s_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O", "O O O O O O O O O O O ", "O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]


class Soccer_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                 "O O O O O O O O O O O ", "O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                          "O O O O O O O O O O O ", "O O O O O O O O O",
                          "O O O O O O O", "O O O O O", "O O O",
                          "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

class FieldHockey_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                 "O O O O O O O O O O O " ,"O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                          "O O O O O O O O O O O " ,"O O O O O O O O O",
                          "O O O O O O O", "O O O O O", "O O O",
                          "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]

class Rugby15_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                 "O O O O O O O O O O O", "O O O O O O O O O O O O O", "O O O O O O O O O O O O O O O", "O O O O O O O O O O O O O","O O O O O O O O O O O ","O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]
        self.ids.twelve.text = self.temp_list[11]
        self.ids.thirteen.text = self.temp_list[12]
        self.ids.fourteen.text = self.temp_list[13]
        self.ids.fifteen.text = self.temp_list[14]

    def reset(self):
        self.temp_list = ["O", "O O O", "O O O O O", "O O O O O O O", "O O O O O O O O O",
                 "O O O O O O O O O O O", "O O O O O O O O O O O O O", "O O O O O O O O O O O O O O O", "O O O O O O O O O O O O O","O O O O O O O O O O O ","O O O O O O O O O",
                 "O O O O O O O", "O O O O O", "O O O",
                 "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]
        self.ids.eight.text = self.temp_list[7]
        self.ids.nine.text = self.temp_list[8]
        self.ids.ten.text = self.temp_list[9]
        self.ids.eleven.text = self.temp_list[10]
        self.ids.twelve.text = self.temp_list[11]
        self.ids.thirteen.text = self.temp_list[12]
        self.ids.fourteen.text = self.temp_list[13]
        self.ids.fifteen.text = self.temp_list[14]

class Rugby7_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O O O", "O O O O O O O O O", "O O O O O O O O O O O O O", "O O O O O O O O O", "O O O O O",
                 "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

    def reset(self):
        self.temp_list = ["O", "O O O O O", "O O O O O O O O O", "O O O O O O O O O O O O O", "O O O O O O O O O",
                          "O O O O O", "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]
        self.ids.six.text = self.temp_list[5]
        self.ids.seven.text = self.temp_list[6]

class Basketball_Show(Screen):
    global o_list
    global o_backup
    temp_list = ["O", "O O O O O", "O O O O O O O O O",  "O O O O O", "O"]

    def create(self):
        print(o_backup)
        for x in range(0, len(o_list)):
            random.shuffle(o_list[x])
        for x in range(0, len(o_list)):
            temp1 = ""
            if len(o_list[x]) != 0:
                temp1 = o_list[x].pop()
            self.temp_list[x] = temp1
        for x in range(0, len(o_list)):
            if len(o_list[x]) == 0:
                for els in range(0, len(o_backup[x])):
                    o_list[x].append(o_backup[x][els])
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]


    def reset(self):
        self.temp_list = ["O", "O O O O O", "O O O O O O O O O",  "O O O O O", "O"]
        self.ids.one.text = self.temp_list[0]
        self.ids.two.text = self.temp_list[1]
        self.ids.three.text = self.temp_list[2]
        self.ids.four.text = self.temp_list[3]
        self.ids.five.text = self.temp_list[4]



class pop_up_oline(Popup):
    pass

class pop_up_dline(Popup):
    pass

class pop_up_stereo(Popup):
    pass


presentation = Builder.load_file('tryout.kv')

class Chem_CanApp(App):
    def build(self):
        return presentation

r=Chem_CanApp()
r.run()
