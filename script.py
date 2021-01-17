import os
import uvicorn


def dev() -> None:
    uvicorn.run(
        "src.main:app", workers=1, host="0.0.0.0", port=9000, reload=True
    )


def test() -> None:
    os.system("pytest tests")


def test_with_coverage() -> None:
    os.system("pytest --cov tests")