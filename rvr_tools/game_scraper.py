from typing import List

import requests
import re
from bs4 import BeautifulSoup


# TODO make work with finished games
class Player():
    def __init__(self, game, id) -> None:
        self.game = game
        self.id = id
        self.state = game.state.find(id='player-table-' + self.id)
        self.situation = game.situation.find(id='position-table-' + self.id)
        self.name = self.state.find('strong').text
        self.stack = int(self.state.find_all('td')[1].text)
        self.invest = int(self.state.find_all('td')[2].text)
        self.init_invest = int(self.situation.find_all('td')[2].text)
        self.status = self.state.find_all('td')[3].text[2:-2]
        self.acting = self.status == 'acting now'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(game={self.game}, id={self.id})"

    def __str__(self) -> str:
        return self.name


class History():
    def __init__(self, game) -> None:
        self.game: Game = game
        self.last_street = 'Preflop'
        self.soup = self.game.soup.find(id='history')
        self.events: List[Event] = self._get_events()

    def _set_v_invest(self, events):
        last_name = events[-1].player.name
        last_amount = events[-1].amount
        vil_amts = [event.amount for event in events if event.player.name ==
                    last_name and event.street == self.last_street]
        events[-1].player.invest = sum(vil_amts) - last_amount

    def _get_events(self):
        events = []
        for event in self.soup.find_all('td'):
            text = Event.purify(event)
            if text in ['Flop:', 'Turn:', 'River:']:
                self.last_street = text[:-1]
            player: Player = self.game.get_player_by_name(text)
            if player is None:
                continue
            e = Event(game=self.game,
                      text=text,
                      player=player,
                      street=self.last_street,
                      )
            events.append(e)
        self._set_v_invest(events)
        return events


class Event():
    def __init__(self, game, text, player: Player, street: str) -> None:
        self.game = game
        self.text = text
        self.player = player
        self.street = street
        self.amount = 0
        self.action = None
        self._parse_text()

    def _parse_text(self):
        name_spaces: int = self.player.name.count(' ')
        if self.player.name not in self.text:
            raise ValueError(f"{self.text} is not a valid Event text.")
        action = self.text.split()[1 + name_spaces]

        if action == "checks":
            self.action = "check"
        elif action == 'calls':
            self.action = 'call'
        elif action == "raises":
            self.action = "raise"
            self.amount = int(self.text.split()[3 + name_spaces])
        elif action == "bets":
            self.action = "bet"
            self.amount = int(self.text.split()[2 + name_spaces])
        elif action == "folds":
            self.action = "fold"
        else:
            raise ValueError(f"{self.text} is not a valid Event text.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(game={self.game}, " + \
            f" text={self.text}, player={self.player}" + \
            f", street={self.street})"

    def __str__(self) -> str:
        return f"{self.street}, {self.text}"

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


class Game():
    def __init__(self, id):
        self.id = id
        self._html = requests.get("https://www.rangevsrange.com/game?gameid="
                                  + self.id)
        self.soup = BeautifulSoup(self._html.content, 'html.parser')
        self.state = self.soup.find(id='game-state')
        self.situation = self.soup.find(id='situation')
        self.sit_name = self.situation.find_all('strong')[0].nextSibling[:-2]
        self.hero: Player = None  # set via self._get_players()
        self.players: List[Player] = self._get_players()
        self.history = History(self)
        self.pot = self._get_pot()
        self.total_pot = self._get_total_pot()
        self.to_call = self.last_bet - self.hero.invest

    def _get_players(self):
        players = []
        try:
            for player in self.state.find_all('tr')[1:]:
                p = Player(self, player.get('id')[-1:])
                if p.acting:
                    self.hero = p
                players.append(p)
            return players
        except AttributeError:
            return []

    def _get_pot(self) -> int:
        pot_txt = 'The pot at the start of this round was:'
        try:
            pot_soup = self.state.find(text=re.compile(pot_txt)).nextSibling
            return int(pot_soup.text)
        except AttributeError:
            try:
                pot_soup = self.situation.find_all('strong')[1]
                pot_soup = pot_soup.nextSibling
                return int(pot_soup)
            except AttributeError:
                return 0

    def _get_total_pot(self) -> int:
        if self.history.last_street == "Preflop":
            return self.last_bet + self.hero.invest + self.pot
        else:
            return self.pot + self.last_bet

    def __str__(self) -> str:
        return f"Game: {self.id}"

    def __repr__(self) -> str:
        return f"Game({self.id})"

    def get_player_by_name(self, text: str):
        for p in self.players:
            if p.name in text:
                return p

    @property
    def acted_last(self) -> Player:
        return self.history.events[-1].player

    @property
    def last_bet(self) -> int:
        if self.history.last_street == self.history.events[-1].street:
            return self.history.events[-1].amount
        else:
            return 0

    def next_bet(self, percentage: float) -> float:
        """
        Function to return next betsize.

        Parameters
        ----

        percentage  =  Percentage of pot in decimal. So 1 = 100% pot
                       and .5 = 50% pot
        """
        return round((((self.total_pot + self.to_call) * percentage)
                      + self.to_call), 1)


class DecisionEvent(Event):
    pass


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
    main('8422')
