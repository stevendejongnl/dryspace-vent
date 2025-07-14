import os
from src.master import MasterController
from src.slave import SlaveController

ROLE = os.getenv("ROLE", "master")  # 'master' or 'slave'
MASTER_IP = os.getenv("MASTER_IP", None)


def main():
    if ROLE == "master":
        controller = MasterController()
        controller.run()
    elif ROLE == "slave":
        if not MASTER_IP:
            raise ValueError(
                "MASTER_IP environment variable is required for slave role"
            )
        controller = SlaveController(MASTER_IP)
        controller.run()
    else:
        raise ValueError("Unknown ROLE: {}".format(ROLE))


if __name__ == "__main__":
    main()
