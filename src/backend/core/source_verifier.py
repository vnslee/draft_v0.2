"""출처 검증 — 도메인 화이트리스트 기반 (LLM 프롬프트에 맡기지 않음)"""
from __future__ import annotations

import re
from enum import Enum
from urllib.parse import urlparse


class SourceTier(str, Enum):
    TIER1 = "TIER1"    # 공식 정부·중앙은행
    TIER2 = "TIER2"    # 신뢰할 수 있는 국제기구·리서치
    TIER3 = "TIER3"    # 기타
    BLOCKED = "BLOCKED"  # 신뢰 불가 출처


_TIER1: dict[str, list[str]] = {
    "KR": ["fsc.go.kr", "bok.or.kr", "law.go.kr", "moef.go.kr", "fss.or.kr"],
    "IN": ["rbi.org.in", "sebi.gov.in", "mca.gov.in", "indiacode.nic.in", "irda.gov.in"],
    "DE": ["bafin.de", "bundesbank.de", "gesetze-im-internet.de", "bmf.de"],
    "US": ["federalreserve.gov", "sec.gov", "consumerfinance.gov", "treasury.gov", "irs.gov"],
    "VN": ["sbv.gov.vn", "mof.gov.vn", "moj.gov.vn"],
    "ID": ["bi.go.id", "ojk.go.id", "kemenkeu.go.id"],
    "MY": ["bnm.gov.my", "sc.com.my", "treasury.gov.my"],
    "TH": ["bot.or.th", "sec.or.th", "mof.go.th"],
    "PH": ["bsp.gov.ph", "sec.gov.ph"],
    "BR": ["bcb.gov.br", "cvm.gov.br", "fazenda.gov.br"],
    "MX": ["banxico.org.mx", "cnbv.gob.mx", "sat.gob.mx"],
    "PL": ["nbp.pl", "knf.gov.pl", "mf.gov.pl"],
    "GB": ["bankofengland.co.uk", "fca.org.uk", "legislation.gov.uk"],
    "AU": ["rba.gov.au", "asic.gov.au", "legislation.gov.au"],
}

_TIER2_DOMAINS: list[str] = [
    "worldbank.org", "imf.org", "bis.org", "oecd.org",
    "ifc.org", "standardandpoors.com", "moodys.com", "fitchratings.com",
    "statista.com", "pwc.com", "deloitte.com", "kpmg.com", "ey.com",
]

_BLOCKED_PATTERNS: list[str] = [
    r"wikipedia\.org",
    r".*\.blogspot\.com",
    r".*\.wordpress\.com",
    r"reddit\.com",
    r"quora\.com",
    r"namu\.wiki",
    r".*\.tistory\.com",
]
_BLOCKED_RE = [re.compile(p) for p in _BLOCKED_PATTERNS]


def _extract_domain(url: str) -> str:
    try:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        host = parsed.netloc or parsed.path
        return host.lower().lstrip("www.")
    except Exception:
        return url.lower()


def verify_source(url: str, country_code: str | None = None) -> SourceTier:
    domain = _extract_domain(url)

    for pattern in _BLOCKED_RE:
        if pattern.match(domain):
            return SourceTier.BLOCKED

    tier1_list: list[str] = []
    if country_code:
        tier1_list = _TIER1.get(country_code.upper(), [])
    # 모든 국가 TIER1 도메인도 검사
    all_tier1 = [d for domains in _TIER1.values() for d in domains]

    for t1 in tier1_list + all_tier1:
        if domain == t1 or domain.endswith(f".{t1}"):
            return SourceTier.TIER1

    for t2 in _TIER2_DOMAINS:
        if domain == t2 or domain.endswith(f".{t2}"):
            return SourceTier.TIER2

    return SourceTier.TIER3
