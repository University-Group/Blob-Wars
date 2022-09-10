from termcolor import colored

class State :

    def __init__(self, cells, played) :
        self.cells = cells
        self.played = played
        self.weight = None

    def nextState(self):
        who = 1 - self.played
        states = []
        for i,row in enumerate(self.cells):
            for j,col in enumerate(row):
                if col == who:
                    movements = self.canMove(i,j)
                    for k in movements:
                        state = self.move(k,who,i,j)
                        states.append(state)
        return states
    def inCells(self,i,j):
        return i >= 0 and i < len(self.cells) and j >= 0 and j < len(self.cells[0])
    
    def isVailibleCell(self,i,j):
        return self.inCells(i,j) and self.cells[i][j] == -5
    
    def canMove(self,i,j):
        lst1 = [
            (1,i-1,j-1),(1,i-1,j),(1,i-1,j+1),
            (1,i,j-1),(1,i,j+1),
            (1,i+1,j-1),(1,i+1,j),(1,i+1,j+1)
        ]
        lst2 = [
            (0,i-2,j-2),(0,i-2,j-1),(0,i-2,j),(0,i-2,j+1),(0,i-2,j+2),
            (0,i-1,j-2),(0,i-1,j+2),
            (0,i,j-2),(0,i,j+2),
            (0,i+1,j-2),(0,i+1,j+2),
            (0,i+2,j-2),(0,i+2,j-1),(0,i+2,j),(0,i+2,j+1),(0,i+2,j+2)
        ]
        lst1.extend(lst2)
        lst = []
        for item in lst1:
            if self.isVailibleCell(item[1],item[2]):
                lst.append(item)
        return lst
    
    def move(self, item, who, x, y):# item (type,i,j) x , y is From
        newArr = self.copy()
        newArr[item[1]][item[2]] = who
        if item[0] == 0:
            newArr[x][y] = -5
        i = item[1]
        j = item[2]
        lst1 = [
            (i-1,j-1),(i-1,j),(i-1,j+1),
            (i,j-1),(i,j+1),
            (i+1,j-1),(i+1,j),(i+1,j+1)
        ]
        for el in lst1:
            if self.inCells(el[0],el[1]) and newArr[el[0]][el[1]] == self.played:
                newArr[el[0]][el[1]] = who
        return State(newArr, who)

    def moveUser(self,fromX,fromY,toX,toY):
        who = 1 - self.played
        if self.inCells(fromX,fromY) and self.cells[fromX][fromY] == 1 - self.played:
            movements = self.canMove(fromX,fromY)
            if (1,toX,toY) in movements:
                return  self.move((1,toX,toY),who,fromX,fromY)
            if (0,toX,toY) in movements:
                return  self.move((0,toX,toY),who,fromX,fromY)
            print("uncorrect To point")
            return False
        print("uncorrect From point")
        return False

    def displayBlob(self):
        print('\n')
        print(colored("*" * 50, "cyan"))
        print('\t',end="")
        for i in range(len(self.cells)):
            print(colored(i, 'green'), end="\t")
        print('\n')
        for i,row in enumerate(self.cells):
            print(colored(i, 'green'), end="\t")
            for col in row :
                if(col == 1) :
                    print(colored('P1', 'blue'), end="")
                elif(col == 0) :
                    print(colored('P2', 'yellow'), end="")
                else:
                    print('-', end="")
                print("\t", end="")
            print("\n\n")
        print(f"Player Score:  {self.getScore(0)}\n")
        print(f"Software Score:  {self.getScore(1)}\n")
        print(colored("*" * 50, "cyan"))

    def getScore(self, player):
        score = 0
        for row in self.cells:
            for col in row:
                if col == player:
                    score += 1
        return score
    
    def isFull(self):
        full = True
        for row in self.cells :
            for col in row :
                if(col == -5):
                    full = False
        if(full == True):
            return True
        else:
            return False
    
    def isGoal(self):
        if self.isFull():
            return True
        elif not self.isFull() and len(self.nextState()) == 0:
            return True
        return False

    def evalutionBlob(self):
        player1Score = self.getScore(self.played)
        player2Score = self.getScore(1-self.played)
        self.weight = -1*(player1Score - player2Score)

    def copy(self) :
        listall = []
        for row in self.cells :
            listall.append(row.copy())
        return listall

class Logic:

    @staticmethod
    def startGame(init):
        inp = input(colored("\nChoose The Level Of Game:\n 1.Easy\n 2.Hard\n", 'green'))
        while inp.isnumeric() != True or int(inp) < 1 or int(inp) > 2 :
            inp = input(colored("\nChoose The Level Of Game:\n 1.Easy\n 2.Hard\n", 'green'))
        if(int(inp) == 1):
            Logic.playGame(init, 2)
        elif(int(inp) == 2):
            Logic.playGame(init, 4)

    @staticmethod
    def playGame(state, Level):
        while state.isGoal() == False:
            state.displayBlob()
            if(state.played == 1):
                state = State(Logic.Me(state).copy(), 0)
            elif(state.played == 0):
                state = State(Logic.Software(state, Level).copy(), 1)
        state.displayBlob()
        print(state.isGoal())
        Logic.checkEndOfTheGame(state)
    
    # Player 2
    @staticmethod
    def Me(state):
        #states = state.nextState()
        # inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
        # while inp.isnumeric() != True or int(inp) < 1 or int(inp) > len(states) :
        #     inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
        # state = states[int(inp) - 1]
        loop = True
        while loop == True:
            fromX , fromY = input("Enter From Position x y \n(like 8 7 ):").split()
            toX , toY = input("Enter to Position x y \n(like 8 7 ):").split()
            st = state.moveUser(int(fromX),int(fromY),int(toX),int(toY))
            if st != False:
                loop = False
        return st

    # Player 1
    @staticmethod
    def Software(state, Level):
        return Logic.Max(state, Level, None)

    @staticmethod
    def Max(state, Level, Beta):
        endGame = Logic.checkEndOfTheGame2(state)
        if (state.isGoal() and endGame == 1):
            state.weight = -1000
            return
        elif (state.isGoal() and endGame == 2):
            state.weight = 1000
            return
        elif (state.isGoal() and endGame == 3):
            state.weight = 0
            return
        if(Level == 0):
            state.evalutionBlob()
            return

        list = []
        states = state.nextState()
        for st in states:
            Logic.Min(st, Level - 1, state.weight)
            list.append(st.weight)
            if(state.weight == None):
                state.weight = st.weight
            else:
                if state.weight is None:
                    state.weight = st.weight
                else:
                    state.weight = max(state.weight, st.weight)

            if(Beta and Beta <= st.weight):
                # print("*************************************************Hello From Beta Cut")
                break

        return states[list.index(state.weight)]

    @staticmethod
    def Min(state, Level, Alpha):
        endGame = Logic.checkEndOfTheGame2(state)
        if (state.isGoal() and endGame == 1):
            state.weight = 1000
            return
        elif (state.isGoal() and endGame == 2):
            state.weight = -1000
            return
        elif (state.isGoal() and endGame == 3):
            state.weight = 0
            return
        if(Level == 0):
            state.evalutionBlob()
            return
        list = []
        states = state.nextState()
        for st in states:
            Logic.Max(st, Level - 1, state.weight)
            list.append(st.weight)
            if(state.weight == None):
                state.weight = st.weight
            else:
                if state.weight is None:
                    state.weight = st.weight
                else:    
                    state.weight = min(state.weight, st.weight)

            if(Alpha and Alpha >= st.weight):
                break

        return states[list.index(state.weight)]
    
    @staticmethod
    def checkEndOfTheGame2(state):
        if state.isFull():
            player1Score = state.getScore(1)
            player2Score = state.getScore(0)
            if player1Score > player2Score:
                return 1
            elif player1Score < player2Score:
                return 2
            else:
                return 3
        elif state.played == 1:
            return 1
        else:
            return 2
    
    @staticmethod
    def checkEndOfTheGame(state):
        if state.isFull():
            player1Score = state.getScore(1)
            player2Score = state.getScore(0)
            if player1Score > player2Score:
                print("\n\tSoftware has won the game\n")
            elif player1Score < player2Score:
                print("\n\tPlayer has won the game\n")
            else:
                print("Draw")
        elif state.played == 1:
            print("\n\tSoftware has won the game\n")
        else:
            print("\n\tPlayer has won the game\n")

############################### Main ###############################

def generateState(size):
        board = [[-5 for x in range(size)] for y in range(size)]
        board[0][0] = 1
        board[0][size-1] = 1
        board[size-1][0] = 0
        board[size-1][size-1] = 0
        return board
size = 0
size = input("choose size of board : ")
init = State(generateState(int(size)), 1)  # 1 For P1 , 0 For P2 , -5 For Empty

Logic.startGame(init)

