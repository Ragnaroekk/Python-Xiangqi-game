# Author: Ray Franklin
# Date: 02/27/2020
# Description: A Xiangqi game in python
# It uses the pieces listed as Wikipedia describes their names.
# General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
# https://en.wikipedia.org/wiki/Xiangqi
#
# A Xiangqi board game with simple visual representation
# Movement is alphanumeric, "a2", "a7" for example. The make_move method is passed the starting and ending locations.
# The board can be displayed by calling display_game_board.
# Rules follow movement based on wikipeida.


class XiangqiGame:
    """Represents a xiangqi game with a board and game pieces."""

    def __init__(self):
        """Initializes a new Xiangqi game"""
        self._game_state = "UNFINISHED"
        self._game_board = XiangqiBoard()
        self._turn_order = 0

    def get_game_board(self):
        """A method to return the current game's board"""
        return self._game_board

    def get_game_state(self):
        """Returns the current game's state"""
        return self._game_state

    def set_game_state(self, status):
        """A method to change the game state"""
        self._game_state = status

    def is_in_check(self, color):
        """
        A method to determine if a general is in check based on the color, "Red" or "Black"
        :returns True if in check, False otherwise
        """
        # find and point to the generals by color
        for row in range(10):
            for col in range(9):
                if type(self.get_game_board().get_game_piece_by_location(row, col)) == General:
                    if self.get_game_board().get_game_piece_color_by_location(row, col) == "Red":
                        red_general = self.get_game_board().get_game_piece_by_location(row, col)
                        if color == "Red":
                            return red_general.get_check_status()
                    if self.get_game_board().get_game_piece_color_by_location(row, col) == "Black":
                        black_general = self.get_game_board().get_game_piece_by_location(row, col)
                        if color == "Black":
                            return black_general.get_check_status()

    def update_check(self):
        """A method to update the check status for each general"""
        # populate the two lists of moves by color
        red_move_list = self.get_game_board().get_all_legal_moves_by_color("Red")
        black_move_list = self.get_game_board().get_all_legal_moves_by_color("Black")

        # grab the two generals and assign them names for referencing
        for row in range(10):
            for col in range(9):
                if self.get_game_board().get_game_piece_by_location(row, col):
                    if type(self.get_game_board().get_game_piece_by_location(row, col)) == General:
                        if self.get_game_board().get_game_piece_by_location(row, col).get_game_piece_color() == "Red":
                            red_general = self.get_game_board().get_game_piece_by_location(row, col)
                            red_general_location = red_general.convert_coordinates_to_string(row, col)
                        else:
                            black_general = self.get_game_board().get_game_piece_by_location(row, col)
                            black_general_location = black_general.convert_coordinates_to_string(row, col)

        # check if the generals current location is in the list of enemy moves, update to true if found
        if red_general_location in black_move_list:
            red_general.update_check_status(True)
        else:
            red_general.update_check_status(False)
        if black_general_location in red_move_list:
            black_general.update_check_status(True)
        else:
            black_general.update_check_status(False)

    def update_game_status(self):
        """A method to change and update who won"""
        # find and reference the generals
        for row in range(10):
            for col in range(9):
                if self.get_game_board().get_game_piece_by_location(row, col):
                    if type(self.get_game_board().get_game_piece_by_location(row, col)) == General:
                        if self.get_game_board().get_game_piece_by_location(row, col).get_game_piece_color() == "Red":
                            red_general = self.get_game_board().get_game_piece_by_location(row, col)
                        else:
                            black_general = self.get_game_board().get_game_piece_by_location(row, col)

        # see which general is in check
        if self.is_in_check("Red"):
            if red_general.get_legal_moves() == [] and not self.is_in_check("Black"):
                self.set_game_state("BLACK_WON")
        if self.is_in_check("Black"):
            if black_general.get_legal_moves() == [] and not self.is_in_check("Red"):
                self.set_game_state("RED_WON")

    def get_turn_order_color(self):
        """A method to return which color's turn it is"""
        if self._turn_order % 2 == 0:
            return "Red"
        else:
            return "Black"

    def get_turn_order_count(self):
        """A method to return the number of turns the current game has taken"""
        return self._turn_order

    def update_turn_order(self):
        """A method to increment the turn order"""
        self._turn_order += 1

    def convert_string_to_coordinates(self, start, end):
        """
        A method to convert the alpha numeric string characters to integers.
        :returns list of integer indexes in order of row_start, row_end, col_start, col_end"""
        try:
            # set up start and end as list so we can pop the first element
            start_list = list(start)
            end_list = list(end)

            # create dictionary to cross reference the string moves to indexes
            move_dict_row = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5, "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
            move_dict_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}

            # pop the first elements and store them as column index
            col_start = move_dict_col[start_list.pop(0)]
            col_end = move_dict_col[end_list.pop(0)]

            # Convert the remaining elements back to strings and store the row index
            start_string = "".join([str(elem) for elem in start_list])
            end_string = "".join([str(elem) for elem in end_list])
            row_start = move_dict_row[start_string]
            row_end = move_dict_row[end_string]

            converted_list = [row_start, row_end, col_start, col_end]

            return converted_list

        # print error message if location not found in dictionary
        except KeyError:
            return False

    def get_potential_move_status(self, row_start, row_end, col_start, col_end):
        """
        A method to check moves before they execute to prevent revealed checks or illegal moves.
        Mirrors make_move method and removes moves that would not be allowed due to check.
        """
        # store the piece we want to moves information
        piece_to_move = self.get_game_board().get_game_piece_by_location(row_start, col_start)
        color_to_move = piece_to_move.get_game_piece_color()

        # undo move list
        undo_move_list = []

        # if we start in check
        if self.is_in_check(color_to_move):
            for row in range(10):
                for col in range(9):
                    # only check the moving side's pieces
                    if self.get_game_board().get_game_piece_color_by_location(row, col) == color_to_move:

                        # move the piece
                        for move in self.get_game_board().get_game_piece_by_location(row, col).get_legal_moves():
                            # convert the location to coordinates
                            current_piece = self.get_game_board().get_game_piece_by_location(row, col)
                            starting_row = current_piece.get_game_piece_location_row()
                            starting_col = current_piece.get_game_piece_location_col()
                            start_string = current_piece.convert_coordinates_to_string(starting_row, starting_col)

                            # convert and store the location info
                            converted_list = self.convert_string_to_coordinates(start_string, move)
                            row_start = converted_list[0]
                            row_end = converted_list[1]
                            col_start = converted_list[2]
                            col_end = converted_list[3]

                            # store the current pieces
                            undo_move_list.append(current_piece)
                            undo_move_list.append(self.get_game_board().get_board()[row_end][col_end])

                            # make the move
                            self.get_game_board().get_board()[row_start][col_start] = "..."
                            self.get_game_board().get_board()[row_end][col_end] = current_piece

                            # did it resolve check?
                            if self.is_in_check(color_to_move):
                                # if not, remove from list
                                try:
                                    current_piece.get_legal_moves().remove(move)
                                except ValueError:
                                    pass

                            # if so, move is ok and restore the original pieces and try again for each piece
                            self.get_game_board().get_board()[row_start][col_start] = undo_move_list[0]
                            self.get_game_board().get_board()[row_end][col_end] = undo_move_list[1]

        # get all the moves for the moving side that remain
        available_moves = self.get_game_board().get_all_legal_moves_by_color(color_to_move)

        # if no moves are available, the other side wins, covers checkmate and stalemates
        if not available_moves:
            if color_to_move == "Red":
                self.set_game_state("BLACK_WON")
            elif color_to_move == "Black":
                self.set_game_state("RED_WON")
            return False
        return True

    def make_move(self, start, end):
        """takes two parameters - strings that represent the square moved from and the square moved to.
        For example, make_move('b3', 'b10'). If the square being moved from does not contain a piece
        belonging to the player whose turn it is, or if the indicated move is not legal, or if the game
        has already been won, then it should just return False. Otherwise it should make the indicated move,
        remove any captured piece, update the game state if necessary, update whose turn it is, and return True."""
        # start and end locations need to be different
        if start == end:
            return False

        # convert and store the index values
        converted_list = self.convert_string_to_coordinates(start, end)
        row_start = converted_list[0]
        row_end = converted_list[1]
        col_start = converted_list[2]
        col_end = converted_list[3]

        # store the piece we want to moves information
        piece_to_move = self.get_game_board().get_game_piece_by_location(row_start, col_start)
        color_to_move = piece_to_move.get_game_piece_color()
        color_to_receive = self.get_game_board().get_game_piece_color_by_location(row_end, col_end)

        # make sure you are moving your own piece, to a legal location
        if piece_to_move.get_game_piece_color() != self.get_turn_order_color():
            return False
        elif color_to_move == color_to_receive:  # can't land on your own piece
            return False
        elif row_end not in piece_to_move.get_legal_moveset_row():  # can't move past river if elephant etc.
            return False
        elif col_end not in piece_to_move.get_legal_moveset_col():  # can't move past river if elephant etc.
            return False
        elif end not in piece_to_move.get_legal_moves():  # check the legal moves available
            return False
        # elif not self.get_potential_move_status(row_start, row_end, col_start, col_end):  # prevent revealed check etc.
        #     return False
        else:
            # move the piece, update its location, and update the turn order
            self.get_game_board().get_board()[row_end][col_end] = piece_to_move
            self.get_game_board().get_board()[row_start][col_start] = "..."
            self.update_game_board()
            self.get_game_board().remove_game_piece_legal_move()
            self.update_check()
            self.update_game_status()
            self.update_turn_order()
            return True

    def update_game_board(self):
        """A method to update all the items on the board"""
        for row in range(10):
            for col in range(9):
                if self.get_game_board().get_board()[row][col] != "...":
                    self.get_game_board().get_board()[row][col].update_game_piece_location(row, col)

        # update the flying General rules
        for row in range(10):
            for col in range(9):
                if type(self.get_game_board().get_game_piece_by_location(row, col)) == General:
                    self.get_game_board().fly_the_general(row, col)

    def display_game_board(self):
        """A method to display the game board"""

        # make a copy of the old list so we don't affect the current data
        display_list = [x[:] for x in self.get_game_board().get_board().copy()]

        # Change pieces to names that are human readable
        for x in range(len(self.get_game_board().get_board())):
            for y in range(len(self.get_game_board().get_board()[x])):
                if self.get_game_board().get_board()[x][y] != "...":
                    display_list[x][y] = self.get_game_board().get_board()[x][y].get_game_piece_name()

        # print each row in order
        for row in display_list:
            print(row)


class XiangqiBoard:
    """Represents a Xiangqi board"""

    def __init__(self):
        """
        Initializes the game board with game pieces at starting locations,
        and updates those pieces' location data
        """
        # set up the game board with pieces in default locations
        self._game_board = [["..."] * 9 for _ in range(10)]
        self._game_board[0][4] = General(None, "Black")
        self._game_board[0][3] = Advisor(None, "Black")
        self._game_board[0][5] = Advisor(None, "Black")
        self._game_board[0][6] = Elephant(None, "Black")
        self._game_board[0][2] = Elephant(None, "Black")
        self._game_board[0][7] = Horse(None, "Black")
        self._game_board[0][1] = Horse(None, "Black")
        self._game_board[0][8] = Chariot(None, "Black")
        self._game_board[0][0] = Chariot(None, "Black")
        self._game_board[2][1] = Cannon(None, "Black")
        self._game_board[2][7] = Cannon(None, "Black")
        self._game_board[3][0] = Soldier(None, "Black")
        self._game_board[3][2] = Soldier(None, "Black")
        self._game_board[3][4] = Soldier(None, "Black")
        self._game_board[3][6] = Soldier(None, "Black")
        self._game_board[3][8] = Soldier(None, "Black")
        self._game_board[9][4] = General(None, "Red")
        self._game_board[9][3] = Advisor(None, "Red")
        self._game_board[9][5] = Advisor(None, "Red")
        self._game_board[9][6] = Elephant(None, "Red")
        self._game_board[9][2] = Elephant(None, "Red")
        self._game_board[9][7] = Horse(None, "Red")
        self._game_board[9][1] = Horse(None, "Red")
        self._game_board[9][8] = Chariot(None, "Red")
        self._game_board[9][0] = Chariot(None, "Red")
        self._game_board[7][1] = Cannon(None, "Red")
        self._game_board[7][7] = Cannon(None, "Red")
        self._game_board[6][0] = Soldier(None, "Red")
        self._game_board[6][2] = Soldier(None, "Red")
        self._game_board[6][4] = Soldier(None, "Red")
        self._game_board[6][6] = Soldier(None, "Red")
        self._game_board[6][8] = Soldier(None, "Red")

        # store the game piece's location in the pieces themselves
        for row in range(10):
            for col in range(9):
                if self.get_board()[row][col] != "...":
                    self.get_board()[row][col].update_game_piece_location(row, col)

    def get_board(self):
        """A method to return the current game board"""
        return self._game_board

    def is_on_board(self, row, col):
        """A method to check if a location exists on the game board"""
        if row in range(len(self.get_board())):
            if col in range(len(self.get_board()[row])):
                return True
            else:
                return False
        return False

    def get_game_piece_name_by_location(self, row, col):
        """
        A search method to find a piece's location and return its name or returns False.
        Takes two parameters, row and column.
        """
        if self.is_on_board(row, col):
            if self.get_board()[row][col] != "...":
                return self.get_board()[row][col].get_game_piece_name()
            else:
                return False
        return False

    def get_game_piece_color_by_location(self, row, col):
        """
        A search method to find a piece's location and return its name or returns False.
        Takes two parameters, row and column.
        """
        if self.is_on_board(row, col):
            if self.get_board()[row][col] != "...":
                return self.get_board()[row][col].get_game_piece_color()
            else:
                return False
        return False

    def get_game_piece_by_location(self, row, col):
        """A method to find and return a game piece by board location or returns none"""
        if self.is_on_board(row, col):
            if self.get_board()[row][col] != "...":
                return self.get_board()[row][col]
            else:
                return False
        else:
            return False

    def get_game_piece_legal_move_row_by_location(self, row, col):
        """A method to return a game piece's legal moves by row"""
        if self.is_on_board(row, col):
            if self.get_board()[row][col] != "...":
                return self.get_board()[row][col].get_legal_moveset_row()
            else:
                return False
        else:
            return False

    def get_game_piece_legal_move_col_by_location(self, row, col):
        """A method to return a game piece's legal moves by row"""
        if self.is_on_board(row, col):
            if self.get_board()[row][col] != "...":
                return self.get_board()[row][col].get_legal_moveset_col()
            else:
                return False
        else:
            return False

    def remove_game_piece_legal_move(self):
        """
        A method to pop illegal moves from the list of current moves based on situational changes.
        That is, elephant is blocked, horse is blocked, etc.
        """
        # check each piece on the board to update them all after each move
        for row in range(10):
            for col in range(9):
                if self.get_board()[row][col] != "...":
                    current_piece = self.get_game_piece_by_location(row, col)

                    # remove friendly fire
                    self.remove_friendly_fire()

                    #  prevent from moving into check
                    if type(current_piece) == General:
                        self.prevent_self_check()

                    # update the blinded elephant rule
                    elif type(current_piece) == Elephant:
                        self.blind_the_elephant(row, col)

                    # update the hobble the horse rule
                    elif type(current_piece) == Horse:
                        self.hobble_the_horse(row, col)

                    # take out illegal moves and add the opposing pieces to the movement list
                    elif type(current_piece) == Chariot:
                        self.block_the_chariot_and_cannon(row, col)
                        self.chariot_hit_detection(row, col)

                    # take out illegal moves and add the opposing pieces to the movement list
                    elif type(current_piece) == Cannon:
                        self.block_the_chariot_and_cannon(row, col)
                        self.cannon_hit_detection(row, col)

                    else:
                        pass

    def remove_friendly_fire(self):
        """A method to remove any same color locations in a piece's move list"""
        # lists to hold the current piece locations
        red_list = []
        black_list = []

        # populate the lists
        for row in range(10):
            for col in range(9):
                if self.get_game_piece_color_by_location(row, col) == "Red":
                    red_list.append(self.get_game_piece_by_location(row, col).convert_coordinates_to_string(row, col))
                elif self.get_game_piece_color_by_location(row, col) == "Black":
                    black_list.append(self.get_game_piece_by_location(row, col).convert_coordinates_to_string(row, col))

        # check each piece and remove the same piece moves
        for row in range(10):
            for col in range(9):

                # red pieces
                if self.get_game_piece_color_by_location(row, col) == "Red":
                    for elem in self.get_game_piece_by_location(row, col).get_legal_moves():
                        if elem in red_list:
                            self.get_game_piece_by_location(row, col).get_legal_moves().remove(elem)
                # black pieces
                elif self.get_game_piece_color_by_location(row, col) == "Black":
                    for elem in self.get_game_piece_by_location(row, col).get_legal_moves():
                        if elem in black_list:
                            self.get_game_piece_by_location(row, col).get_legal_moves().remove(elem)

    def prevent_self_check(self):
        """A method to remove the self checking moves from the general's list of movement."""
        # list for holding available moves
        red_general_flight = []
        black_general_flight = []

        # set up the generals and locations for reference
        for row in range(0, 10):
            for col in range(0, 9):
                if type(self.get_game_piece_by_location(row, col)) == General:
                    current_piece = self.get_game_piece_by_location(row, col)
                    if current_piece.get_game_piece_color() == "Red":
                        red_general = self.get_game_piece_by_location(row, col)
                        red_general_flight = current_piece.get_flying_moves()
                    else:
                        black_general = self.get_game_piece_by_location(row, col)
                        black_general_flight = current_piece.get_flying_moves()

        # check for red general
        if red_general.get_game_piece_color() == "Red":
            for elem in current_piece.get_legal_moves():
                if elem in self.get_all_legal_moves_by_color("Black"):
                    try:
                        red_general.get_legal_moves().remove(elem)
                    except ValueError:
                        pass
                if elem in black_general_flight:
                    try:
                        red_general.get_legal_moves().remove(elem)
                    except ValueError:
                        pass
        # black general
        if black_general.get_game_piece_color() == "Black":
            for elem in black_general.get_legal_moves():
                if elem in self.get_all_legal_moves_by_color("Red"):
                    try:
                        black_general.get_legal_moves().remove(elem)
                    except ValueError:
                        pass
                if elem in red_general_flight:
                    try:
                        black_general.get_legal_moves().remove(elem)
                    except ValueError:
                        pass

    def get_all_legal_moves_by_color(self, color):
        """A method to get all available moves by each piece based upon color
        :returns a master list depending on which color is passed into the method"""
        # lists for holding the moves
        red_move_list = []
        black_move_list = []

        # populate the lists
        for row in range(10):
            for col in range(9):
                if self.get_game_piece_by_location(row, col):
                    if self.get_game_piece_color_by_location(row, col) == "Red":
                        for elem in self.get_game_piece_by_location(row, col).get_legal_moves():
                            red_move_list.append(elem)
                    else:
                        for elem in self.get_game_piece_by_location(row, col).get_legal_moves():
                            black_move_list.append(elem)

        # return the lists based on colors
        if color == "Red":
            return red_move_list
        else:
            return black_move_list

    def fly_the_general(self, row, col):
        """A method to add flying moves for the Generals"""
        # check each piece on the board to update them all after each move
        current_piece = self.get_game_piece_by_location(row, col)
        current_piece.get_flying_moves().clear()

        # check for the red general flying moves
        if current_piece.get_game_piece_color() == "Red":
            for num in range((row - 1), -1, -1):  # check for empty spaces from the general's location
                if self.get_board()[num][col] != "..." and num > 2:  # if row is blocked
                    break
                elif num in range(0, 3):  # go until the next palace
                    if self.get_game_piece_by_location(num, col):
                        if self.get_game_piece_color_by_location(num, col) == current_piece.get_game_piece_color():
                            try:
                                current_piece.get_flying_moves().append(
                                    current_piece.convert_coordinates_to_string(num, col))
                            except ValueError:
                                break
                        else:
                            break
                    elif self.get_board()[num][col] == "...":
                        try:
                            current_piece.get_flying_moves().append(
                                current_piece.convert_coordinates_to_string(num, col))
                        except ValueError:
                            pass
                else:
                    pass

        # check for the black general flying moves
        else:
            for num in range((row + 1), 10, 1):
                if self.get_board()[num][col] != "..." and num < 7:  # if row is blocked
                    break
                elif num in range(7, 10):  # go until the next palace
                    if self.get_game_piece_by_location(num, col):
                        if self.get_game_piece_color_by_location(row, col) == current_piece.get_game_piece_color():
                            try:
                                current_piece.get_flying_moves().append(
                                 current_piece.convert_coordinates_to_string(num, col))
                            except ValueError:
                                break
                        else:
                            break
                    elif self.get_board()[num][col] == "...":
                        try:
                            current_piece.get_flying_moves().append(
                                current_piece.convert_coordinates_to_string(num, col))
                        except ValueError:
                            pass
                else:
                    pass

    def hobble_the_horse(self, row, col):
        """A method to determine if the horse's movement is blocked, and to update the list of moves if so"""
        # check each piece on the board to update them all after each move
        current_piece = self.get_game_piece_by_location(row, col)

        # check above location
        blocking_piece = self.get_game_piece_by_location(row - 1, col)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 2, col - 1))
            except ValueError:
                pass
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 2, col + 1))
            except ValueError:
                pass

        # check right location
        blocking_piece = self.get_game_piece_by_location(row, col + 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 1, col + 2))
            except ValueError:
                pass
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 1, col + 2))
            except ValueError:
                pass

        # check lower location
        blocking_piece = self.get_game_piece_by_location(row - 1, col)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 2, col + 1))
            except ValueError:
                pass
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 2, col - 1))
            except ValueError:
                pass

        # check left location
        blocking_piece = self.get_game_piece_by_location(row, col - 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 1, col - 2))
            except ValueError:
                pass
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 1, col - 2))
            except ValueError:
                pass

    def blind_the_elephant(self, row, col):
        """A method to determine if the elephant's movement is blocked, and to update the list of moves if so"""
        # check each piece on the board to update them all after each move
        current_piece = self.get_game_piece_by_location(row, col)

        # check for "eye blocking" of the elephant, upper right direction
        blocking_piece = self.get_game_piece_by_location(row - 1, col + 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 2, col + 2))
            except ValueError:
                pass

        # check lower right direction
        blocking_piece = self.get_game_piece_by_location(row + 1, col + 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 2, col + 2))
            except ValueError:
                pass

        # check lower left location
        blocking_piece = self.get_game_piece_by_location(row + 1, col - 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row + 2, col - 2))
            except ValueError:
                pass

        # check upper left location
        blocking_piece = self.get_game_piece_by_location(row - 1, col - 1)
        if blocking_piece:
            try:
                current_piece.get_legal_moves().remove(
                    current_piece.convert_coordinates_to_string(row - 2, col - 2))
            except ValueError:
                pass

    def block_the_chariot_and_cannon(self, row, col):
        """A method to remove the illegal moves from the chariot's and cannon's list of moves"""
        # assign the chariot to current the piece
        current_piece = self.get_game_piece_by_location(row, col)

        # check left and right to remove illegal moves in the list
        for col_num in range(9):
            if col_num < col:
                if self.get_game_piece_by_location(row, col_num):

                    # remove the left side blocked options
                    for blocked_col in range((col_num + 1)):
                        try:
                            current_piece.get_legal_moves().remove(
                                current_piece.convert_coordinates_to_string(row, blocked_col))
                        except ValueError:
                            pass
            elif col_num > col:
                if self.get_game_piece_by_location(row, col_num):

                    # remove the right side blocked options
                    for blocked_col in range(9, (col_num - 1), -1):
                        try:
                            current_piece.get_legal_moves().remove(
                                current_piece.convert_coordinates_to_string(row, blocked_col))
                        except ValueError:
                            pass

        # check up and down to remove illegal moves in the list
        for row_num in range(10):
            if row_num < row:
                if self.get_game_piece_by_location(row_num, col):

                    # remove lower blocked options
                    for blocked_row in range(0, (row_num + 1)):
                        try:
                            current_piece.get_legal_moves().remove(
                                current_piece.convert_coordinates_to_string(blocked_row, col))
                        except ValueError:
                            pass
            elif row_num > row:
                if self.get_game_piece_by_location(row_num, col):

                    # remove upper blocked options
                    for blocked_row in range(row_num, 10):
                        try:
                            current_piece.get_legal_moves().remove(
                                current_piece.convert_coordinates_to_string(blocked_row, col))
                        except ValueError:
                            pass

    def chariot_hit_detection(self, row, col):
        """A method to add functionality so the chariot can land on opposing pieces"""
        # assign the chariot to the current piece
        current_piece = self.get_game_piece_by_location(row, col)

        # check left direction
        for num in range((col - 1), -1, -1):
            if self.get_game_piece_by_location(row, num):  # if we find another piece
                if self.get_game_piece_by_location(row,
                                                   num).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(row, num))
                        break
                    except ValueError:
                        break
                else:
                    break

        # check right direction
        for num in range((col + 1), 9):
            if self.get_game_piece_by_location(row, num):  # if we find another piece
                if self.get_game_piece_by_location(row,
                                                   num).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(row, num))
                        break
                    except ValueError:
                        break
                else:
                    break

        # check upper direction
        for num in range((row - 1), -1, -1):
            if self.get_game_piece_by_location(num, col):
                if self.get_game_piece_by_location(num, col).get_game_piece_color() != \
                        current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(num, col))
                        break
                    except ValueError:
                        break
                else:
                    break

        # check lower direction
        for num in range((row + 1), 10):
            if self.get_game_piece_by_location(num, col):
                if self.get_game_piece_by_location(num,
                                                   col).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(num, col))
                        break
                    except ValueError:
                        break
                else:
                    break

    def cannon_hit_detection(self, row, col):
        """A method to add functionality so the cannon can land on opposing pieces"""
        # assign the cannon to the current the piece
        current_piece = self.get_game_piece_by_location(row, col)
        can_attack = False

        # check left direction, start at the piece and work your way to the edge
        for num in range((col - 1), -1, -1):
            if can_attack:
                if not self.get_game_piece_by_location(row, num):
                    if current_piece.convert_coordinates_to_string(row, num) not in current_piece.get_legal_moves():
                        try:
                            current_piece.get_legal_moves().append(
                                current_piece.convert_coordinates_to_string(row, num))
                        except ValueError:
                            pass
                elif self.get_game_piece_by_location(
                        row, num).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(row, num))
                        break
                    except ValueError:
                        break
                else:
                    break

            # add the functionality to attack if we found a first piece
            if self.get_game_piece_by_location(row, num):
                can_attack = True

        # check right direction
        can_attack = False
        for num in range((col + 1), 9):
            if can_attack:

                # add empty places to allow for attacking those locations
                if not self.get_game_piece_by_location(row, num):
                    if current_piece.convert_coordinates_to_string(row, num) not in current_piece.get_legal_moves():
                        try:
                            current_piece.get_legal_moves().append(
                                current_piece.convert_coordinates_to_string(row, num))
                        except ValueError:
                            pass

                # add enemy locations
                elif self.get_game_piece_by_location(
                        row, num).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(row, num))
                        break
                    except ValueError:
                        break

            # add the functionality to attack if we found a first piece
            if self.get_game_piece_by_location(row, num):
                can_attack = True

        # check upper direction
        can_attack = False
        for num in range((row - 1), -1, -1):
            if can_attack:

                # add empty places to allow for attacking those locations
                if self.get_board()[num][col] == "...":
                    if current_piece.convert_coordinates_to_string(num, col) not in current_piece.get_legal_moves():
                        try:
                            current_piece.get_legal_moves().append(
                                current_piece.convert_coordinates_to_string(num, col))
                        except ValueError:
                            pass

                # add enemy locations
                elif self.get_game_piece_by_location(
                        num, col).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(num, col))
                        break
                    except ValueError:
                        break

            # add the functionality to attack if we found a first piece
            if self.get_game_piece_by_location(num, col):
                can_attack = True

        # check lower direction
        can_attack = False
        for num in range((row + 1), 10):
            if can_attack:

                # add empty places to allow for attacking those locations
                if not self.get_game_piece_by_location(num, col):
                    if current_piece.convert_coordinates_to_string(num, col) not in current_piece.get_legal_moves():
                        try:
                            current_piece.get_legal_moves().append(
                                current_piece.convert_coordinates_to_string(num, col))
                        except ValueError:
                            pass

                # add enemy locations
                elif self.get_game_piece_by_location(
                        num, col).get_game_piece_color() != current_piece.get_game_piece_color():
                    try:
                        current_piece.get_legal_moves().append(
                            current_piece.convert_coordinates_to_string(num, col))
                        break
                    except ValueError:
                        break

            # add the functionality to attack if we found a first piece
            if self.get_game_piece_by_location(num, col):
                can_attack = True


class XiangqiPiece:
    """Represents a playable piece of a Xiangqi game"""

    def __init__(self, name=None, color=None):
        """Initializes a game piece with ID and color"""
        self._name = name
        self._color = color
        self._location_row = None
        self._location_col = None
        self._moveset_row = range(0, 10)
        self._moveset_col = range(0, 9)
        self._legal_moves = None

    def get_game_piece_name(self):
        """A method to return a game piece's name"""
        return self._name

    def get_game_piece_color(self):
        """A method to return a game piece's color"""
        return self._color

    def get_game_piece_location_row(self):
        """A method to return a game piece's row location"""
        return self._location_row

    def get_game_piece_location_col(self):
        """A method to return a game piece's column location"""
        return self._location_col

    def convert_coordinates_to_string(self, row, col):
        """
        A method to convert the integers indexes to alpha numeric characters
        :returns the row and column as concatenated strings
        """
        try:
            # Create dictionary to cross reference
            convert_dict_row = {0: "10", 1: "9", 2: "8", 3: "7", 4: "6", 5: "5", 6: "4", 7: "3", 8: "2", 9: "1"}
            convert_dict_col = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

            # convert and store the values as strings, then return them together
            row_string = convert_dict_row[row]
            col_string = convert_dict_col[col]
            return col_string + row_string
        except KeyError:
            return "N/A"

    def update_game_piece_location(self, row, col):
        """A method to update a game piece's location and available moves"""
        self._location_row = row
        self._location_col = col

        if type(self) == General:
            self.update_general_legal_moves(row, col)
        elif type(self) == Advisor:
            self.update_advisor_legal_moves(row, col)
        elif type(self) == Elephant:
            self.update_elephant_legal_moves(row, col)
        elif type(self) == Horse:
            self.update_horse_legal_moves(row, col)
        elif type(self) == Chariot:
            self.update_chariot_legal_moves(row, col)
        elif type(self) == Cannon:
            self.update_cannon_legal_moves(row, col)
        elif type(self) == Soldier:
            self.update_soldier_legal_moves(row, col)
        else:
            pass

    def get_legal_moveset_row(self):
        """A method to return a list of legal moves by row"""
        return self._moveset_row

    def get_legal_moveset_col(self):
        """A method to return a list of legal moves by column"""
        return self._moveset_col

    def get_legal_moves(self):
        """A method to get all the available legal moves"""
        return self._legal_moves

    def update_general_legal_moves(self, row, col):
        """A method to update the legal moves available by General"""
        # moves one space orthogonally, can't leave the palace
        self._legal_moves = []
        if col + 1 in range(3, 6):
            self._legal_moves.append(self.convert_coordinates_to_string(row, col + 1))
        if col - 1 in range(3, 6):
            self._legal_moves.append(self.convert_coordinates_to_string(row, col - 1))

        if self.get_game_piece_color() == "Red":
            if row + 1 in range(7, 10):
                self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col))
            if row - 1 in range(7, 10):
                self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col))
        else:
            if row + 1 in range(0, 3):
                self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col))
            if row - 1 in range(0, 3):
                self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col))

        # remove if None was added to keep the list cleaner
        try:
            self._legal_moves.remove("N/A")
        except ValueError:
            pass

    def update_advisor_legal_moves(self, row, col):
        """A method to update the legal moves available by Advisor"""
        # reset with each move
        self._legal_moves = []

        # moves one space diagonally, can't leave the palace
        if col + 1 in range(3, 6):
            if self.get_game_piece_color() == "Red":
                if row + 1 in range(7, 10):
                    self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col + 1))
                if row - 1 in range(7, 10):
                    self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col + 1))
            else:
                if row + 1 in range(0, 3):
                    self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col + 1))
                if row - 1 in range(0, 3):
                    self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col + 1))
        if col - 1 in range(3, 6):
            if self. get_game_piece_color() == "Red":
                if row + 1 in range(7, 10):
                    self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col - 1))
                if row - 1 in range(7, 10):
                    self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col - 1))
            else:
                if row + 1 in range(0, 3):
                    self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col - 1))
                if row - 1 in range(0, 3):
                    self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col - 1))

        # remove if None was added to keep the list cleaner
        try:
            self._legal_moves.remove("N/A")
        except ValueError:
            pass

    def update_elephant_legal_moves(self, row, col):
        """A method to update the legal moves available by Elephant"""
        # reset with each move
        self._legal_moves = []

        # add the movable locations, 2 steps diagonally
        self._legal_moves.append(self.convert_coordinates_to_string(row + 2, col + 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 2, col + 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 2, col - 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row + 2, col - 2))

        # remove if None was added to keep the list cleaner
        try:
            self._legal_moves.remove("N/A")
        except ValueError:
            pass

    def update_horse_legal_moves(self, row, col):
        """A method to update the legal moves available by Horse"""
        # reset with each move
        self._legal_moves = []

        # move one place orthogonal the one place diagonal
        self._legal_moves.append(self.convert_coordinates_to_string(row + 2, col + 1))
        self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col + 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col + 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 2, col + 1))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 2, col - 1))
        self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col - 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col - 2))
        self._legal_moves.append(self.convert_coordinates_to_string(row + 2, col - 1))

        # remove if None was added to keep the list cleaner
        try:
            self._legal_moves.remove("N/A")
        except ValueError:
            pass

    def update_chariot_legal_moves(self, row, col):
        """A method to update the legal moves available by Chariot"""
        # reset with each move
        self._legal_moves = []

        # moves like a rook, in a column or row
        for x in range(10):
            if x != row:
                self._legal_moves.append(self.convert_coordinates_to_string(x, col))
        for y in range(9):
            if y != col:
                self._legal_moves.append(self.convert_coordinates_to_string(row, y))

    def update_cannon_legal_moves(self, row, col):
        """A method to update the legal moves available by Cannon"""
        # reset with each move
        self._legal_moves = []

        # moves like a rook, in a column or row, attacking takes place elsewhere
        for x in range(10):
            if x != row:
                self._legal_moves.append(self.convert_coordinates_to_string(x, col))
        for y in range(9):
            if y != col:
                self._legal_moves.append(self.convert_coordinates_to_string(row, y))

    def update_soldier_legal_moves(self, row, col):
        """A method to update the legal moves available by Soldier"""
        # moves one place forward until reaching the river it can then move left and right
        if self.get_game_piece_color() == "Red":
            self._legal_moves = []
            if self.get_game_piece_location_row() <= 4:
                self._legal_moves.append(self.convert_coordinates_to_string(row, col + 1))
                self._legal_moves.append(self.convert_coordinates_to_string(row, col - 1))
            self._legal_moves.append(self.convert_coordinates_to_string(row - 1, col))
        else:
            self._legal_moves = []
            if self.get_game_piece_location_row() >= 5:
                self._legal_moves.append(self.convert_coordinates_to_string(row, col + 1))
                self._legal_moves.append(self.convert_coordinates_to_string(row, col - 1))
            self._legal_moves.append(self.convert_coordinates_to_string(row + 1, col))

            # remove if None was added to keep the list cleaner
        try:
            self._legal_moves.remove("N/A")
        except ValueError:
            pass

class General(XiangqiPiece):
    """Represents a Xiangqi General game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new General game piece"""
        self._in_check = False
        self._name = " G "
        self._color = color
        self._moveset_col = range(3, 6)
        self._flying_moves = []

        # set moveset by color, column is the same for both
        if self.get_game_piece_color() == "Red":
            self._moveset_row = range(7, 10)
        else:
            self._moveset_row = range(0, 3)

    def get_flying_moves(self):
        """A method to return the flying general's moves"""
        return self._flying_moves

    def get_check_status(self):
        """A method to return current in check status for a General"""
        return self._in_check

    def update_check_status(self, true_false=bool):
        """
        A method to update the current check status. Receives a boolean value and reassigns the _in_check attribute
        :type true_false: bool
        """
        self._in_check = true_false


class Advisor(XiangqiPiece):
    """Represents a Xiangqi Advisor game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Advisor game piece"""
        self._name = " A "
        self._color = color
        self._moveset_col = range(3, 6)

        # set moveset by color, column is the same for both
        if self.get_game_piece_color() == "Red":
            self._moveset_row = range(7, 10)
        else:
            self._moveset_row = range(0, 3)


class Elephant(XiangqiPiece):
    """Represents a Xiangqi Elephant game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Elephant game piece"""
        self._name = " E "
        self._color = color
        self._moveset_col = (0, 2, 4, 6, 8)

        # set moveset by color, it only has seven locations it can move
        if self.get_game_piece_color() == "Red":
            self._moveset_row = (5, 7, 9)
        else:
            self._moveset_row = (0, 2, 4)


class Horse(XiangqiPiece):
    """Represents a Xiangqi Horse game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Horse game piece"""
        self._name = " H "
        self._color = color


class Chariot(XiangqiPiece):
    """Represents a Xiangqi Chariot game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Chariot game piece"""
        self._name = " R "
        self._color = color


class Cannon(XiangqiPiece):
    """Represents a Xiangqi Cannon game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Cannon game piece"""
        self._name = " C "
        self._color = color


class Soldier(XiangqiPiece):
    """Represents a Xiangqi Soldier game piece"""

    def __init__(self, name, color):
        super().__init__(name, color)
        """Initializes a new Soldier game piece"""
        self._name = " S "
        self._color = color

        if self.get_game_piece_color() == "Red":
            self._moveset_row = range(0, 7)
            if self.get_game_piece_location_row() != 9:
                self._moveset_col = (0, 2, 4, 6, 8)
        else:
            self._moveset_row = range(3, 10)
            if self.get_game_piece_location_row() != 0:
                self._moveset_col = (0, 2, 4, 6, 8)


def main():
    # main function to be run when not imported only
    g1 = XiangqiGame()
    g1.make_move("a1", "a2")  # red
    g1.make_move("a10", "a9")  # black
    g1.make_move("e1", "e2")  # red
    g1.make_move("a9", "a10")  # black
    g1.make_move("a2", "d2")  # red
    g1.make_move("a7", "a6")
    g1.make_move("d2", "d9")  # red
    g1.make_move("b8", "b9")
    g1.make_move("e2", "d2")  # red
    g1.make_move("b9", "b8")
    g1.make_move("d9", "d10")  # red
    print(g1.get_game_board().get_game_piece_by_location(0, 4).get_legal_moves())
    g1.make_move("e10", "e9")  # ??
    # g1.make_move("e4", "e5")  # red
    # g1.make_move("b9", "b8")
    # g1.make_move("e5", "e6")  # red
    # g1.make_move("b8", "b9")
    # g1.make_move("e6", "e7")  # red
    # g1.make_move("b9", "b8")
    # g1.make_move("b3", "e3")
    g1.display_game_board()
    print(g1.get_game_state())
    pass

# added to prevent running as a script when imported
if __name__ == '__main__':
    main()
