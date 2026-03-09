import fire


class DebugRunner:

    def test_all(self) -> None:
        import pytest

        pytest.main(["tests/"])

    def test_e2e(self) -> None:
        import pytest

        pytest.main(["tests/e2e/"])

    def test_e2e_config(self) -> None:
        import pytest

        pytest.main(["tests/e2e/test_end2end_config.py"])

    def test_e2e_non_paired(self) -> None:
        import pytest

        pytest.main(["tests/e2e/test_end2end_non_paired_run.py"])

    def test_e2e_paired(self) -> None:
        import pytest

        pytest.main(["tests/e2e/test_end2end_paired_run.py"])

    def test_e2e_makedatabase(self) -> None:

        import pytest

        pytest.main(["tests/e2e/test_end2end_makedatabase.py"])

    def test_runners(self) -> None:
        import pytest

        pytest.main(["tests/test_runners.py"])


if __name__ == "__main__":
    fire.Fire(DebugRunner)
