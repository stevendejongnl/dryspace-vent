def log(msg, level="INFO"):
    import time

    try:
        t = time.time()
    except Exception:
        t = "?"
    print("[{}][{}] {}".format(level, t, msg))
