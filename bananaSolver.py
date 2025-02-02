def toFreq(strList: list[str]) -> dict[str, int]:
    """
    Make a frequency dictionary corresponding to each element in strList

    @param (list[str]) strList: list (or other iterable) containing
                                strings (repititions allowed)
    @returns (dict[str,int]) for each key, it's value is how many times it appears in strList

    Exemple:
    >>> toFreq("hellothere")
    {'h':2, 'e':3, 'l':2, 'o':1, 't':1, 'r':1}
    """
    frequencies = {}
    for s in strList: 
        if s not in frequencies:
            frequencies[s] = 0
        frequencies[s] += 1
    return frequencies

def freqSousFreq(freq1: dict[str, int], freq2: dict[str, int]) -> bool:
    """
    Verifie que tout les lettres de freq1 apparaissent max le meme
    nombre de fois dans freq2 et minimum 1 fois (on peut pas avoir 
    un lettre qui est dans freq1 et pas freq2)

    @param (dict[str,int]) freq1, freq2: dictionnaire representant la frequence
                                         de chaque caractere dans un liste
    @returns (bool) True si pour tout caractere c de freq1, c dans freq2 et freq1[c] <= freq2[c]. 
                    Sinon False
    """
    
    # pour tout caractere c de freq 1, verifie qu'il est present dans freq 2
    # et que sa frequence dans freq1 ne depase pas celle de freq2
    return all(c in freq2 and freq1[c] <= freq2[c] for c in freq1)

def addCol(grid: list[list[str]], left=False):
    """Ajoute un colonne a gauche ou a droite de la grille"""
    
    for row in grid:
        if left:
            row.insert(0, (".", ""))
        else:
            row.append((".", ""))

def addRow(grid: list[list[str]], top=False):
    """Ajoute un ligne en haut ou en bas de la grille"""
    nCols = len(grid[0])
    if top:
        grid.insert(0, [(".", "")]*nCols)
    else:
        grid.append([(".", "")]*nCols)


def calcGridPos(string: str, pos: tuple[int, int], vertical: bool = False) -> list[tuple[int,int,str,str]]:
    """
    Calculates the position of letters to place on the grid, vertically or horizontally, starting from the starting position
    
    @param (str) string: the string that we would like to place on the grid
    @param (tuple[int,int]) pos: the starting position of the string placement (the first character of the string will be placed here)
    @param (bool) vertical: wether or not we place the word vertically or horizontally on the grid (default = False)

    @return (list[tuple[int,int, str,str]]) a list of all the positions that characters were placed on in the grid
    """
    r, c = pos
    toPlace = []

    # places the letters of a string on each position of the grid
    for offset,char in enumerate(string):
        if vertical: # places the string vertically down
            toPlace.append((r+offset, c, char, 'v'))
        else: # places the string horizontally right
            toPlace.append((r,c+offset, char, 'h'))
    
    return toPlace

def placeWordFromPos(grid, allowedLetters, posList) -> bool:
    """
    Places characters on the grid in the positions returned by calcGridPos 
    """
    usableOnBoard = []
    lettersInWord = []

    for r,c,char,d in posList:
        # si la lettre n'est pas parmis les lettres dans notre main, et la case du grille est vide, on ne peut pas le poser
        if char not in allowedLetters and grid[r][c][0] == '.':
            return False
        else: # si c'est un lettre qu'on peut utiliser
            # si la case du grille a deja un lettre
            if grid[r][c][0] != '.':
                usableOnBoard.append(grid[r][c][0])
            else: # sinon, place la lettre sur le grille
                grid[r][c] = (char,d)
            lettersInWord.append(char)

    # verifie qu'on n'a pas placee plus de lettre que nous avons le droit
    return freqSousFreq(toFreq(lettersInWord), toFreq(allowedLetters + usableOnBoard))

def adjacentValid(wordlist: set[str], grid, pos, char, vertical: bool = False) -> bool:
    """
    Verify that the concatination of the letter `pos` with the letters adjacent/around it, also forms a valid word 

    Idea:
    - We make a string of all letters before the position
    - We make a string of all the characters after the position
    - We then make sure if the concatination of all this is a valid word

    @param (set[str]) wordlist: the set of valid words
    @param grid: letters that are currently placed on the grid
    @param (tuple[int,int]) pos: position of letter to place
    @param (str) char: the character we want to place here
    @param vertical: if we are looking on the vertical axis or not
    
    @returns (bool) if it forms a valid word or not
    """

    side1 = char
    side2 = ""

    r, c = pos
    if vertical:
        tempr = r
        r -= 1 # car on met char au pos r
        while (r >= 0 and grid[r][c][0] != "."):
            side1 = grid[r][c][0] + side1
            r -= 1
        r = tempr + 1
        while (len(grid) > r and grid[r][c][0] != "."):
            side2 = side2 + grid[r][c][0]
            r += 1
    else:
        tempc = c
        c -= 1 # car on met char au pos c
        while (c >= 0 and grid[r][c][0] != "."):
            side1 = grid[r][c][0] + side1
            c -= 1
        c = tempc + 1
        while (c < len(grid[0]) and grid[r][c][0] != "."):
            side2 = side2 + grid[r][c][0]
            c += 1
    # print(f"joined word: '{side1+side2}'")
    return (side1+side2) in wordlist

def allAdjacentValid(wordlist: set[str], grid, gridSize, posList) -> bool:
    """posList is the list of the same form as the one returned by calcGridPos"""
    gridR, gridC = gridSize
    r,c,char,direction = posList[0]
    # on verifie deja que le mot qu'on pose ne fait pas un concatenation menant a un mot invalide
    allValid = adjacentValid(wordlist, grid, (r,c), char, direction == 'v') #True
    i = 0
    while allValid and i < len(posList):
        r,c,char,_ = posList[i]

        hasAdjHorizontal = gridR > r >= 0 and ((gridC >= c > 0 and grid[r][c-1][0] != '.') or (gridC-1 > c >= 0 and grid[r][c+1][0] != '.'))
        
        hasAdjVertical = gridC > c >= 0 and ((gridR >= r > 0 and grid[r-1][c][0] != '.') or (gridR-1 > r >= 0 and grid[r+1][c][0] != '.'))
        
        if hasAdjHorizontal and direction == 'v':
            allValid = adjacentValid(wordlist, grid, (r,c), char, vertical=False)

        if hasAdjVertical and direction == 'h':
            allValid = adjacentValid(wordlist, grid, (r,c), char, vertical=True)
        
        i += 1

    return allValid

def intersectValid(grid, positions) -> bool:
    """
    Given the letter grid and a list of positions where we want to place letters, check if all intersections with other words are valid
    ex: here we place the word NONE among the existing words JUST, UNION and THORN

        J U S T
          N   H
          I   O
          O   R
          N O N E
    
    @param (list[list[tuple[char,char]]]) grid: the grid containing our characters
    @param (list[tulpe[int,int,char,char]]) positions: list of position tuples of form (row, column, character, direction ['v', 'c'])

    @returns (bool) wether the words can intersect and still be valid

    Premis:
    For each position in `positions`, if there is a letter on one of those positions on the grid then make sure it is the same letter

    """

    for r,c,char,_ in positions:
        gridChar = grid[r][c][0] # char already on grid
        # if the grid char is a letter and doesn't match the word position char
        if gridChar != '.' and gridChar != char:
            return False

    return True


def cleanGridScreen(lst: list[list[str]]) -> str:
    """formate just un string representant la grille de tuples [[(char, direction),...],...]"""
    out = ""
    for line in lst:
        out += " ".join(map(lambda x: x[0], line)) + "\n"
    
    return out



def rectifyBounds(grid, gridSize: tuple[int,int], positions) -> tuple[tuple[int,int], tuple[int,int]]:
    """
    Modifies the size of the grid depending on the positions of letters we would like to place on it.

    @param grid: the grid of letters
    @param gridSize: the current size of the grid
    @param positions: the positions we will use to determin if we must rectify anything

    @returns (tuple, tuple) of new gridSize AND new gridOffsets
    """
    r1,c1,_,d = positions[0]
    r2,c2,_,_ = positions[-1]

    nGridR, nGridC = gridSize

    # on determine de combien de cases on depasse pour chaque cote
    topRow = abs(r1) if r1 < 0 else 0
    bottomRow = r2 - nGridR + 1 if r2 >= nGridR else 0

    leftCol = abs(c1) if c1 < 0 else 0
    rightCol = c2 - nGridC + 1 if c2 >= nGridC else 0

    nGridC += rightCol + leftCol
    nGridR += topRow + bottomRow

    # ajoute au cotes concerné, le nombre de colonnes ou lignes necessaires
    if d == 'v':
        for _ in range(topRow):
            addRow(grid, top=True)

        for _ in range(bottomRow):
            addRow(grid)
    else:
        for _ in range(leftCol):
            addCol(grid, left=True)

        for _ in range(rightCol):
            addCol(grid)

    # on change seulement le offset si on ajoute un ligne au debut, ou un colonne au debut
    return (nGridR, nGridC), (topRow, leftCol)

def bananaSolverRec(
        wordlist: set[str],\
        offsets: tuple[int, int],\
        gridSize: tuple[int,int],\
        grid: list[list[tuple[str, str]]],\
        toTreat: list[tuple[int,int]],\
        letters: list[str],
    ) -> list[list[tuple[str, str]]]:
    """
    Finds a table of Banana Split where all of our given letters are used up in the game

    @param wordlist: a list containing all words we can do with our current letters
    @param offsets: the global offsets that we will apply to the coordinates in toTreat. 
                   This is done because we might need to increase the grid's size
    @param gridSize: contains the current number of rows and columns in the grid
    @param grid: the grid where we will place each letter of the game
    @param toTreat: a list of all positions we must go over
    @param letters: the list of letters that we must place on the grid

    @returns the first found result grid that uses up all letters. If not such grids are found, it returns an empty list []
    """
    if not toTreat and letters:
        return []
    elif not letters:
        return grid
    else:
        result = []
        ro, co = offsets
        r, c = toTreat.pop()
        posChar, d = grid[r+ro][c+co]

        # all words that contain the character at (r,c) + the characters that the word could intersect with from (r,c)
        wordsAtPos = []
        for word in wordlist:
            # pour pouvoir avoir des intersections entre plusieurs mot, il faut les lettres possibles d'intersections deja sur la grille
            templetters = letters.copy()
            if d == 'v': # si le mot d'origine est vertical, on regarde sur l'horizontal ou on va placer
                start = c+co - len(word)
                end = c+co + len(word) - 1
                if end >= gridSize[1]: end = gridSize[1]
                if start < 0: start = 0
                for i in range(start, end):
                    templetters.append(grid[r+ro][i][0])
            else:
                start = r+ro - len(word)
                end = r+co + len(word) - 1
                if end > gridSize[0]: end = gridSize[0]
                if start < 0: start = 0
                for i in range(start, end):
                    templetters.append(grid[i][c+co][0])
            if len(word) > 1 and posChar in word and freqSousFreq(toFreq(word), toFreq(templetters)):
                wordsAtPos.append(word)


        i = 0
        while not result and i < len(wordsAtPos):
            word: str = wordsAtPos[i]
            posInWord = word.index(posChar)

            # the "offset" or "character alignment" between the grid word and this word
            diffPos = (r+ro, c+co-posInWord) if d == 'v' else (r+ro-posInWord, c+co)
            newPositions = calcGridPos(word, diffPos, d == 'h')

            # resize grid if needed
            copiedGrid = [line.copy() for line in grid]
            newGridSize, offsetDiffs = rectifyBounds(copiedGrid, gridSize, newPositions)
            nro, nco = offsetDiffs

            # we only need to apply the nro and nco because the previous offsets have already been applied at creation of these positions
            newPositions = [(rr+nro, cc+nco, char, direction) for rr, cc, char, direction in newPositions]
            alreadyOnGrid = []
            for nr, nc, _, _ in newPositions:
                if copiedGrid[nr][nc][0] != '.':
                    alreadyOnGrid.append((nr,nc))

            # check if it's a valid word that can be placed at this position
            icond = intersectValid(copiedGrid, newPositions)
            posable = placeWordFromPos(copiedGrid, letters, newPositions)
            acond = allAdjacentValid(wordlist, copiedGrid, newGridSize, newPositions) 
            # if not (icond and acond and posable): print("\033[35;5;196mVIBE CHECK FAILED!\033[0m")

            if acond and icond and posable:
                # start making copies for the next recursive call.
                # we do this because the current versions will be used for the next iterations of the while loop
                copiedToTreat = toTreat.copy()
                copiedLetters = letters.copy()

                # update the toTreat for the next iteration
                for nr, nc, nChar, _ in newPositions:
                    # remove the applied offsets from the positions, that way we can store the relative positions from offsets. 
                    # Offsets are applied each call (because they change). We do this intead of applying them to all positions in toTreat at each call (it would be less efficient)
                    origPos = (nr-ro-nro, nc-co-nco) 
                    if (nr,nc) not in alreadyOnGrid and origPos != (r,c):
                        copiedToTreat.append(origPos)
                        copiedLetters.remove(nChar)

                            
                result = bananaSolverRec(wordlist, (ro+nro, co+nco), newGridSize, copiedGrid, copiedToTreat, copiedLetters)
            i += 1

        # if no words can be placed on the current position, try on the next position
        if not result and i == len(wordsAtPos):

            result = bananaSolverRec(wordlist.copy(),
                             offsets,
                             gridSize,
                             [line.copy() for line in grid],
                             toTreat.copy(),
                             letters.copy())
        
        return result

def toNormalCharMat(grid: list[list[tuple[str,str]]]):
    """
    Transforms each row of our structured grid from:
    [(str,str), ...] to [str, ...]
    """

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            grid[r][c] = grid[r][c][0]

def bananaSolver(wordlist, letters: str) -> list[list[str]]:
    """
    Fonction d'initiation du bananaSolver
    
    @param (iterable de str) wordlist: un objet iterable contennant tout les mots valides (notre dictionnaire)
    @param (str) lettres: string contennat tout les lettres que nous pouvons utiliser

    @returns le tableau resultant d'un bananagram utilisant tout les lettres donnees
    """
    lettersList = list(letters)
    lettersFreq = toFreq(lettersList)
    startingWords = [word for word in wordlist if freqSousFreq(toFreq(word), lettersFreq)]
    # a copy here is not ideal. But the O(1) of the set inclusion is pretty good so...
    usableWords = set(startingWords)

    result = []
    i = 0
    while not result and i < len(startingWords):
        word = startingWords[i]
        # print(word)
        copiedLetters = lettersList.copy()
        toTreat = []
        grid = [[]]
        for i,char in enumerate(word):
            copiedLetters.remove(char)
            toTreat.append( (0, i) )
            grid[0].append( (char, 'h') )

        result = bananaSolverRec(usableWords, (0,0), (len(grid), len(grid[0])), grid, toTreat, copiedLetters)
        i += 1

    toNormalCharMat(result)
    return result
