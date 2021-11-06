def header_option():
    return {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*'}


def check_session(header):
    session = header.get('session') or header.get('Session')
    if session:
        return session
