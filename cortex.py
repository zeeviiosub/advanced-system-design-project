import calendar
import reader
import sys

if sys.argv[1] == 'read':
    mind = reader.Reader(sys.argv[2])
    if mind.gender == 'm':
        gender = 'male'
    elif mind.gender == 'f':
        gender = 'female'
    elif mind.gender == 'o':
        gender = 'other'
    print(f'user {mind.user_id}: {mind.username}, born ' +
        calendar.month_name[mind.birth_date.month] +
        f' {mind.birth_date.day}, {mind.birth_date.year} ({gender})')
    for snapshot in mind:
        print('Snapshot from ' +
            calendar.month_name[snapshot.datetime.month] +
            f' {snapshot.datetime.day}, {snapshot.datetime.year} at ' +
            f'{snapshot.datetime.hour}:{snapshot.datetime.minute}:' +
            str(snapshot.datetime.second) +
            f'.{snapshot.datetime.microsecond // 1000} on ' +
            f'{snapshot.translation} / {snapshot.rotation} with a ' +
            f'{snapshot.color_image.height}x{snapshot.color_image.width}' +
            ' color image and a ' +
            f'{snapshot.depth_image.height}x{snapshot.depth_image.width}' +
            ' depth image.')
