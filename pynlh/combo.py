class ComboError(Exception):
    """
    Exception class pf pynlh's Combo class.
    """
    pass

    def __init__(self, combo_str: str, msg: str = 'Not a valid combo!'):
        self.combo_str = combo_str
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.combo_str}' -> {self.msg}"


class Combo():
    def __init__(self,
                 combo_str: str = None,
                 hand: str = None,
                 suit1: str = None,
                 suit2: str = None,
                 freq: float = 0.00,
                 ) -> None:
        """
        Pynlh's Combo class object.
        Can be isntanciated either giving it a combo_str like "Ac5d" or a hand
        string like "AK" and two suits "c" "d".
        """
        self.combo_str = combo_str
        self.hand = hand
        self.suit1 = suit1
        self.suit2 = suit2
        self.freq = freq

    def __repr__(self) -> str:
        return f"Combo(combo_strt='{self.combo_str}')"

    def __str__(self) -> str:
        return self.combo_str
