"Simple Python variable serializer/loader using pickle."
import sys
import time
import pickle


VERBOSE = True
"Indicate if save/load shows some messages about progress."

BLOCK_SIZE = 2**31-1
"Block size in bytes to write dumped pickle bytes in a file."


def set_verbosity(b: bool):
    "Set verbosity of save/load."
    global VERBOSE
    VERBOSE = b


def save(filename: str, *args, **kwargs) -> None:
    """Save objects into a file using pickle.

    Parameters
    ==========
    filename: str
        File name to be saved.
    args: tuple of Any
        Variable to be saved specified in the positional manner.
    kwargs: dict[str, Any]
        Variable to be saved specified in the named manner.
    
    Note
    ====
    args and kwargs are exclusive, i.e., you cannot mix positional and named
    variables.
    In positional manner, variables are saved in a tuple and loaded like that.
    If and only if a single variable is specified, it is  unpacked
    automatically.
    In named manner, they are packed in a dict, and loaded as is.
    """
    if VERBOSE:
        t0 = time.time()
        print(
            "save: '{}' ... ".format(filename),
            end="", flush=True, file=sys.stderr)
    if args and kwargs:
        raise ValueError("Positional and keyword arguments cannot be mixed.")
    if args:
        if len(args) == 1:
            # Single object, tuple is extracted.
            data = pickle.dumps(args[0])
        else:
            data = pickle.dumps(args)
    elif kwargs:
        data = pickle.dumps(kwargs)
    else:
        raise NotImplementedError
    with open(filename, "wb") as f:
        for i in range(0, len(data), BLOCK_SIZE):
            f.write(data[i:i+BLOCK_SIZE])
    if VERBOSE:
        t1 = time.time()
        print(f"done (elapsed: {t1 - t0:g} s).", file=sys.stderr)


def load(filename: str):
    """Load objects from a file using pickle.

    Parameters
    ==========
    filename: str
        File name to be loaded.

    Returns
    =======
    variable1, variable2, ...: tuple of Any
        This is returned when variables were specified and saved in positional
        manner. If there were only one variable in the file, it is unpacked and
        no tuple is returned.
    variables: dict[str, Any]
        This is returned when variables were specified and saved in named
        manner. You can restore variables in the workspace by
        ```
        locals().update(load(filename))
        ```
    """
    if VERBOSE:
        t0 = time.time()
        print(
            "load: '{}' ... ".format(filename),
            end="", flush=True, file=sys.stderr)
    ans = pickle.load(open(filename, "rb"))
    if VERBOSE:
        t1 = time.time()
        print(f"done (elapsed: {t1 - t0:g} s).", file=sys.stderr)
    return ans
