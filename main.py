# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class UnitDied(Exception):
    pass

class UnitDied(Exception):
    pass

class Unit():
    def __init__(self, coord, hp):
        self.coord = coord
        self.hp = hp  # текущее количество хит-поинтов
        self.got_key = False #наличие у юнита ключа для открытия двери в конце уровня
        self.escaped = False #флаг, говорящий о том, удалось ли сбежать из подземелья

    def has_position (self,coord): # проверяет в этих ли координатах установлен юнит (bool)
        return self.coord == coord

    def set_position(self,coord): # устанавливает координаты юнита
        self.coord = coord

    def get_position(self): #hero.get_position(x,y)  # получает координаты, возвращает кортеж
        return self.coord

    def get_damage(self, damage):
        self.hp -= damage

    def get_hp(self):
        return int(self.hp)

    def set_hp(self, new_value):
        self.hp = new_value

    def has_key(self): #- возвращает есть ли ключ(bool)
        return self.got_key

    def set_key(self):
        print('You have the key!')
        self.got_key = True

    def set_escaped(self):
        self.escaped = True

    def has_escaped(self): #проверяет, удалось ли сбежать (bool)
        return self.escaped

    def is_alive(self): #проверяет, есть ли еще у юнита положительное количество хит-поинтов
        if self.hp <= 0:
            print('You are lost!')
            raise UnitDied(f'Game Over!')
        return True

    def get_damage(self, damage): #обрабатывает входящий урон с учетом текущего параметра защиты
        print(f'Damage - {damage}')
        self.hp -= damage
        self.is_alive()

class Ghost(Unit):
    def __init__(self, coord, hp):
        super().__init__(coord, hp)
        self.name = 'Ghost'

class Terrain():
    def __init__(self,walkable,terrain):
        self.walkable = walkable  # можно ли юниту пройти через этот объект
        self.terrain = terrain # имя

    def step_on(self,unit): #в качестве аргумента должен передаваться объект типа Unit
        pass

    def is_walkable(self): #возвращающий флаг о "проходимости" объекта
        #if self.walkable: print('Поле проходимое')
        #else: print('Поле непроходимое')
        return self.walkable

    def get_terrain(self): #возвращает имя объекта
        return self.terrain

class Door(Terrain):
    def __init__(self):
        super().__init__(True, 'Door')

    def step_on(self,unit):
        '''когда юнит наступает на дверь, если у юнита есть ключ,
        то для юнита должен быть установлен флаг escaped'''
        if unit.has_key(): unit.set_escaped()

class Key(Terrain):
    def __init__(self):
        super().__init__(True, 'Key')

    def step_on(self,unit):
        '''должен добавлять юниту, который наступил на ключ,
        этот самый ключ установкой ключа has_key через публичный метод'''
        unit.set_key()

class Trap(Terrain):
    def __init__(self,damage):
        super().__init__(True, 'Trap')
        self.damage = damage

    def step_on(self,unit):
        unit.get_damage(self.damage)

class Grass(Terrain):
    def __init__(self):
        super().__init__(True,'Grass')

class Wall(Terrain):
    def __init__(self):
        super().__init__(False, 'Wall')

class Cell():
    def __init__(self,obj):
        self.obj = obj

    def get_obj(self):
        return self.obj

class Field():
    def __init__(self,unit,field):
        self.unit = unit
        self.field = field

        self.rows = len(field) #int, количество строк в поле
        self.cols = len(field[0])  # int, количество столбцов в поле

        # self.field = [] #list, положение наших объектов, изменяется во время игры
        # for i in range(self.rows):
        #     self.field.append([])
        #     for j in range(self.cols):
        #         if i == 0 or j == 0 or i == self.rows-1 or j == self.cols-1:
        #             self.field[-1].append(Cell(Wall()))
        #         else:
        #             self.field[-1].append(Cell(Grass()))

    def get_field(self): #возвращает свойство field
        return self.field

    def get_cols(self):
        return self.cols

    def get_rows(self):
        return self.rows

    def cell(self,coord): #возвращающий объект находящийся по данным координатам
        return self.field[coord[0]][coord[1]].get_obj() #!!! тестить

    def move_unit_up(self,unit):
        p = unit.get_position()
        pn = (p[0]-1,p[1])
        if self.cell(pn).is_walkable():
            unit.set_position(pn)

    def move_unit_down(self, unit):
        p = unit.get_position()
        pn = (p[0]+1,p[1])
        if self.cell(pn).is_walkable():
            unit.set_position(pn)


    def move_unit_right(self, unit):
        p = unit.get_position()
        pn = (p[0],p[1]+1)
        if self.cell(pn).is_walkable():
            unit.set_position(pn)

    def move_unit_left(self, unit):
        p = unit.get_position()
        pn = (p[0],p[1]-1)
        if self.cell(pn).is_walkable():
            unit.set_position(pn)


class GameController():
    def __init__(self, hero, field):
        self.game_on = True #маркер, сообщающий что пользователь не выразил желание прервать игру
        self.hero = hero
        self.field = field
        self.mapping = {
            'Wall': '🔲',
            'Grass': '⬜',
            'Ghost': '👻',
            'Key': '🗝',
            'Door': '🚪',
            'Trap': '💀',
        }

    def make_field(self):
        drawings = [[aaa.get_obj().terrain for aaa in aa] for aa in self.field.get_field()]
        p = self.hero.get_position()
        drawings[p[0]][p[1]] = self.hero.name
        for aa in drawings: print(' '.join([self.mapping[aaa] for aaa in aa]))


    def play(self):
        prompt = "\nPlease print 'w' or 's' or 'a' or 'd'"
        prompt += "\nEnter 'stop' to end the program. "
        while self.game_on:

            message = input(prompt)
            if message == 'stop':
                self.game_on = False
            else:
                try:
                    if message == 'w': self.field.move_unit_up(self.hero) #изменение координат юнита
                    if message == 's': self.field.move_unit_down(self.hero)
                    if message == 'a': self.field.move_unit_left(self.hero)
                    if message == 'd': self.field.move_unit_right(self.hero)

                    self.field.cell(self.hero.get_position()).step_on(self.hero)  # объект (terrain) где юнит -> step on

                    #if self.hero.has_key() == True: print('You have the key!')
                    if self.hero.has_escaped():
                        print('You are win!')
                        self.game_on = False
                        break

                    self.make_field()
                except UnitDied:
                    print('Game Over!')
                    break
                    #sys.exit()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #формирую входной массив с полем
    #наверное, некорректно его формировать в конструкторе класса
    I,J = 7,8
    field_list = []
    for i in range(I):
        field_list.append([])
        for j in range(J):
            if i == 0 or j == 0 or i == I - 1 or j == J - 1:
                field_list[-1].append(Cell(Wall()))
            else:
                field_list[-1].append(Cell(Grass()))

    field_list[I-1][J-2] = Cell(Door())
    field_list[2][3] = Cell(Trap(30))
    field_list[5][5] = Cell(Trap(30))
    field_list[3][3] = Cell(Key())

    ghost = Ghost((1, 1), 50)
    field = Field(ghost,field_list)

    gamecontroller = GameController(ghost,field)
    gamecontroller.make_field()
    gamecontroller.play()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
