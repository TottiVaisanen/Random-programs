"""
COMP.CS.100 Ohjelmointi 1
            Programming 1

StudentId: 151364051
Firstname Lastname: Totti Väisänen
Email: totti.vaisanen@tuni.fi
Sink the ship game where the player tries to guess where the computers ships
are located. The player wins when all the ships have been sunk."""

# A list of all the letters in the coordinates.
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


class Board:
    """This class creates the game board where the game is played on."""

    def __init__(self, ship_list):

        # Create a list of all the coordinates where ships are.
        self.__all_coordinates = []

        for ship in ship_list:
            coordinates = ship.get_coordinates()
            for number_coordinates in coordinates:
                self.__all_coordinates.append(",".join(number_coordinates))

        # List of all the coordinates that have already been shot at.
        self.__shot_coordinates = []

        # The amount of ships that there are in the beginning.
        self.__beginning_ships = len(ship_list)

        # The amount of ships that have sunk.
        self.__sunken_ships = 0

        # List of all the ships on the board, with their names/types.
        self.__ships = ship_list

        # List of all the ships that have not been sunk.
        self.__still_afloat = ship_list

        # A dict with ship's types first letter as the key and a list of
        # all the type's ships that been sunk.

        self.__sunk = {"B": [], "C": [], "D": [], "S": []}

    def ships_afloat(self):
        """A method that returns how many ships are still afloat."""
        remaining = self.__beginning_ships - self.__sunken_ships
        return remaining

    def is_it_afloat(self):
        """Checks if the player has sunk a ship."""

        for ship in self.__still_afloat:

            # A counter to represent the coordinates that have been hit.
            counter = 0

            # If the coordinates have been shot at the counter goes up by one,
            # but if one or more of the ships coordinates have not been fired
            # at, it means the ship is still afloat.

            for coordinates in ship.get_coordinates():
                if coordinates in "".join(self.__shot_coordinates):
                    counter += 1
                    pass
                else:
                    break

                # If the ship has sunk, some changes need to be made.
                if counter == len(ship.get_coordinates()):
                    self.update_sunken(ship)
                    self.__sunken_ships += 1
                    # Print a message to inform which type of ship
                    # has been sunk.
                    print(f"You sank a {ship.get_ship_type()}!")
                    # Remove the ship from the list of ships afloat.
                    self.__still_afloat.remove(ship)

    def print_board(self):
        """Prints the game board, with all the coordinates that have been
        fired.

        If the shot has missed all the ships = *
        If the shot has hit a ship but the ship is still afloat = X
        If the ship has sunk = first letter of the ships type in upper."""

        # First let's create the game board which is a list. Every list is
        # one line and one list has its own list inside.
        board = []
        # The first and last rows are special so they need to be printed out
        # separately.
        first_row = [" ", " ", "A", " ", "B", " ", "C", " ", "D", " ",
                     "E", " ", "F", " ", "G", " ", "H", " ", "I", " ",
                     "J"]
        # A counter to represent the row currently on.
        counter1 = -1
        while counter1 <= 10:
            row = []

            # In case if it's the first or the last line.
            if counter1 == -1 or counter1 == 10:
                board.append(first_row)
                counter1 += 1
            else:
                # A counter to represent the distance from the left edge.
                counter2 = 1
                while counter2 <= 23:
                    if counter2 == 1 or counter2 == 23:
                        row.append(str(counter1))
                        counter2 += 1
                    else:
                        row.append(" ")
                        counter2 += 1
                board.append(row)
                counter1 += 1

        # Now an empty board has been generated.

        # Then we need to take into consideration if shots have been fired and
        # if the shots have hit any of the ships.
        for coordinate in self.__shot_coordinates:
            separated = coordinate.split(",")
            # A counter to represent the x-coordinate.
            counter = -1
            # The row that has been fired at
            row = int(int(separated[1])+1)
            for place in board[row]:
                counter += 1
                if counter == int(separated[0]):
                    # If the shot has hit a ship it prints out an X.
                    if ",".join(coordinate) in self.__all_coordinates:
                        board[int(separated[1]) + 1][
                        int(separated[0])] = "X"
                    # If the shot has missed it prints out a *.
                    else:
                        board[int(separated[1]) + 1][
                            int(separated[0])] = "*"
                else:
                    pass

        # Then change the X:s into the first letters of the ships type,
        # if the ship has sunk.

        for letter in self.__sunk:
            # If there aren't any sunken ships of this type:
            if len(self.__sunk[letter]) == 0:
                pass
            else:
                for coordinates in self.__sunk[letter]:
                    separated = coordinates.split(",")
                    counter = -1
                    row = int(int(separated[1]) + 1)
                    for place in board[row]:
                        counter += 1
                        # Change the X into the first letter of the ship's
                        # type.
                        if counter == int(separated[0]):
                            board[int(separated[1]) + 1][
                                int(separated[0])] = f"{letter}"

        # And at last the board is ready to be printed out.
        for row in board:
            print("".join(row))

    def get_fired_coordinates(self):
        """Returns a list of coordinates that have been fired at."""
        return self.__shot_coordinates

    def update_fired(self, command):
        """Adds the fired coordinates to the <shot_coordinates> list."""
        self.__shot_coordinates.append(",".join(into_numbers(command)))

    def update_sunken(self, ship):
        """Updates the coordinates of the sunken ship's."""
        letter = ship.get_first_letter()
        for coordinates in ship.get_coordinates():
            self.__sunk[letter].append(coordinates)


class Ship:
    """This class defines where a ship is located"""
    def __init__(self, information):
        """Constructor that saves a name of a single ship and adds the ship
         into the dict with a list of the ships coordinates as its key"""
        self.__coordinates = information[1:]
        self.__ship_type = information[0]

    def get_coordinates(self):
        """Returns the coordinates of the ship that have been transformed into
        numbers."""

        number_coordinates = []
        for xy in self.__coordinates:
            number_coordinates.append(",".join(into_numbers(xy)))

        return number_coordinates

    def get_first_letter(self):
        """Return the first letter of the ships type in upper case."""
        string = list(self.__ship_type)
        return string[0].upper()

    def get_ship_type(self):
        """Returns the type of the ship."""
        return self.__ship_type


def into_numbers(coordinates):
    """Changes the x-coordinate into a number which represents the
        distance from the left edge of the page and returns the coordinates."""

    # A dict which has the information of how many characters from the left
    # edge of the screen each letter is.
    letters_spots = {"A": "2", "B": "4", "C": "6", "D": "8", "E": "10",
                     "F": "12", "G": "14", "H": "16", "I": "18", "J": "20"}
    # A list of the coordinates in numbers.
    number_coordinates = []
    # A list where the x and y are separated.
    separated_xy = []

    separated = list(coordinates)
    letter = separated[0].upper()
    separated_xy.append(letters_spots[letter])
    separated_xy.append(separated[1])

    number_coordinates.append(",".join(separated_xy))
    return number_coordinates


def read_file(file_name, ship_list):
    """Reads a file that contains information about a ship's type and its
    coordinates and saves it."""
    try:
        file = open(file_name, mode="r")

        coordinate_list = []

        # Save the information from the file to create ships.
        for row in file:
            stripped = row.rstrip()
            # First separate the coordinates and the ship name.
            information = stripped.split(";")
            # Check if the coordinates are correct. Coordinates start from
            # the second item on the list onwards.
            for coordinates in information[1:]:
                # First check if the coordinates overlap.
                if coordinates in coordinate_list:
                    print("There are overlapping ships in the input file!")
                    return False
                else:
                    coordinate_list.append(coordinates)
                # Check if the coordinates fit on the game board.
                letter_number = list(coordinates)
                if letter_number[0] not in LETTERS:
                    print("Error in ship coordinates!")
                    return False
                if int(letter_number[1]) not in range(0, 10):
                    print("Error in ship coordinates!")
                    return False
                if len(letter_number) != 2:
                    print("Error in ship coordinates!")
                    return False
            ship = Ship(information)
            ship_list.append(ship)
        return ship_list

    # An error message if the file can't be read.
    except OSError:
        print("File can not be read!")
        return False


def check_command_form(command):
    """Checks if the command is given in correct form."""

    separated = list(command)

    # If there are more than 2 characters, the command is wrong.
    if len(separated) != 2:
        return False
    # If the x-coordinate isn't in the LETTERS list.
    elif separated[0].upper() not in LETTERS:
        return False
    # If the y-coordinate isn't in the correct range.
    elif int(separated[1]) not in range(0, 10):
        return False
    else:
        return True


def check_command(command, game_board):
    """Checks if the command is valid and if the player wants to quit."""

    # Check if the fire command is in correct form.
    if check_command_form(command) == False:
        print("Invalid command!")
        return False

    # Check if the coordinates have already been fired at.
    elif ",".join(into_numbers(command)) in game_board.get_fired_coordinates():
        print("Location has already been shot at!")
        return False

    else:
        return True


def shoot(command, game_board):
    """Makes the changes that shooting at specific coordinates does."""

    # Update the fired coordinates to the game boards <shot_coordinates>
    game_board.update_fired(command)

    # Then if the shot has hit a target, the target's condition needs to be
    # checked.
    game_board.is_it_afloat()


def main():

    # A list of all the ships
    ship_list = []

    # The name of the file where is the ship's type and its coordinates
    # separated by ";".
    file_name = input("Enter file name: ")

    # If the file is successfully read.
    if read_file(file_name, ship_list):

        # Create the game board.
        game_board = Board(ship_list)

        print()

        # Print the game board
        game_board.print_board()

        print()

        # A loop which only ends if the player wins or decides to quit.
        # While there are ships afloat the game is on.
        while game_board.ships_afloat() > 0:
            # Firing coordinates from the player.
            command = input("Enter place to shoot (q to quit): ")

            # If the player wants to quit.
            if command == "q" or command == "Q":
                print("Aborting game!")
                break
            # Check if the command is given in correct form.
            elif check_command(command, game_board) == False:
                pass
            # Make the changes to the game board.
            else:
                shoot(command, game_board)
            print()
            game_board.print_board()
            print()

        # Check if the player has won.
        if game_board.ships_afloat() == 0:
            print("Congratulations! You sank all enemy ships.")


if __name__ == "__main__":
    main()
