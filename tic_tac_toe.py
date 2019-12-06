import random

reference_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
game_play_board = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
game_over = False


def play_board(board):
    game_board = board[0] + '|' + board[1] + '|' + board[2] + '\n' + board[3] + '|' + board[4] + '|' + board[5] +\
                 '\n' + board[6] + '|' + board[7] + '|' + board[8]
    return game_board


def replace_element(index, selection):
    game_play_board[index - 1] = selection
    print(play_board(game_play_board))
    reference_board.remove(index)


def computer_first_choice(users_first_turn, computer_symbol):
    print("Computers Turn")
    tough_move = [1, 3, 7, 9]
    if users_first_turn % 2 == 0:
        if users_first_turn == 2:
            temp_list = [1, 3]
            random.shuffle(temp_list)
            for i in temp_list:
                if i in reference_board:
                    computer_choice = i
                    return computer_choice
        elif users_first_turn == 4:
            temp_list = [1, 7]
            random.shuffle(temp_list)
            for i in temp_list:
                if i in reference_board:
                    computer_choice = i
                    return computer_choice
        elif users_first_turn == 6:
            temp_list = [9, 3]
            random.shuffle(temp_list)
            for i in temp_list:
                if i in reference_board:
                    computer_choice = i
                    return computer_choice
        else:
            temp_list = [7, 9]
            random.shuffle(temp_list)
            for i in temp_list:
                if i in reference_board:
                    computer_choice = i
                    return computer_choice
    elif users_first_turn in tough_move:
        if 5 in reference_board:
            computer_choice = 5
            return computer_choice
    else:
        if computer_symbol == 'X':
            computer_choice = 9
        else:
            computer_choice = random.choice(reference_board)
        replace_element(computer_choice, computer_symbol)
        return computer_choice


def computer_second_choice(users_first_turn, users_second_turn, computer_first_turn, computer_symbol):
    print("Computers Turn")
    local_list = [users_first_turn, users_second_turn]
    possible_lines = []
    for sublist in COMBINATION:
        if users_first_turn in sublist and users_second_turn in sublist and computer_first_turn not in sublist:
            replace_number = [i for i in sublist if i not in local_list][0]
            if replace_number in reference_board:
                replace_element(replace_number, computer_symbol)
                return True, replace_number
        elif (users_first_turn in sublist or users_second_turn in sublist) and computer_first_turn not in sublist:
            possible_lines.append(sublist)
    else:
        # print("possible_lines", possible_lines)
        if 5 in reference_board:
            replace_number = 5
            replace_element(replace_number, computer_symbol)
            return True, replace_number
        else:
            for sublist in COMBINATION:
                if users_first_turn not in sublist and users_second_turn not in sublist and computer_first_turn in \
                        sublist:
                    replace_number = [i for i in sublist if i != computer_first_turn if i in reference_board]
                    if len(replace_number) == 2:
                        if users_first_turn % 2 != 0 and users_second_turn % 2 != 0:
                            replace_element(6, computer_symbol)
                            return True, 6
                        else:
                            # print("replace_number", replace_number)
                            for position in replace_number:
                                occurrence = 0
                                for row in possible_lines:
                                    if position in row:
                                        occurrence += 1
                                        if occurrence == 2:
                                            replace_element(position, computer_symbol)
                                            return True, position
            else:
                replace_number = reference_board[0]
                replace_element(replace_number, computer_symbol)
                return True, replace_number


def find_winner(user_options, computer_options):
    user_winner_list = []
    com_winner_list = []
    for sublist in COMBINATION:
        compare_user = []
        compare_computer = []
        if len(user_options) >= 3 or computer_options >= 3:
            for user_item in user_options:
                if user_item in sublist:
                    compare_user.append(user_item)
            for comp_item in computer_options:
                if comp_item in sublist:
                    compare_computer.append(comp_item)
        if sorted(compare_user) == sorted(sublist):
            print("YOU WON!")
            return True, None, None
        if sorted(compare_computer) == sorted(sublist):
            print("You LOST!")
            return True, None, None
        if len(compare_user) == 2:
            winner_move = [i for i in sublist if i not in compare_user][0]
            if winner_move in reference_board:
                # print("USER", winner_move)
                user_winner_list.append(winner_move)
        if len(compare_computer) == 2:
            winner_move = [i for i in sublist if i not in compare_computer][0]
            if winner_move in reference_board:
                # print("COMPUTER", winner_move)
                com_winner_list.append(winner_move)
    return False, user_winner_list, com_winner_list


def select_move(com_win_move, user_win_move, computer_options, computer_symbol):
    print("Computer Turn")
    computer_third_turn = None
    second_next_move = None
    if len(com_win_move) > 0:
        replace_element(com_win_move[0], computer_symbol)
        second_next_move, computer_third_turn = True, com_win_move[0]
    elif len(user_win_move) > 0:
        replace_element(user_win_move[0], computer_symbol)
        second_next_move, computer_third_turn = True, user_win_move[0]
    else:
        for list_combo in COMBINATION:
            win_choice = [[i for i in list_combo if i != item] for item in computer_options if item in list_combo]
            # print("win_choice", win_choice, list_combo)
            if len(win_choice) > 0:
                win_choice = win_choice[0]
            else:
                win_choice = win_choice
            index = 0
            for i in win_choice:
                # print(i)
                if i in reference_board:
                    index += 1
                    if index == len(win_choice):
                        replace_element(i, computer_symbol)
                        second_next_move, computer_third_turn = True, i

        else:
            if computer_third_turn is None:
                second_next_move, computer_third_turn = True, reference_board[0]
                replace_element(reference_board[0], computer_symbol)

    return second_next_move, computer_third_turn


def user_selection(position):
    attempt = 0
    users_choice = None
    game_status = False
    n = 2
    while attempt < n:
        try:
            users_choice = int(input("Enter your %s position from reference board:" % position))
        except ValueError:
            game_status = True
            attempt += 1
            print("Invalid response --", n-attempt, "attempt left")
        else:
            if users_choice in reference_board:
                game_status = False
                attempt = n
                users_choice = users_choice
            else:
                attempt += 1
                print("Select from available:", reference_board, "--", n-attempt, "attempt left")
                game_status = True
    return users_choice, game_status


def flip():
    noughts_or_crosses = input("Choose X or O to begin:")
    if noughts_or_crosses in ['x', 'X']:
        user_symbol = 'X'
        computer_symbol = 'O'
    elif noughts_or_crosses in ['o', 'O', '0']:
        user_symbol = 'O'
        computer_symbol = 'X'
    else:
        user_symbol = None
        computer_symbol = None
        print("Invalid selection")
    return user_symbol, computer_symbol


def play_game():
    global game_over
    while not game_over:
        user_symbol, computer_symbol = flip()
        if user_symbol == 'X':
            users_first_choice, game_over = user_selection('first')
            if not game_over:
                replace_element(users_first_choice, user_symbol)
                computer_first_turn = computer_first_choice(users_first_choice, computer_symbol)
                users_second_choice, game_over = user_selection('second')
                if not game_over:
                    replace_element(users_second_choice, user_symbol)
                    first_next_move, computer_second_turn = computer_second_choice(users_first_choice,
                                                                                   users_second_choice,
                                                                                   computer_first_turn, computer_symbol)
                    if first_next_move:
                        users_third_choice, game_over = user_selection('third')
                        if not game_over:
                            replace_element(users_third_choice, user_symbol)
                            user_option = [users_first_choice, users_second_choice, users_third_choice]
                            computer_option = [computer_first_turn, computer_second_turn]
                            game_over, user_win_move, com_win_move = find_winner(user_option, computer_option)
                            # print(user_win_move, com_win_move)
                            if not game_over:
                                second_next_move, computer_third_turn = select_move(com_win_move, user_win_move,
                                                                                    computer_option, computer_symbol)
                                computer_option += [computer_third_turn]
                                # print(computer_option, user_option)
                                game_over, user_win_move, com_win_move = find_winner(user_option, computer_option)
                                if second_next_move and not game_over:
                                    users_fourth_choice, game_over = user_selection('fourth')
                                    if not game_over:
                                        replace_element(users_fourth_choice, user_symbol)
                                        user_option += [users_fourth_choice]
                                        game_over, user_win_move, com_win_move = find_winner(user_option,
                                                                                             computer_option)
                                        if not game_over:
                                            next_move, computer_fourth_turn = select_move(com_win_move, user_win_move,
                                                                                          computer_option,
                                                                                          computer_symbol)
                                            computer_option += [computer_fourth_turn]
                                            if next_move:
                                                game_over,  user_win_move, com_win_move = find_winner(user_option,
                                                                                                      computer_option)
                                                if not game_over:
                                                    users_fifth_choice, game_over = user_selection('fifth')
                                                    replace_element(users_fifth_choice, user_symbol)
                                                    user_option += [users_fifth_choice]
                                                    game_over, user_win_move, com_win_move = find_winner(user_option,
                                                                                                         computer_option)
                                                    if not game_over:
                                                        print("DRAW!")
                                                        game_over = True
        elif user_symbol == 'O':
            random_computer_position = random.choice(reference_board)
            replace_element(random_computer_position, computer_symbol)
            users_first_choice, game_over = user_selection('first')
            if not game_over:
                replace_element(users_first_choice, user_symbol)
                computer_first_turn = computer_first_choice(users_first_choice, computer_symbol)
                users_second_choice, game_over = user_selection('second')
                if not game_over:
                    replace_element(users_second_choice, user_symbol)
                    first_next_move, computer_second_turn = computer_second_choice(users_first_choice,
                                                                                   users_second_choice,
                                                                                   computer_first_turn, computer_symbol)
                    if first_next_move:
                        users_third_choice, game_over = user_selection('third')
                        if not game_over:
                            replace_element(users_third_choice, user_symbol)
                            user_option = [users_first_choice, users_second_choice, users_third_choice]
                            computer_option = [computer_first_turn, computer_second_turn]
                            game_over, user_win_move, com_win_move = find_winner(user_option, computer_option)
                            # print(user_win_move, com_win_move)
                            if not game_over:
                                second_next_move, computer_third_turn = select_move(com_win_move, user_win_move,
                                                                                    computer_option, computer_symbol)
                                computer_option += [computer_third_turn]
                                # print(computer_option, user_option)
                                game_over, user_win_move, com_win_move = find_winner(user_option, computer_option)
                                if second_next_move and not game_over:
                                    users_fourth_choice, game_over = user_selection('fourth')
                                    if not game_over:
                                        replace_element(users_fourth_choice, user_symbol)
                                        user_option += [users_fourth_choice]
                                        game_over, user_win_move, com_win_move = find_winner(user_option,
                                                                                             computer_option)
                                        if not game_over:
                                            next_move, computer_fourth_turn = select_move(com_win_move, user_win_move,
                                                                                          computer_option,
                                                                                          computer_symbol)
                                            computer_option += [computer_fourth_turn]
                                            if next_move:
                                                game_over, user_win_move, com_win_move = find_winner(user_option,
                                                                                                     computer_option)
                                                if not game_over:
                                                    print("DRAW!")
                                                    game_over = True


if __name__ == '__main__':
    print("REFERENCE BOARD:" + '\n' + play_board([str(i) for i in reference_board]))
    COMBINATION = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
    play_game()
