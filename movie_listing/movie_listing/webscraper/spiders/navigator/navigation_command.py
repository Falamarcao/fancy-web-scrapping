from typing import Any

from selenium.webdriver.common.by import By


class NavigationCommand:
    def __init__(self, **kwargs):
        for key in ('human_label', 'actions', 'many', 'subcommands', 'model_name', 'get_attribute', 'CLASS_NAME', 'CSS_SELECTOR', 'ID',
                    'LINK_TEXT', 'NAME', 'PARTIAL_LINK_TEXT', 'TAG_NAME', 'XPATH'):
            if key in kwargs:
                if key == 'subcommands':
                    setattr(self, key, [NavigationCommand(
                            **command) for command in kwargs[key]])
                else:
                    setattr(self, key, kwargs[key])

        self.__attrname = next(filter(lambda x: x.isupper(),
                                      list(self.__dict__.keys())), None)

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except:
            return None

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    @property
    def by(self):
        return getattr(By, self.__attrname)

    @property
    def path(self):
        return getattr(self, self.__attrname)

    def to_dict(self):
        dic_repr = self.__dict__.copy()
        del dic_repr['_NavigationCommand__attrname']
        return dic_repr
