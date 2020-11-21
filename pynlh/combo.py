class Combo():
    def __init__(self,
                 combo_str: str = None,
                 hand: str = None,
                 suit1: str = None,
                 suit2: str = None,
                 ) -> None:
        """
        Pynlh's Combo class object.

        Can be isntanciated either giving it a combo_str like "Ac5d" or a hand
        string like "AK" and two suits "c" "d".
        """
        
