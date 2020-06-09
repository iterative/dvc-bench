import copy
import hashlib
import json
import os
import sys

from asv.machine import Machine, MachineCollection


def floor_nearest(x, floor):
    return x // floor * floor


def write_machine_info():
    # Hack making sure that similar machines will have same name, so that
    # we can reuse results from previous runs.
    if os.path.exists(MachineCollection.get_machine_file_path()):
        os.remove(MachineCollection.get_machine_file_path())

    machine_info = Machine.get_defaults()
    # floor to tolerate small fluctuations in RAM between runners
    if machine_info["ram"]:
        machine_info["ram"] = str(floor_nearest(int(machine_info["ram"]), 100))

    machine_marker = copy.copy(machine_info)
    del machine_marker["machine"]

    marker_str = json.dumps(machine_marker, sort_keys=True)
    suffix = hashlib.md5(marker_str.encode("utf-8")).hexdigest()[:7]

    machine_name = "{}_{}".format(sys.platform, suffix)
    machine_info["machine"] = machine_name

    MachineCollection.save(machine_name, machine_info)


if __name__ == "__main__":
    write_machine_info()
