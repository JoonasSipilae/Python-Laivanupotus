

"""
@ Joonas Sipilä
22.8.2021

Laivanupotus
"""

# main
def main():
    print("\nTervetuloa pelaamaan laivanupotusta"+"\n-----------------------------------\n")

    # menee ReadFiles() jossa luetaan tekstitiedostot laivojen sijainneista 
    Ships1, Ships2, ValidFiles = ReadFiles()
    if not ValidFiles:
        exit()

    # pidetään kirjaa upotettujen laivojen lukumäärästä
    SunkenShips1 = 0
    SunkenShips2 = 0

    # laudat joihin merkattu laivat
    ShipPositionBoard1 = MakeBoard(True, Ships1)
    ShipPositionBoard2 = MakeBoard(True, Ships2)

    # laudat jotka näytetään pelaajille
    PlayBoard1 = MakeBoard(False, None)
    PlayBoard2 = MakeBoard(False, None)

    # turn = True -> pelaaja 1 vuoro
    # turn = False -> pelaaja 2 vuoro
    turn = True

    while True:
        # vuoron alussa määritellään mitä taulua käsitellään.
        # pelaajan 1 ja 2 vuoroilla käsitellään omia tauluja.
        if turn == True:
            ShipPositionBoard = ShipPositionBoard2
            PlayBoard = PlayBoard1
            SunkenShips = SunkenShips2
            print("Pelaajan 1 vuoro:")
        else:
            ShipPositionBoard = ShipPositionBoard1
            PlayBoard = PlayBoard2
            SunkenShips = SunkenShips1
            print("Pelaajan 2 vuoro:")

        # tulostaa pelaajan upottamien laivojen määrän
        PrintBoard(PlayBoard)
        print("Upotetut laivat = ", SunkenShips)

        # vertaa pelaajan antamia koordinaatteja vihollisen laivoja
        # sisältävään tauluun, palauttaa tiedon osuiko yms.
        col, row = AskCoordinates()
        bombardment, mark = CheckCollision(row, col, ShipPositionBoard, PlayBoard)

        # jos ruutu on pommitettu jo aikaisemmin
        while bombardment == 3:
            print("ruutu on jo pommitettu aikaisemmin, Anna uudet koordinaatit")
            col, row = AskCoordinates()
            bombardment, mark = CheckCollision(row, col, ShipPositionBoard, PlayBoard)

        # jos osui, ei uponnut
        if bombardment == 1:
            print("osui, ei uponnut")
            print("----------------\n")

        # jos osui, upposi
        elif bombardment == 2:
            print("osui, upposi")
            print("----------------\n")
            SunkenShips += 1
            SunkShip(mark, ShipPositionBoard, PlayBoard)
            if SunkenShips == 10:
                break

        #jos huti        
        else:
            print("ohi")
            print("----------------\n")

        if turn == True:
            # palauttaa palaajan 1 tai 2 muuttuneet tiedot omiin tauluihin
            ShipPositionBoard2 = ShipPositionBoard
            PlayBoard1 = PlayBoard
            SunkenShips2 = SunkenShips
        else:
            ShipPositionBoard1 = ShipPositionBoard
            PlayBoard2 = PlayBoard
            SunkenShips1 = SunkenShips
        turn = Turn(turn)


    # peli on päättynyt, näytetään molempien pelaajien laivat
    print("Pelaaja", turn + 1, "voitti")
    ShipPositionBoard1 = MakeBoard(True, Ships1)
    ShipPositionBoard2 = MakeBoard(True, Ships2)

    print("\nPelaaja 1 lauta:")
    PrintBoard(ShipPositionBoard1)
    print("\nPelaaja 2 lauta:")
    PrintBoard(ShipPositionBoard2)

"""
Lukee tekstitiedostot ja palauttaa laivojen tiedot listoina
Palauttaa myös boolin ValidFiles, joka kertoo jatketaanko ohjelmaa
"""
def ReadFiles():
    # avaa ja tallentaa pelaajan 1 laivojen sijainnit
    ValidFiles = True
    Data1 = open("player1_ships.txt")
    Ships1 = Data1.read().splitlines()
    Data1.close()

    # avaa ja tallentaa pelaajan 2 laivojen sijainnit
    Data2 = open("player2_ships.txt")
    Ships2 = Data2.read().splitlines()
    Data2.close()

    # tarkistaa että pelaajien tekstitiedostoissa on oikea määrä (10) laivoja
    if len(Ships1) != 10:
        print("\n VIRHE: 1 pelaajan Tekstitiedostossa tulee olla 10 riviä tekstiä")
        ValidFiles = False

    if len(Ships2) != 10:
        print("\n VIRHE: 2 pelaajan Tekstitiedostossa tulee olla 10 riviä tekstiä")
        ValidFiles = False

    return Ships1, Ships2, ValidFiles

def Turn(turn):
    # määrittää vuoron
    return (turn+1) % 2


def SunkShip(mark, ShipPositionBoard, PlayBoard):
    for i in range(10):
        for j in range(10):
            char_to_int = ord(ShipPositionBoard[i][j]) - 97
            if char_to_int == int(mark):
                PlayBoard[i][j] = "#"


def AskCoordinates():
    while True:
        try:
            koordinaatti = input("Syötä koordinaatti muodossa x,y > ")
            colrow = koordinaatti.split(",")
            col = int(colrow[0]) - 1
            row = int(colrow[1]) - 1
            break
        # virhekäsittely väärin annetulle koordinaatille
        except ValueError:
            print("Anna koordinaatti muodossa x,y")

    if col < -1 or col > 8 or row < -1 or row > 8:
        print("Anna koordinaatit 0-9 välistä")
        col, row = AskCoordinates()
    return col, row



"""
Tarkastaa mitä annetuissa koordinaateissa on

col = laudan sarake
row = laudan rivi
ShipPositionBoard = tieto laivojen sijainneista
PlayBoard = pelilauta joka näytetään pelaajalle

Metodi palauttaa kaksi asiaa:

Numeron siitä mitä on tapahtunut:
0 = ohi
1 = osuttu
2 = osuttu ja upotettu
3 = osuttu samaan kohtaan uudestaan

Jos osuttu laiva upotetaan, palautetaan myös laivan numero.
Muulloin palautetaan merkin tilalla None
"""

def CheckCollision(col, row, ShipPositionBoard, PlayBoard):

    # laivat merkattu ShipPositionBoardiin numerolla
    mark = ShipPositionBoard[col][row]

    # laivaan on osuttu
    if mark.isdigit():
        # ShipPositionBoardilla kyseisen laivan numero muuttuu sitä vastaavaksi kirjaimeksi
        # 0 -> a
        # 1 -> b
        # 2 -> c
        # ...
        ShipPositionBoard[col][row] = str(chr(int(mark) + 97))
        # pelaajalle kyseinen kohta merkataan osutuksi
        PlayBoard[col][row] = "X"
        # laivaan on osuttu, tarkastetaan onko se upotettu
        if Sunken(ShipPositionBoard, mark):
            return 2, mark
        else:
            return 1, None
    # osutaan osuttuun kohtaan
    elif PlayBoard[col][row] == "X" or PlayBoard[col][row] == "#" or PlayBoard[col][row] == "O":
        return 3, None

    # osutaan ohi
    PlayBoard[col][row] = "O"
    return 0, None

"""
Tarkastaa onko osuttu laiva upotettu

Board = lauta mitä tarkastellaan
mark = laivan oma uniikki numeronsa
"""
def Sunken(Board, mark):
    # käydään jokainen kohta lautaa läpi
    for col in range(10):
        for row in range(10):
            # vastaan tulee upottamaton osa laivaa
            if Board[col][row] == mark:
                # laiva ei ole uponnut
                return False
    # laiva on uponnut
    return True


"""
Luo lautoja

PutShipsInBoard = boolean joka määrittää lisätäänkö laudan koordinaatteihin laivoja
DataInRows = lista laivojen pituuksista ja sijainneista

"""
def MakeBoard(PutShipsInBoard, DataInRows):
    # luo tyhjän laudan
    EmptyBoard = [["~" for y in range(10)] for x in range(10)]
    # laittaa laivoja koordinaatteihin, jos PutShipsInBoard = True
    if PutShipsInBoard:
        Board = MarkBoard(EmptyBoard, DataInRows)
    # palauttaa laudat
        return Board
    return EmptyBoard

"""
Board = lauta mihin koordinaatit laivoista asetetaan
DataInRows = tieto laivoijen pituuksista ja sijainneista

palauttaa laudan 2D-listana jossa tieto laivoista
"""
def MarkBoard(Board, DataInRows):
    # jokaisella uniikilla laivalla on oma numeronsa
    ShipNumber = 0
    for row in DataInRows:

        ShipID = str(ShipNumber)
        vaakasuunta = False
        laivanpituus = 0

        # laivan pituus
        if row[0] == "L":
            laivanpituus = 4
        elif row[0] == "R":
            laivanpituus = 3
        elif row[0] == "H":
            laivanpituus = 2
        elif row[0] == "S":
            laivanpituus = 1
        else:
            # virhekäsittely
            exit("Merkitse laivat käyttämällä L,R,H,S")

        # laivan orientaatio
        if row[1] == "V" or row[1] == "P":
            pass
        else:
            # virhekäsittely
            exit("Merkitse suunta käyttämällä V tai P")

        # orientaatiolla vain kaksi vaihtoehtoa -> true tai false = vaaka tai pysty
        if row[1] == "V":
            vaakasuunta = True

        # laivojen aloituspisteet laudalla
        # -1 jotta koordinaatit täsmää lautaan pelatessa
        StartX = int(row[2]) - 1
        StartY = int(row[4]) - 1
        if StartX == -1:
            StartX = 9
        if StartY == -1:
            StartY = 9

        # asettaa laivan tauluun oikeassa orientaatiossa
        if vaakasuunta:
            for x in range(laivanpituus):
                Board[StartY][StartX + x] = ShipID
        else:
            for y in range(laivanpituus):
                Board[StartY + y][StartX] = ShipID
        ShipNumber += 1

    return Board

"""
Tulostaa halutun laudan
Board = 10x10 2D-lista
"""
def PrintBoard(Board):
    print(" 1234567890")
    for column in range(10):
        RowToPrint = str((column + 1) % 10) + ""
        for row in range(10):
            RowToPrint += Board[column][row]
        print(RowToPrint)

main()
