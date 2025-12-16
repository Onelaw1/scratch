# NCS 기반 직무 분류 데이터
# 한국고용정보원 NCS (National Competency Standards) 기반

NCS_JOB_HIERARCHY = {
    "경영·회계·사무": {
        "code": "JG01",
        "series": {
            "인사·조직": {
                "code": "JS0101",
                "positions": [
                    {"code": "JP010101", "name": "인사"},
                    {"code": "JP010102", "name": "노무관리"},
                    {"code": "JP010103", "name": "HRD"},
                    {"code": "JP010104", "name": "채용"},
                ]
            },
            "총무·법무": {
                "code": "JS0102",
                "positions": [
                    {"code": "JP010201", "name": "총무"},
                    {"code": "JP010202", "name": "법무"},
                    {"code": "JP010203", "name": "비서"},
                ]
            },
            "재무·회계": {
                "code": "JS0103",
                "positions": [
                    {"code": "JP010301", "name": "재무"},
                    {"code": "JP010302", "name": "회계"},
                    {"code": "JP010303", "name": "세무"},
                ]
            }
        }
    },
    "금융·보험": {
        "code": "JG02",
        "series": {
            "금융": {
                "code": "JS0201",
                "positions": [
                    {"code": "JP020101", "name": "은행"},
                    {"code": "JP020102", "name": "증권·외환"},
                    {"code": "JP020103", "name": "여신·수신"},
                ]
            },
            "보험": {
                "code": "JS0202",
                "positions": [
                    {"code": "JP020201", "name": "보험영업"},
                    {"code": "JP020202", "name": "보험상품개발"},
                    {"code": "JP020203", "name": "손해사정"},
                ]
            }
        }
    },
    "교육·자연·사회과학": {
        "code": "JG03",
        "series": {
            "교육": {
                "code": "JS0301",
                "positions": [
                    {"code": "JP030101", "name": "유아교육"},
                    {"code": "JP030102", "name": "초등교육"},
                    {"code": "JP030103", "name": "중등교육"},
                    {"code": "JP030104", "name": "특수교육"},
                ]
            }
        }
    },
    "정보통신": {
        "code": "JG04",
        "series": {
            "정보기술": {
                "code": "JS0401",
                "positions": [
                    {"code": "JP040101", "name": "시스템소프트웨어개발"},
                    {"code": "JP040102", "name": "응용소프트웨어개발"},
                    {"code": "JP040103", "name": "데이터베이스"},
                    {"code": "JP040104", "name": "네트워크"},
                    {"code": "JP040105", "name": "정보보안"},
                ]
            },
            "통신": {
                "code": "JS0402",
                "positions": [
                    {"code": "JP040201", "name": "통신공학"},
                    {"code": "JP040202", "name": "통신기기"},
                ]
            }
        }
    },
    "연구개발·설계": {
        "code": "JG05",
        "series": {
            "연구개발": {
                "code": "JS0501",
                "positions": [
                    {"code": "JP050101", "name": "기초연구"},
                    {"code": "JP050102", "name": "응용연구"},
                    {"code": "JP050103", "name": "개발연구"},
                ]
            }
        }
    },
    "영업·판매": {
        "code": "JG06",
        "series": {
            "영업": {
                "code": "JS0601",
                "positions": [
                    {"code": "JP060101", "name": "영업기획"},
                    {"code": "JP060102", "name": "국내영업"},
                    {"code": "JP060103", "name": "해외영업"},
                ]
            },
            "판매": {
                "code": "JS0602",
                "positions": [
                    {"code": "JP060201", "name": "매장판매"},
                    {"code": "JP060202", "name": "방문판매"},
                ]
            }
        }
    },
    "경비·청소": {
        "code": "JG07",
        "series": {
            "경비": {
                "code": "JS0701",
                "positions": [
                    {"code": "JP070101", "name": "시설경비"},
                    {"code": "JP070102", "name": "호송경비"},
                ]
            }
        }
    }
}


def get_ncs_job_list():
    """NCS 직무 목록을 플랫 리스트로 반환"""
    jobs = []
    for group_name, group_data in NCS_JOB_HIERARCHY.items():
        for series_name, series_data in group_data["series"].items():
            for position in series_data["positions"]:
                jobs.append({
                    "group": group_name,
                    "group_code": group_data["code"],
                    "series": series_name,
                    "series_code": series_data["code"],
                    "position": position["name"],
                    "position_code": position["code"],
                    "full_path": f"{group_name} > {series_name} > {position['name']}"
                })
    return jobs


def get_job_placeholders():
    """직무 입력 필드용 플레이스홀더 생성"""
    jobs = get_ncs_job_list()
    return {
        "group_examples": list(set([j["group"] for j in jobs]))[:5],
        "series_examples": list(set([j["series"] for j in jobs]))[:5],
        "position_examples": list(set([j["position"] for j in jobs]))[:10],
    }
