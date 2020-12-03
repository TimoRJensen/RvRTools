from bs4 import BeautifulSoup
import re
import requests
from typing import List


class GameScraper():

    def __init__(self, game_id) -> None:
        self.game_id = game_id
        self._page = requests.get("https://www.rangevsrange.com/game?gameid="
                                  + game_id)
        self._soup = BeautifulSoup(self.page.content, 'html.parser')
        self._state = self._soup.find(id='game-state')
        self._state_act = self._state.find(id='player-table-'
                                           + self._active_id)
        self._state_v = self._state.find(id='player-table-')

    @property
    def _active_id(self) -> str:
        active = self._soup.find(text=re.compile('acting now'))
        return active.parent.parent.parent.get('id')[-1:]

    @property
    def _villain_ids(self) -> List[str]:
        try:
            vils = self._soup.find_all(text=re.compile('acted'))
            rv = [vil.parent.parent.parent.get('id')[-1:] for vil in vils]
            vils = self._soup.find_all(text=re.compile('still to act'))
            rv = [vil.parent.parent.parent.get('id')[-1:] for vil in vils]
            return rv
        except AttributeError:
            return None

    @property
    def pot(self) -> int:
        return int(self._state.find('strong').text)

    @property
    def hero_name(self) -> str:
        return self._state_act.find('strong').text

    @property
    def villain_name(self) -> str:
        return self._state_v.find('strong').text

    @property
    def hero_stack(self) -> str:
        return (self._state.find(id='player-table-' + self._active_id).
                find_all('td')[1].text)

    @property
    def villain_stack(self) -> str:
        return (self._state.find(id='player-table-' + self._villain).
                find_all('td')[1].text)

    @property
    def hero_invest(self) -> int:
        return (int(self._state.find(id='player-table-' + self._active_id).
                find_all('td')[2].text))

    @property
    def villain_invest(self) -> int:
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
