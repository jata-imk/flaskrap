from typing import List, Dict

class PivotImageFilter:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def table_id(self) -> List[int]:
        # Este campo se llamará {nombre_tabla_uno}_id
        return self.__dict__["table_id"]

    @property
    def is_primary(self) -> bool:
        return self.__dict__["is_primary"]

    @property
    def include(self) -> Dict:
        return self.__dict__["include"]