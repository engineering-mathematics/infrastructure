"""Settings validation, env parsing and override scoping."""

from __future__ import annotations

import numpy as np
import pytest

from engg_math.core import ConfigError, Settings, configure, from_env, get_settings, override, reset


@pytest.fixture(autouse=True)
def _clean() -> None:
    reset()


def test_defaults() -> None:
    s = Settings()
    assert (s.precision, s.strict_mode, s.kappa_warning, s.kappa_error) == (
        "float64",
        False,
        1e5,
        1e7,
    )
    assert s.float_dtype == np.dtype("float64")
    assert s.complex_dtype == np.dtype("complex128")


def test_float32_maps_to_complex64() -> None:
    assert Settings(precision="float32").complex_dtype == np.dtype("complex64")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"precision": "float16"},
        {"kappa_warning": 0.0},
        {"kappa_warning": 1e8, "kappa_error": 1e7},
        {"kappa_warning": 1e5, "kappa_error": 1e5},
    ],
)
def test_invalid_settings_rejected(kwargs: dict[str, object]) -> None:
    with pytest.raises(ConfigError):
        Settings(**kwargs)  # type: ignore[arg-type]


def test_from_env_parses_all_variables() -> None:
    s = from_env(
        {
            "ENGG_MATH_PRECISION": " Float32 ",
            "ENGG_MATH_STRICT": "yes",
            "ENGG_MATH_KAPPA_WARNING": "1e3",
            "ENGG_MATH_KAPPA_ERROR": "1e6",
        }
    )
    assert s == Settings("float32", True, 1e3, 1e6)


@pytest.mark.parametrize(
    "env",
    [
        {"ENGG_MATH_STRICT": "maybe"},
        {"ENGG_MATH_KAPPA_ERROR": "lots"},
        {"ENGG_MATH_PRECISION": "f8"},
    ],
)
def test_from_env_rejects_garbage(env: dict[str, str]) -> None:
    with pytest.raises(ConfigError):
        from_env(env)


def test_from_env_false_values() -> None:
    assert from_env({"ENGG_MATH_STRICT": "off"}).strict_mode is False


def test_configure_persists_until_reset() -> None:
    configure(strict_mode=True)
    assert get_settings().strict_mode is True
    reset()
    assert get_settings().strict_mode is False


def test_configure_validates() -> None:
    with pytest.raises(ConfigError):
        configure(kappa_warning=-1.0)
    assert get_settings().kappa_warning == 1e5


def test_override_is_scoped() -> None:
    with override(strict_mode=True) as inner:
        assert inner.strict_mode
        assert get_settings().strict_mode
    assert get_settings().strict_mode is False


def test_override_nests_and_restores() -> None:
    with override(kappa_warning=10.0, kappa_error=100.0):
        with override(strict_mode=True):
            s = get_settings()
            assert (s.kappa_warning, s.strict_mode) == (10.0, True)
        assert get_settings().strict_mode is False
    assert get_settings().kappa_warning == 1e5


def test_get_settings_reads_environment_lazily(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENGG_MATH_PRECISION", "float32")
    assert get_settings().precision == "float32"
