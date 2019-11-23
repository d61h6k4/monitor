
import dataclasses
import datetime
import re


@dataclasses.dataclass
class URI(object):
    section: str
    page: str

    @staticmethod
    def from_string(raw_string: str) -> 'URI':
        record = raw_string.split('/')
        if len(record) < 2:
            return URI('', raw_string)
        return URI(record[1], raw_string)


@dataclasses.dataclass
class Request(object):
    method: str
    uri: URI
    version: str

    @staticmethod
    def from_string(raw_string: str) -> 'Request':
        record = raw_string.strip('"').split(' ')
        return Request(record[0], URI.from_string(record[1]), record[2])


# Regex for the common Apache log format.
PARTS = [
    r'(?P<remotehost>\S+)',             # remotehost
    r'\S+',                             # rfc931
    r'(?P<authuser>\S+)',               # authuser
    r'\[(?P<date>.+)\]',                # date %t
    r'"(?P<request>.*)"',               # request
    r'(?P<status>[0-9]+)',              # status
    r'(?P<size>\S+)'                    # size
]
PATTERN = re.compile(r'\s+'.join(PARTS)+r'\s*\Z')


@dataclasses.dataclass
class W3CHTTPAccessLog(object):
    remotehost: str
    rfc931: str
    authuser: str
    date: datetime.datetime
    request: Request
    status: int
    size: int

    @staticmethod
    def from_string(raw_string: str) -> 'W3CHTTPAccessLog':
        matched = PATTERN.match(raw_string)

        if matched:
            record = matched.groupdict()

            return W3CHTTPAccessLog(record['remotehost'],
                                    '-',
                                    record['authuser'],
                                    datetime.datetime.strptime(record['date'], '%d/%b/%Y:%H:%M:%S %z'),
                                    Request.from_string(record['request']),
                                    int(record['status']),
                                    int(record['size']))
        else:
            raise ValueError(f'Cannot create W3CHTTPAccessLog. Invalid raw string {raw_string}.')
