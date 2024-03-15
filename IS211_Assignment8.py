import time
import random
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def turn(self):
        pass

class HumanPlayer(Player):
    def turn(self):
        while True:
            choice = input("Roll or Hold? (r/h): ").lower()
            if choice == 'r':
                roll = random.randint(1, 6)
                print(f"{self.name} rolled a {roll}")
                if roll == 1:
                    print("You rolled a 1. No points gained this turn.")
                    return 0
                self.score += roll
            elif choice == 'h':
                print(f"{self.name} holds. Total score for this turn: {self.score}")
                return self.score
            else:
                print("Invalid choice. Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def turn(self):
        target_score = min(25, 100 - self.score)
        turn_score = 0
        while turn_score < target_score:
            roll = random.randint(1, 6)
            print(f"{self.name} rolled a {roll}")
            if roll == 1:
                print("Computer rolled a 1. No points gained this turn.")
                return 0
            turn_score += roll
        self.score += turn_score
        print(f"{self.name} holds. Total score for this turn: {turn_score}")
        return turn_score

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_turn(self, player):
        if time.time() - self.start_time > 60:
            print("Time's up! Game over.")
            return True
        return self.game.play_turn(player)

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        self.current_score = 0

    def play_turn(self, player):
        score = player.turn()
        if score == 0:
            self.current_score = 0
            self.current_player = (self.current_player + 1) % 2
            return False
        self.current_score += score
        if self.players[self.current_player].score + self.current_score >= 100:
            print(f"{self.players[self.current_player].name} wins with {self.players[self.current_player].score + self.current_score} points!")
            return True
        return False

def main():
    parser = argparse.ArgumentParser(description="Play Pig game.")
    parser.add_argument('--player1', choices=['human', 'computer'], default='human', help="Type of player 1")
    parser.add_argument('--player2', choices=['human', 'computer'], default='computer', help="Type of player 2")
    parser.add_argument('--timed', action='store_true', help="Enable timed game")
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    if args.timed:
        game = TimedGameProxy(Game(player1, player2))
    else:
        game = Game(player1, player2)

    while not game.play_turn(game.players[game.current_player]):
        pass

if __name__ == "__main__":
    main()

