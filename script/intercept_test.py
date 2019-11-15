from mitmproxy import http
from mitmproxy.script import concurrent


@concurrent
def request(flow: http.HTTPFlow) -> None:
    # /api/hrm/kq/attendanceButton/getOutButtons
    # /api/hrm/kq/attendanceButton/punchButton

    if '/api/hrm/kq/attendanceButton/' in flow.request.path:
        print('=' * 10 + flow.request.path)
        # print(flow.request.content)
        content = flow.request.content.decode('utf-8')
        content = content.replace("longitude=", "longitude=120.113035").replace("latitude=", "latitude=30.333035")
        flow.request.content = content.encode('utf-8')
        # print(flow.request.content)


@concurrent
def response(flow: http.HTTPFlow) -> None:
    if '/api/hrm/kq/attendanceButton/' in flow.request.path:
        print(flow.response.text)
