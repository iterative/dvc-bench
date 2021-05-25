import json
import os
from pathlib import Path
from string import Template


def get_default_config():
    base_path = Path(__file__).parent.parent
    return base_path / "configs" / "basic.json"


def get_config(path):
    with open(path) as stream:
        template = Template(stream.read())

    try:
        source = template.substitute(os.environ)
    except KeyError as key_error:
        [key] = key_error.args
        raise ValueError(f"Missing configuration value: {key}") from key_error
    else:
        return json.loads(source)


config = get_config(os.getenv("DVC_BENCH_CONFIG", get_default_config()))
