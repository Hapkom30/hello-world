def clean_screen(n):
   for a in range(n):
      print('\n')

def NewGame():
      global pole
      pole = [[' ','0', '1', '2'],
              ['0','-','-','-'],
              ['1','-','-','-'],
              ['2','-','-','-']]

def PoleScreen():
   print(f'\n {pole[0]} \n {pole[1]} \n {pole[2]} \n {pole[3]} \n')

def HowHodsCount():
    global pole
    return pole[1].count('X')+pole[2].count('X')+pole[3].count('X') + pole[1].count('O') + pole[2].count('O') + pole[3].count('O')

def hod_player(player):
   global player1
   oper = 'X' if player1 == player else 'O'
   return input(f'''{player} Ваш ход! Введите данные для {oper}: 
   Примеры: 0 0, 0 1, 0 2, 1 0, 1 1, 1 2, 2 0, 2 1, 2 0   ''')

def WhoWinner():
    countXD = 0
    countOD = 0
    global pole
    global player1
    global player2
    for i in range(1, 4):
        countXG = 0
        countOG = 0
        for j in range(1, 4):
            if pole[i][j] == 'X':
                countXG += 1
            elif pole[i][j] == 'O':
                countOG += 1
            if countXG == 3:
                return f'Побеждает {player1} по горизонтали!!!'
            elif countOG == 3:
                return f'Побеждает {player2} по горизонтали!!!'
    for i in range(1, 4):
        countXV = 0
        countOV = 0
        for j in range(1, 4):
            if pole[j][i] == 'X':
                countXV += 1
            elif pole[j][i] == 'O':
                countOV += 1
            if countXV == 3:
                return f'Побеждает {player1} по вертикали!!!'
            elif countOV == 3:
                return f'Побеждает {player2} по вертикали!!!'
    for j in range(1, 4):
        if pole[j][j] == 'X':
            countXD += 1
        elif pole[j][j] == 'O':
            countOD += 1
        if countXD == 3:
            return f'Побеждает {player1} по диагонали!!!'
        elif countOD == 3:
            return f'Побеждает {player2} по диагонали!!!'
    if pole[3][1] == 'X' and pole[2][2] == 'X' and pole[1][3] == 'X':
        return f'Побеждает {player1} по диагонали!!!'
    elif pole[3][1] == 'O' and pole[2][2] == 'O' and pole[1][3] == 'O':
        return f'Побеждает {player2} по диагонали!!!'
    if HowHodsCount() == 9:
        return f'Ничья!!!'
    return None

def StartGame(player1, player2):
   global help
   XO = 'X'
   hodList = []
   PoleScreen()
   hod = hod_player(player1)
   countHod = 0
   while True:
         if (hod == 'Start' or hod == 'New Game') and countHod == 0:
             print('Игра только началась!')
             hod = hod_player(player1) if XO == 'X' else hod_player(player2)
         elif (hod == 'Start' or hod == 'New Game') and countHod > 0:
             hod = input('Вы уверены что хотите начать игру сначала? (Y/N): ')
             if hod == "Y":
                print('Партия завершена!')
                NewGame()
                StartGame(input('Введите имя первого игрока '), input('Введите имя второго игрока '))
                break
             elif hod == 'N':
                hod = hod_player(player1) if XO == 'X' else hod_player(player2)
             else:
                print('Игра продолжается!')
                hod = hod_player(player1) if XO == 'X' else hod_player(player2)
         elif hod == 'Help':
            print(help)
            hod = hod_player(player1) if XO == 'X' else hod_player(player2)
         elif hod == 'Pole':
            clean_screen(10)
            PoleScreen()
            hod = hod_player(player1) if XO == 'X' else hod_player(player2)
         elif hod == 'Exit':
            break
         else:
            hodList = list(hod)
            hodList.pop(1)
            print(hodList)
            if pole[int(hodList[0])+1][int(hodList[1])+1] == '-' and int(hodList[0]) <= 2 and int(hodList[1]) <= 2 and type(int(hodList[0])) == int and type(int(hodList[1])) == int:
                pole[int(hodList[0])+1].pop(int(hodList[1])+1)
                pole[int(hodList[0])+1].insert(int(hodList[1])+1, XO)
                PoleScreen()
                if WhoWinner() is not None:
                    print(WhoWinner())
                    print('Партия завершена!')
                    hod = input('Хотите попробовать еще? (Y/N): ')
                    if hod == "Y":
                        NewGame()
                        StartGame(player1, player2)
                        break
                    elif hod == 'N':
                        break
                    break
                XO = 'O' if countHod % 2 == 0 else 'X'
                hod = hod_player(player1) if XO == 'X' else hod_player(player2)
                countHod += 1
            else:
                print('Неверный ход, ходите заного')
                hod = hod_player(player1) if XO == 'X' else hod_player(player2)

pole = []
NewGame()
help = (f'''Добро пожаловать в консольную игру "Крестики - Нулики" 
Вам предоставлен функционал команд с помощью которых 
Вы сможете управлять программой. Игра рассчитана для одного-двух человек.
Искусственный интеллект отсутствует - его Мы добавим в следующих обновлениях.
Правила ходов: Для того чтобы корректно выполнить ход, необходимо
указать номер ячейки в формате двух чисел через пробел в диапазоне
от 0 до 2 (Примеры: 0 0, 0 1, 0 2, 1 0, 1 1, 1 2, 2 0, 2 1, 2 0)
Первый ход выполняет X, затем O и так далее по очереди.
Победа засчитывается в случаи если ходя-бы один из игроков
сумел записать свое значение 3 раза в ряд, если ячейка уже заполнена, то
такой ход не принимается и игрок ходит повторно.
\n {pole[0]} \n {pole[1]} \n {pole[2]} \n {pole[3]} \n
Доступные команды:
1. New Game - Создает новую игру и завершает текущую партию.
2. Start - Необходимо ввести перед началом игры
3. Help - Для вывода данного сообщения повторно
4. Pole - Выводит на экран поле текущей сессии
5. Exit завершает программу.''')
print(help)
player1 = input('Введите имя первого игрока ')
player2 = input('Введите имя второго игрока ')
StartGame(player1, player2)

