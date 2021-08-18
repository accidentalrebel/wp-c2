is_debug = False

def log_print(msg, level):
    global is_debug
    if not is_debug and level > 1:
        return

    print(msg)
