import sqlite3
from datetime import datetime

con = sqlite3.connect("game.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")


PLAYER = """
CREATE TABLE IF NOT EXISTS Player (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);
"""
BOARD_GAME = """
CREATE TABLE IF NOT EXISTS Boardgame (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);
"""
GAME_SESSION = """
CREATE TABLE IF NOT EXISTS Gamesession (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score TEXT NOT NULL,
    date DATE,
    boardgame_id INTEGER,
    FOREIGN KEY (boardgame_id) REFERENCES Boardgame(id)
);
"""
PARTICIPATE = """
CREATE TABLE IF NOT EXISTS Participate(
    player_id INTEGER,
    gamesession_id INTEGER,
    PRIMARY KEY (player_id, gamesession_id),
    FOREIGN KEY (player_id) REFERENCES Player(id),
    FOREIGN KEY (gamesession_id) REFERENCES Gamesession(id)
);
"""

cur.execute(PLAYER)
cur.execute(BOARD_GAME)
cur.execute(GAME_SESSION)   
cur.execute(PARTICIPATE)
con.commit()

def input_correct():
    ans = input("Is the input correct [Y/n]").lower()

    if not ans or ans[0] == "y":
        return True
    else:
        return False

def add_player():
    while True:
        name = input("Enter player name: ") 

        print()
        print("You entered:")
        print(f"Name: {name}")
        print()

        if input_correct():
            break
    
    cur.execute("INSERT INTO Player (name) VALUES (?)", (name,))
    con.commit()
    print(f"Player {name} added successfully!")

def add_board_game():
    while True:
        name = input("Enter board game name: ")

        print("\nYou entered:")
        print(f"Name: {name}")
        print()

        if input_correct():
            break
    
    cur.execute("INSERT INTO Boardgame (name) VALUES (?)", (name,))
    con.commit()
    print(f"Board game {name} added successfully!")

def add_game_session():
    while True: 
        score = input("Enter score: ")

        while True:
            date = input("Enter date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Invalid date format. Please enter date in format YYYY-MM-DD.")

        boardgame_id = input("Enter board game id: ")

        print("\nYou entered:")
        print(f"Score: {score}")
        print(f"Date: {date}")
        print(f"Board game id: {boardgame_id}")
        print()
        
        if input_correct():
            break
    
    cur.execute("INSERT INTO Gamesession (score, date, boardgame_id) VALUES (?, ?, ?)", (score, date, boardgame_id))
    con.commit()
    gamesession_id = cur.lastrowid

    while True:
        print()
        print("Add players to the game session")
        print()
        print("If you want to stop adding players, enter 'q'.")
        print()
        player_id = input("Enter player id: ")

        if player_id == "q":
            break
        
        try:
            cur.execute("INSERT INTO Participate (player_id, gamesession_id) VALUES (?, ?)", (player_id, gamesession_id))
            con.commit()
            print("Player added successfully!")
            print()
        except sqlite3.IntegrityError as e:
            print("Error: this player ID does not exist or its already in this game session.")

    print()
    print("Game session added successfully!")

def show_statistics():
    boardgame_name = input("Enter board game name: ")
    date = input("Enter date (YYYY-MM-DD): ")

    cur.execute("""
    SELECT Gamesession.id, Boardgame.name, Gamesession.date, Player.name, Gamesession.score
    FROM Gamesession
    JOIN Boardgame ON Gamesession.boardgame_id = Boardgame.id
    JOIN Participate ON Gamesession.id = Participate.gamesession_id
    JOIN Player ON Participate.player_id = Player.id
    WHERE Boardgame.name = ? AND Gamesession.date = ?
    """, (boardgame_name, date))
    
    results = cur.fetchall()

    if results:
        print()
        print("Game session statistics:")
        current_session = None
        for row in results:
            session_id, game_name, session_date, player_name, score = row
            if session_id != current_session:
                if current_session is not None:
                    print()
                print(f"Session ID: {session_id}, Game: {game_name}, Date: {session_date}, Score: {score}")
                print("Participated players:")
                current_session = session_id
            print(f"  - {player_name}")
        
    else:
        print()
        print("No statistics.")

def main():
    while True:
        menu = """
Select an option:
1. Add player
2. Add board game
3. Add game session
4. Show statistics
5. Quit
"""

        choice = input(menu)
        if choice == "1":
            add_player()
        elif choice == "2": 
            add_board_game()
        elif choice == "3":
            add_game_session()
        elif choice == "4":
            show_statistics()
        elif choice == "5":
            break

if __name__ == "__main__":
    main()
    con.close()