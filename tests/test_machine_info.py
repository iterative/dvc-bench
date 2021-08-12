import hashlib
import json
import sys

import pytest
from asv.machine import Machine, MachineCollection
from write_asv_machine import floor_nearest, write_machine_info


@pytest.mark.parametrize("ram, expected_ram", [("98765", "98700"), ("", "")])
def test_write_asv_machine(mocker, ram, expected_ram):
    mocker.patch.object(
        Machine,
        "get_defaults",
        return_value={
            "ram": ram,
            "machine": "machine_name",
            "other_info": "other_info",
        },
    )

    expected_name = "{}_{}".format(
        sys.platform,
        hashlib.md5(
            json.dumps(
                {"ram": expected_ram, "other_info": "other_info"},
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:7],
    )

    save_mock = mocker.patch.object(MachineCollection, "save")
    write_machine_info()

    assert save_mock.call_args == mocker.call(
        expected_name,
        {
            "ram": expected_ram,
            "machine": expected_name,
            "other_info": "other_info",
        },
    )


@pytest.mark.parametrize(
    "x, floor, expected_result",
    [(199, 100, 100), (101, 100, 100), (99, 100, 0)],
)
def test_floor_nearest(x, floor, expected_result):
    assert floor_nearest(x, floor) == expected_result
