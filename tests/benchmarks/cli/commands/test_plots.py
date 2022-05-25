from textwrap import dedent


def test_plots_diff(tmp_dir, bench_dvc, dvc):
    num_points = 1000
    num_files = 50

    CODE = dedent(
        """
        import json
        import sys
        num_points=int(sys.argv[1])
        num_files=int(sys.argv[2])
        metric = [{'m':(i/num_points)**2} for i in range(0, num_points)]
        for i in range(num_files):
            with open(f'metric_{i}.json', 'w') as fd:
                json.dump(metric, fd)
        """
    )

    tmp_dir.gen("train.py", CODE)

    dvc.run(
        name=f"generate_plots",
        deps=["train.py"],
        plots=[f"metric_{i}.json" for i in range(num_files)],
        cmd=f"python train.py {num_points} {num_files}",
    )

    bench_dvc("plots", "show")

    assert (tmp_dir / "dvc_plots" / "index.html").is_file()
