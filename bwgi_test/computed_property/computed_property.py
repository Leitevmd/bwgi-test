
from functools import wraps
from weakref import WeakKeyDictionary


class computed_property:
    def __init__(self, *dependencies):
        self.dependencies = dependencies
        self._values = WeakKeyDictionary()
        self._versions = WeakKeyDictionary()
        self.fget = None
        self.fset = None
        self.fdel = None
        self.__doc__ = None

    def __call__(self, fget):
        self.fget = fget
        self.__doc__ = fget.__doc__

        @wraps(fget)
        def wrapper(instance):
            current_versions = tuple(getattr(instance, dep, object()) for dep in self.dependencies)
            cached_version = self._versions.get(instance)
            if cached_version == current_versions:
                return self._values[instance]
            value = fget(instance)
            self._versions[instance] = current_versions
            self._values[instance] = value
            return value

        return property(wrapper, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        self.fset = fset
        return self

    def deleter(self, fdel):
        self.fdel = fdel
        return self
