from .navigation_command import NavigationCommand


class NavigationGuide(list[NavigationCommand]):
    def __init__(self, iterable: list = []):
        super().__init__(NavigationCommand(**item) for item in iterable)

    def __setitem__(self, index, item):
        super().__setitem__(index, NavigationCommand(**item))

    def insert(self, index, item):
        super().insert(index, NavigationCommand(**item))

    def append(self, item):
        super().append(NavigationCommand(**item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(NavigationCommand(**other))
        else:
            super().extend(NavigationCommand(**item) for item in other)

    @property
    def first(self):
        return self[0]

    @property
    def last(self):
        return self[-1]
