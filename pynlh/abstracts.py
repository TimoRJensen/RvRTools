from abc import ABC, abstractmethod


class PynlhComponent(ABC):

    @abstractmethod
    def apply_rng() -> bool:
        pass


class ComboComposite(PynlhComponent, ABC):
    pass
