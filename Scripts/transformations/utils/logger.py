from functools import wraps
import inspect
import warnings

def wrap_func_names(func):
    # Return a list of calling functions in hierarchical order.
    # Used for logging purposes.
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        _calling_func_names = list()
        try:  # Running from command line
            _calling_frame = inspect.currentframe().f_back
        except:  # Running from PowerPoint
            #print F.__name__
            print "inspect.currentframe() = ", inspect.currentframe()
            return func(*args, **kwargs)
        for i in range(0, 10):
            try: 
                name = inspect.getframeinfo(_calling_frame).function
                _calling_func_names.append(name)
                _calling_frame = (_calling_frame).f_back
            except:
                try:
                    _calling_func_names.reverse()
                except:
                    pass
                return func(str(_calling_func_names), *args, **kwargs)
    return func_wrapper

@wrap_func_names
def logger(*args):
    """Logging functions for writing Log.* messages when run from within PowerPoint
    or warnings.* messages if run from the command line
    """
    try:
        from globals import Log
        Log.Warn(str(args))
    except:
        warnings.warn(str(args))