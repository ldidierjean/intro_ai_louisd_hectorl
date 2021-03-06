import random
from random import randint, choice
from Character import Character
from typing import List, Set

import model
from globals import passages, colors, pink_passages, before, after, mandatory_powers


class Player:
    """
        Class representing the players, either the inspector (player 0)
        or the fantom (player 1)
    """
    num: int
    agent: model.Agent

    def __init__(self, n: int, agent: model.Agent):
        self.num = n
        self.agent = agent
        # Todo: Should not be a str, enum instead.
        self.role: str = "inspector" if n == 0 else "fantom"

    def play(self, game):
        darkOrAloneBefore = self.nbDarkOrAlone(game)
        charact = self.select(
            game.active_cards, game.update_game_state(self.role))

        # purple and brown power choose to activate or not before moving
        moved_character = self.activate_power(charact,
                                              game,
                                              before,
                                              game.update_game_state(self.role))

        self.move(charact,
                  moved_character,
                  game.blocked,
                  game.update_game_state(self.role),
                  game)

        self.activate_power(charact,
                            game,
                            after,
                            game.update_game_state(self.role))
        darkOrAloneAfter = self.nbDarkOrAlone(game)
        if self.agent is not None:
            self.give_points(game, darkOrAloneBefore, darkOrAloneAfter)

    def nbDarkOrAlone(self, game):
        p: List[Set[Character]] = [
            {c for c in game.characters if c.position == i} for i in range(10)]
        darkOrAlone = 0
        for c in game.characters:
            if c.position == game.shadow or len(p[c.position]) == 1:
                darkOrAlone += 1
        return darkOrAlone

    def give_points(self, game, darkOrAloneBefore, darkOrAloneAfter):
        p: List[Set[Character]] = [
            {c for c in game.characters if c.position == i} for i in range(10)]
        fantomeIsDarkOrAlone = False
        if len(p[game.fantom.position]) == 1 or game.fantom.position == game.shadow:
            fantomeIsDarkOrAlone = True
        if self.role == "fantom":
            if fantomeIsDarkOrAlone:
                diff = darkOrAloneAfter - darkOrAloneBefore
            else:
                diff = (8 - darkOrAloneAfter) - (8 - darkOrAloneBefore)
            #print(diff)
            self.agent.give_reward(diff*5, False)
        else:
            b = abs(darkOrAloneBefore - 4)
            a = abs(darkOrAloneAfter - 4)
            self.agent.give_reward((b - a) * 7, False)

    def random_move(self, question):
        data = question['data']
        return random.randint(0, len(data) - 1)

    def select(self, active_cards, game_state):
        """
            Choose the character to activate whithin
            the given choices.
        """
        available_characters = [character.display()
                                for character in active_cards]
        question = {"question type": "select character",
                    "data": available_characters,
                    "game state": game_state}
        selected_character = self.agent.get_action(question) if self.agent is not None else self.random_move(question)
        if self.agent is not None:
            self.agent.give_reward(0, False)

        if selected_character not in range(len(active_cards)):
            selected_character = randint(0, len(active_cards) - 1)

        perso = active_cards[selected_character]

        del active_cards[selected_character]
        return perso

    def get_adjacent_positions(self, charact, game):
        if charact.color == "pink":
            active_passages = pink_passages
        else:
            active_passages = passages
        return [room for room in active_passages[charact.position] if {room, charact.position} != set(game.blocked)]

    def get_adjacent_positions_from_position(self, position, charact, game):
        if charact.color == "pink":
            active_passages = pink_passages
        else:
            active_passages = passages
        return [room for room in active_passages[position] if {room, position} != set(game.blocked)]

    def activate_power(self, charact, game, activables, game_state):
        """
            Use the special power of the character.
        """
        # check if the power should be used before of after moving
        # this depends on the "activables" variable, which is a set.
        if not charact.power_activated and charact.color in activables:
            # check if special power is mandatory
            if charact.color in mandatory_powers:
                power_activation = 1

            # special power is not mandatory
            else:
                question = {"question type": f"activate {charact.color} power",
                            "data": [0, 1],
                            "game state": game_state}
                power_activation = self.agent.get_action(question) if self.agent is not None else self.random_move(
                    question)
                if self.agent is not None:
                    self.agent.give_reward(0, False)

            # the power will be used
            # charact.power represents the fact that
            # the power is still available
            if power_activation:
                charact.power_activated = True

                # red character
                if charact.color == "red":
                    draw = choice(game.alibi_cards)
                    game.alibi_cards.remove(draw)
                    if draw == "fantom":
                        game.position_carlotta += -1 if self.num == 0 else 1
                    elif self.num == 0:
                        draw.suspect = False

                # black character
                if charact.color == "black":
                    for q in game.characters:
                        if q.position in self.get_adjacent_positions(charact, game):
                            q.position = charact.position

                # white character
                if charact.color == "white":
                    for moved_character in game.characters:
                        if moved_character.position == charact.position and charact != moved_character:
                            available_positions = self.get_adjacent_positions(
                                charact, game)

                            # format the name of the moved character to string
                            character_to_move = str(
                                moved_character).split("-")[0]
                            question = {"question type": "white character power move " + character_to_move,
                                        "data": available_positions,
                                        "game state": game_state}
                            selected_index = self.agent.get_action(
                                question) if self.agent is not None else self.random_move(question)
                            if self.agent is not None:
                                self.agent.give_reward(0, False)

                            # test
                            if selected_index not in range(len(available_positions)):
                                selected_position = choice(available_positions)
                            else:
                                selected_position = available_positions[selected_index]

                            moved_character.position = selected_position

                # purple character
                if charact.color == "purple":
                    # logger.debug("Rappel des positions :\n" + str(game))

                    available_characters = [q for q in game.characters if
                                            q.color != "purple"]

                    # the socket can not take an object
                    available_colors = [q.color for q in available_characters]

                    question = {"question type": "purple character power",
                                "data": available_colors,
                                "game state": game_state}
                    selected_index = self.agent.get_action(question) if self.agent is not None else self.random_move(
                        question)
                    if self.agent is not None:
                        self.agent.give_reward(0, False)

                    # test
                    if selected_index not in range(len(colors)):
                        selected_character = choice(colors)

                    else:
                        selected_character = available_characters[selected_index]
                    # swap positions
                    charact.position, selected_character.position = selected_character.position, charact.position
                    return selected_character

                # brown character
                if charact.color == "brown":
                    # the brown character can take one other character with him
                    # when moving.
                    available_characters = [q for q in game.characters if
                                            charact.position == q.position if
                                            q.color != "brown"]

                    # the socket can not take an object
                    available_colors = [q.color for q in available_characters]
                    if len(available_colors) > 0:
                        question = {"question type": "brown character power",
                                    "data": available_colors,
                                    "game state": game_state}
                        selected_index = self.agent.get_action(
                            question) if self.agent is not None else self.random_move(question)
                        if self.agent is not None:
                            self.agent.give_reward(0, False)

                        # test
                        if selected_index not in range(len(colors)):
                            selected_character = choice(colors)
                        else:
                            selected_character = available_characters[selected_index]
                        return selected_character
                    else:
                        return None

                # grey character
                if charact.color == "grey":
                    available_rooms = [room for room in range(10) if room is
                                       not game.shadow]
                    question = {"question type": "grey character power",
                                "data": available_rooms,
                                "game state": game_state}
                    selected_index = self.agent.get_action(question) if self.agent is not None else self.random_move(
                        question)
                    if self.agent is not None:
                        self.agent.give_reward(0, False)

                    # test
                    if selected_index not in range(len(available_rooms)):
                        selected_index = randint(0, len(available_rooms) - 1)
                        selected_room = available_rooms[selected_index]

                    else:
                        selected_room = available_rooms[selected_index]

                    game.shadow = selected_room

                # blue character
                if charact.color == "blue":
                    # choose room
                    available_rooms = [room for room in range(10)]
                    question = {"question type": "blue character power room",
                                "data": available_rooms,
                                "game state": game_state}
                    selected_index = self.agent.get_action(question) if self.agent is not None else self.random_move(
                        question)
                    if self.agent is not None:
                        self.agent.give_reward(0, False)

                    # test
                    if selected_index not in range(len(available_rooms)):
                        selected_index = randint(0, len(available_rooms) - 1)
                        selected_room = available_rooms[selected_index]

                    else:
                        selected_room = available_rooms[selected_index]

                    # choose exit
                    passages_work = passages[selected_room].copy()
                    available_exits = list(passages_work)
                    question = {"question type": "blue character power exit",
                                "data": available_exits,
                                "game state": game_state}
                    selected_index = self.agent.get_action(question) if self.agent is not None else self.random_move(
                        question)
                    if self.agent is not None:
                        self.agent.give_reward(0, False)

                    # test
                    if selected_index not in range(len(available_exits)):
                        __import__('ipdb').set_trace()
                        selected_exit = choice(passages_work)

                    else:
                        selected_exit = available_exits[selected_index]
                    game.blocked = tuple((selected_room, selected_exit))
            else:
                # if the power was not used
                return None

    def move(self, charact, moved_character, blocked, game_state, game):
        """
            Select a new position for the character.
        """

        # get the number of characters in the same room
        characters_in_room = [
            q for q in game.characters if q.position == charact.position]
        number_of_characters_in_room = len(characters_in_room)

        # get the available rooms from a given position
        available_rooms = list()
        available_rooms.append(self.get_adjacent_positions(charact, game))
        for step in range(1, number_of_characters_in_room):
            # build rooms that are a distance equal to step+1
            next_rooms = list()
            for room in available_rooms[step - 1]:
                next_rooms += self.get_adjacent_positions_from_position(room,
                                                                        charact,
                                                                        game)
            available_rooms.append(next_rooms)

        # flatten the obtained list
        temp = list()
        for sublist in available_rooms:
            for room in sublist:
                temp.append(room)

        # filter the list in order to keep an unique occurrence of each room
        temp = set(temp)
        available_positions = list(temp)

        # ensure the character changes room
        if charact.position in available_positions:
            available_positions.remove(charact.position)

        # if the character is purple and the power has
        # already been used, we pass since it was already moved
        # (the positions were swapped)
        if charact.color == "purple" and charact.power_activated:
            pass
        else:
            question = {"question type": "select position",
                        "data": available_positions,
                        "game state": game_state}
            selected_index = self.agent.get_action(question) if self.agent is not None else self.random_move(question)
            if self.agent is not None:
                self.agent.give_reward(0, False)

            # test
            if selected_index not in range(len(available_positions)):
                selected_position = choice(available_positions)

            else:
                selected_position = available_positions[selected_index]

            # it the character is brown and the power has been activated
            # we move several characters with him
            if charact.color == "brown" and charact.power_activated:
                charact.position = selected_position
                if moved_character:
                    moved_character.position = selected_position
            else:
                charact.position = selected_position
