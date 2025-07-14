import os
import sys
import types
import pytest
from unittest import mock


# Patch imports for MasterController and SlaveController
@pytest.fixture(autouse=True)
def patch_controllers(monkeypatch):
    master_mock = mock.MagicMock(name="MasterController")
    slave_mock = mock.MagicMock(name="SlaveController")
    monkeypatch.setitem(
        sys.modules, "src.master", types.SimpleNamespace(MasterController=master_mock)
    )
    monkeypatch.setitem(
        sys.modules, "src.slave", types.SimpleNamespace(SlaveController=slave_mock)
    )
    monkeypatch.setitem(
        sys.modules,
        "src.controller",
        types.SimpleNamespace(MasterController=master_mock, SlaveController=slave_mock),
    )
    yield
    monkeypatch.delitem(sys.modules, "src.master")
    monkeypatch.delitem(sys.modules, "src.slave")
    monkeypatch.delitem(sys.modules, "src.controller")


@mock.patch.dict(os.environ, {"ROLE": "master"})
def test_main_master(monkeypatch):
    import src.main as main

    monkeypatch.setattr(main, "MasterController", mock.MagicMock())
    monkeypatch.setattr(main, "SlaveController", mock.MagicMock())
    main.ROLE = "master"
    main.CONFIG = {}
    main.main()
    main.MasterController.assert_called()


@mock.patch.dict(os.environ, {"ROLE": "slave", "MASTER_IP": "1.2.3.4"})
def test_main_slave(monkeypatch):
    import src.main as main

    monkeypatch.setattr(main, "MasterController", mock.MagicMock())
    monkeypatch.setattr(main, "SlaveController", mock.MagicMock())
    main.ROLE = "slave"
    main.MASTER_IP = "1.2.3.4"
    main.CONFIG = {}
    main.main()
    main.SlaveController.assert_called()


@mock.patch.dict(os.environ, {"ROLE": "slave"})
def test_main_slave_no_master_ip(monkeypatch):
    import src.main as main

    monkeypatch.setattr(main, "MasterController", mock.MagicMock())
    monkeypatch.setattr(main, "SlaveController", mock.MagicMock())
    main.ROLE = "slave"
    main.MASTER_IP = None
    main.CONFIG = {}
    with pytest.raises(
        ValueError,
        match="MASTER_IP environment variable or config is required for slave role",
    ):
        main.main()


@mock.patch.dict(os.environ, {"ROLE": "foobar"})
def test_main_unknown_role(monkeypatch):
    import src.main as main

    monkeypatch.setattr(main, "MasterController", mock.MagicMock())
    monkeypatch.setattr(main, "SlaveController", mock.MagicMock())
    main.ROLE = "foobar"
    main.CONFIG = {}
    with pytest.raises(ValueError, match="Unknown ROLE: foobar"):
        main.main()
