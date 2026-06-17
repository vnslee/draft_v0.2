"""단위·통화 정규화 — 유사도 엔진이 수치 비교 전에 호출"""
from __future__ import annotations


# USD 기준 환율 테이블 (2025 기준 고정값, 정기 업데이트 필요)
_FX_TO_USD: dict[str, float] = {
    "USD": 1.0,
    "KRW": 1 / 1350.0,
    "EUR": 1.08,
    "INR": 1 / 84.0,
    "VND": 1 / 25000.0,
    "IDR": 1 / 15800.0,
    "MYR": 1 / 4.7,
    "THB": 1 / 35.0,
    "PHP": 1 / 57.0,
    "BRL": 1 / 5.1,
    "MXN": 1 / 17.5,
    "PLN": 1 / 4.0,
    "GBP": 1.27,
    "AUD": 0.65,
}


def to_usd(value: float, currency: str) -> float | None:
    rate = _FX_TO_USD.get(currency.upper())
    if rate is None:
        return None
    return value * rate


def normalize_pair(a: float, b: float, currency_a: str = "USD", currency_b: str = "USD") -> tuple[float, float] | None:
    """두 수치를 동일 통화(USD)로 정규화. 실패 시 None 반환."""
    na = to_usd(a, currency_a)
    nb = to_usd(b, currency_b)
    if na is None or nb is None:
        return None
    return na, nb


def normalize_rate(value: float) -> float:
    """비율값을 0~1 범위로 정규화 (입력이 % 형태인 경우 0.01 곱)."""
    if value > 1.0:
        return value / 100.0
    return value
