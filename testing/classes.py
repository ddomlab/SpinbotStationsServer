class house:
    def __init__(self, room_num):
        self.title = "LETS GO HOUSE!!!"
        self.rooms = room_num
        return

    def print_title(self):
        print(self.title)
        return

class kitchen(house):
    def __init__(self):
        self.fridge = ["milk", "eggs", "bread"]
        return

    def print_fridge(self):
        for item in self.fridge:
            print(item)


home = house(5)

room1 = kitchen()
room1.print_fridge()
room1.print_title()