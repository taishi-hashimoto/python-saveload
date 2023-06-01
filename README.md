# python-saveload

Simple Python variable serializer/loader using pickle.

```Python
from saveload import save, load

obj1 = "hoge"
obj2 = 42

# Positional manner
save("test.pkl", obj1, obj2)
obj1, obj2 = load("test.pkl")

# Named manner
save("test.pkl", obj1=obj1, obj2=obj2)
objects = load("test.pkl")  # objects = {"obj1: ..., "obj2": ...}

# This will restore variables into the current local environment.
locals().update(load("test.pkl"))
```
