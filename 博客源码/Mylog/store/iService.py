from abc import abstractmethod, ABCMeta
from datetime import datetime
from Mylog import db, cache


class IService(metaclass=ABCMeta):
    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs) -> list:
        pass

    @abstractmethod
    def get_by_many(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_one(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> bool:
        pass

    def extract_attr(self, obj: object) -> dict:
        prop_dict = vars(obj)
        response_dict = {}
        for k, v in prop_dict.items():
            if k.startswith("_") or k.endswith("_"):
                continue
            if isinstance(v, datetime):
                prop_v = v.strftime('%a, %d %b %Y %H:%M:%S %z')
            else:
                prop_v = v
            response_dict[k] = prop_v
        return response_dict

    @abstractmethod
    def save2db(self, obj: object):
        pass

    @abstractmethod
    def delete_from_db(self, obj: object):
        pass


class ServerBase(IService):
    def __init__(self):
        self.__db = db

    def create(self, *args, **kwargs):
        pass

    def get_all(self, *args, **kwargs) -> list:
        pass

    def get_by_many(self, *args, **kwargs):
        pass

    def get_one(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs) -> bool:
        pass

    def delete(self, *args, **kwargs) -> bool:
        pass

    def save2db(self, obj):
        self.__db.session.add(obj)
        self.__db.session.commit()

    def delete_from_db(self, obj: object):
        self.__db.session.delete(obj)
        self.__db.session.commit()

    def update_cache(self, key: str):
        cache.delete(key)
