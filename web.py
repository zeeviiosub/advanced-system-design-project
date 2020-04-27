import pathlib
from website import Website


website = Website()


_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''


_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''


_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''


_THOUGHT_LINE_HTML = '''
<tr>
    <td>{time}</td>
    <td>{thought}
    </td>
</tr>
'''


@website.route('/')
def index():
    users_html = []
    for user_dir in website.data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return 200, index_html


@website.route('/users/([0-9]+)')
def user(user_id):
    user_dir = pathlib.Path(f'{website.data_dir.as_posix()}/{user_id}')
    thought_lines = []
    for thoughts_file in user_dir.iterdir():
        date_time = thoughts_file.name.split('.')[0]
        date, time = date_time.split('_')
        hours, minutes, seconds = time.split('-')
        displayed_time = f'{date} {hours}:{minutes}:{seconds}'
        for thought in open(thoughts_file).read().splitlines():
            thought_line = _THOUGHT_LINE_HTML.format(time=displayed_time,
                                                     thought=thought)
            thought_lines.append(thought_line)
    thoughts = '\n'.join(thought_lines)
    user_html = _USER_HTML.format(user=user_id, thoughts=thoughts)
    return 200, user_html


def run_webserver(address, data_dir):
    website.data_dir = data_dir
    website.run(address)


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        split_str = argv[1].split(':')
        address = (split_str[0], int(split_str[1]))
        run_webserver(address, pathlib.Path(argv[2]))
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
