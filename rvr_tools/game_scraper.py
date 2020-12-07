import re
from typing import List

import requests
from bs4 import BeautifulSoup


# TODO make work with finished games
class Game():
    def __init__(self, id):
        self.id = id
        self._html = requests.get("https://www.rangevsrange.com/game?gameid="
                                  + self.id)
        self.soup = BeautifulSoup(self._html.content, 'html.parser')
        self.state = self.soup.find(id='game-state')
        self.players: List[Player] = self._get_players()
        self.hero: Player = None
        self.history = History(self)
        self.pot: int = int(self.state.find('strong').text)

    def _get_players(self):
        players = []
        for player in self.state.find_all('tr')[1:]:
            p = Player(self, player.get('id')[-1:])
            players.append(p)
        return players

    def __str__(self) -> str:
        return f"Game: {self.id}"

    def __repr__(self) -> str:
        return f"Game({self.id})"

    def get_player_by_name(self, name):
        for p in self.players:
            if name == p.name:
                return p


class Player():
    def __init__(self, game, id) -> None:
        self.game = game
        self.id = id
        self.state = game.state.find(id='player-table-' + self.id)
        self.name = self.state.find('strong').text
        self.stack = int(self.state.find_all('td')[1].text)
        self.invest = int(self.state.find_all('td')[2].text)
        self.status = self.state.find_all('td')[3].text[2:-2]
        self.acting = self.status == 'acting now'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(game={self.game}, id={self.id})"

    def __str__(self) -> str:
        return self.id


class History():
    def __init__(self, game: Game) -> None:
        self.game = game
        self.soup = self.game.soup.find(id='history')
        self.events: List[Event] = self._get_events()

    def _get_events(self):
        events = []
        for event in self.soup.find_all('td'):
            text = Event.purify(event)
            if text in ['Flop:', 'Turn:', 'River:']:
                self.last_street = text[:-1]
            player = self.game.get_player_by_name(text.split()[0])
            if player is None:
                continue
            e = Event(game=self.game,
                      text=text,
                      player=player,
                      street=self.last_street,
                      )
            events.append(e)
        return events


class Event():
    def __init__(self, game: Game, text, player: Player, street: str) -> None:
        self.game = game
        self.text = text
        self.player = player
        self.street = street

    def _parse_text(self):
        if self.player.name != self.text.split()[0]:
            raise ValueError(f"{self.text} is not a valid Event text.")
        action = self.text.split()[1]

        if action == "checks":
            self.action = "check"
        elif action == "raises":
            self.action = "raise"
            self.amount = int(self.text.split()[3])
        elif action == "bets":
            self.action = "bet"
            self.amount = int(self.text.split()[2])
        elif action == "folds":
            self.action = "fold"
        else:
            raise ValueError(f"{self.text} is not a valid Event text.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(game={self.game}, " + \
            f"content={self.text})"

    def __str__(self) -> str:
        return self.text

    @staticmethod
    def purify(content) -> str:
        """
        cleans the given event tag and returns the clean text.
        """
        rv = content.text.split()
        rv = ' '.join(rv[0:4])
        rv = rv.replace('(ranges', '')
        rv = rv.replace('hidden', '')
        return rv


class EventDecision(Event):
    pass


class GameScraper():

    def __init__(self, game_id) -> None:
        self.game_id = game_id
        self._page = requests.get("https://www.rangevsrange.com/game?gameid="
                                  + game_id)
        self._soup = BeautifulSoup(self._page.content, 'html.parser')
        self._state = self._soup.find(id='game-state')
        self._state_act = self._state.find(id='player-table-'
                                           + self._active_id)
        self._state_v1 = self._state.find(id='player-table-' +
                                          self._villain_ids[0])
        if len(self._villain_ids) == 2:
            self._state_v2 = self._state.find(id='player-table-' +
                                              self._villain_ids[1])
        else:
            self._state_v2 = None

    @property
    def _active_id(self) -> str:
        active = self._soup.find(text=re.compile('acting now'))
        return active.parent.parent.parent.get('id')[-1:]

    @property
    def _villain_ids(self) -> List[str]:
        try:
            vils = self._soup.find_all(text=re.compile('acted'))
            acted = [vil.parent.parent.parent.get('id')[-1:] for vil in vils]
        except AttributeError:
            pass
        try:
            vils = self._soup.find_all(text=re.compile('still to act'))
            to_act = [vil.parent.parent.parent.get('id')[-1:] for vil in vils]
        except AttributeError:
            pass
        finally:
            return acted + to_act

    @property
    def pot(self) -> int:
        return int(self._state.find('strong').text)

    @property
    def hero_name(self) -> str:
        return self._state_act.find('strong').text

    @property
    def vil1_name(self) -> str:
        return self._state_v1.find('strong').text

    @property
    def vil2_name(self) -> str:
        return self._state_v2.find('strong').text

    @property
    def hero_stack(self) -> str:
        return (self._state.find(id='player-table-' + self._active_id).
                find_all('td')[1].text)

    @property
    def vil1_stack(self) -> str:
        return (self._state.find(id='player-table-' + self._villain).
                find_all('td')[1].text)

    @property
    def hero_invest(self) -> int:
        return (int(self._state.find(id='player-table-' + self._active_id).
                    find_all('td')[2].text))

    @property
    def vil1_invest(self) -> int:
        return (int(self._state.find(id='player-table-' + self._villain).
                    find_all('td')[2].text))

    @ property
    def hero_status(self) -> str:
        return (self._state.find(id='player-table-' + self._active_id).
                find_all('td')[3].text[2:-2])

    @ property
    def villain_status(self) -> str:
        return (self._state.find(id='player-table-' + self._villain).
                find_all('td')[3].text[2:-2])


def main(game_id):
    # g = GameScraper(game_id)
    # print(g.hero_name)
    # print(g.villain_name)
    g = Game(game_id)
    # g.get_players()
    print(g)
    print(f"Potsize: {g.pot}\n")
    for p in g.players:
        print(f"Name: {p.name}, Acting: {p.acting}, Stack: {p.stack}, "
              f"Invest: {p.invest}, Status: {p.status}"
              )
    print("\nHistory:")
    for e in g.history.events:
        print(e.text)
    print("\nLast Street:")
    print(g.history.last_street)
    for e in g.history.events:
        print(e)


if __name__ == "__main__":
    main('8400')
