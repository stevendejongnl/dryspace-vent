import os

ROLE = os.getenv('ROLE', 'master')  # 'master' or 'slave'
MASTER_IP = os.getenv('MASTER_IP', None)

if ROLE == 'master':
    from master import run_master

    run_master()
elif ROLE == 'slave':
    from slave import run_slave

    if not MASTER_IP:
        raise ValueError("MASTER_IP environment variable is required for slave role")
    run_slave(MASTER_IP)
else:
    raise ValueError("Unknown ROLE: {}".format(ROLE))
