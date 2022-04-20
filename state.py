
# Objekts, kas apraksta spēles stāvokli
class State:

    def __init__(self, parent, level: int, gems: list, move: bool, path: int):
        self.move = move
        self.parent = parent
        self.level = level
        self.gems = list(gems)
        self.score = None
        self.children = []
        self.path = path

    def __str__(self):
        res = f'Level: {self.level}\n' \
              f'Move: {self.move}\n' \
              f' {self.gems[5]} {self.gems[4]} {self.gems[3]} {self.gems[2]} {self.gems[1]} {self.gems[0]} \n' \
              f'{self.gems[6]}           {self.gems[13]}\n' \
              f' {self.gems[7]} {self.gems[8]} {self.gems[9]} {self.gems[10]} {self.gems[11]} {self.gems[12]} \n'
        return res

    def gems_to_str(self):
        res = ''
        for i in self.gems:
            res += str(i)
        return res

    def add_child(self, child):
        self.children.append(child)

    def get_winner(self):

        for i in range(6):
            if self.gems[i] > 0:
                return None
        for i in range(7, 13, 1):
            if self.gems[i] > 0:
                return None

    def get_move_result(self, pit, current_move):
        gems = list(self.gems)
        temp_gems = gems[pit]
        gems[pit] = 0
        while temp_gems > 0:
            pit += 1
            if pit == len(gems):
                pit = 0
            if (current_move and pit == 6) or (not current_move and pit == 13):
                continue
            temp_gems -= 1
            gems[pit] += 1
        if gems[pit] == 1:
            if (current_move and 7 <= pit <= 12) or (not current_move and 0 <= pit <= 5):
                if gems[pit + 2 * (6 - pit)] > 0:
                    if current_move:
                        gems[13] += gems[pit] + gems[pit + 2 * (6 - pit)]
                    else:
                        gems[6] += gems[pit] + gems[pit + 2 * (6 - pit)]
                    gems[pit] = 0
                    gems[pit + 2 * (6 - pit)] = 0
        return gems
