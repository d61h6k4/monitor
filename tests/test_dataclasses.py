
import datetime
import monitor.dataclasses


LOG_LINES = [
    '127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 123',
    '127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 234',
    '127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 200 34',
    '127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "POST /api/user HTTP/1.0" 503 12',
]


def test_http_access_log_parser():
    assert monitor.dataclasses.W3CHTTPAccessLog.from_string(LOG_LINES[0]) == monitor.dataclasses.W3CHTTPAccessLog('127.0.0.1', '-', 'james', datetime.datetime(2018, 5, 9, 16, 00, 39, tzinfo=datetime.timezone.utc), monitor.dataclasses.Request("GET", monitor.dataclasses.URI("report", "/report"), "HTTP/1.0"), 200, 123)
