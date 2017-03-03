#!/usr/bin/python3

# Either download the API courses list from https://incubator.duolingo.com/api/1/courses/list
# and run the script with the file as the first argument
# or run it with no arguments and it will try to download the course data automatically

# If you are going to try out the filtering options, then go easy on Duo's API.
# Download the data and then use it locally
# ./duo_to_graphviz.py --download > list
# ./duo_to_graphviz.py list <options>

# for more options run: ./duo_to_graphviz.py -h

# use results with graphviz: ./duo_to_graphviz.py | circo -Tpng -o courses.png

from requests import get
from collections import namedtuple
from json import load

Language = namedtuple('Language', ['phase', 'source', 'dest'])

def download_api_data():
    return get('https://incubator.duolingo.com/api/1/courses/list')

def get_api_data():
    fp = download_api_data()
    return fp.json()

def get_file_data(f):
    with open(f) as fp:
      data = load(fp)
    return data

def filter_phases(data, phases):

    course_data = filter(lambda cd: cd.phase in phases, data)
    return course_data

def filter_languages(data, languages, filter_arg, source_or_dest):

    include = [l for l in filter_arg if l[0] != '~']
    exclude = [l[1:] for l in filter_arg if l[0] == '~']

    course_data = filter(lambda cd: 
                             (len(include) == 0 or languages[getattr(cd, source_or_dest)].upper() in include) and
                              languages[getattr(cd, source_or_dest)].upper() not in exclude,
                             data)
    return course_data

def parse_json(data):

    course_data = [Language(direction['phase'],direction['from_language_id'],direction['learning_language_id'])
                        for direction in data['directions']]
    return course_data

def produce_graph(course_data, languages, colours):

    courses = {}
    for course in sorted(course_data):
        if course.phase not in courses:
            courses[course.phase] = {}
        if course.source not in courses[course.phase]:
            courses[course.phase][course.source] = []
        courses[course.phase][course.source].append(course.dest)

    print('digraph G {')
    print('  rankdir=LR;')
    print('  overlap=false;')

    for (phase,sources) in courses.items():
        print('\n  edge [color={}]'.format(colours[phase]))

        for (source, dests) in sorted(sources.items()):
            print('  "{}" -> {{ '.format(languages[source]), end='')

            for dest in sorted(dests):
                print('"{}" '.format(languages[dest]), end='')

            print('};')
    print('}')

def diff_courses(courses, old_courses):
    return [language for language in courses if language not in old_courses]

def get_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Process Duolingo course data into a dot file for graphviz')
    parser.add_argument('filename', nargs='?', help='Name of the file with the Duolingo course data. Requests current data from the Duolino API if ommitted')
    parser.add_argument('-s', '--source_language', nargs='*', default='', type=str, help='Filter to only show courses from the SOURCE_LANGUAGE. Prefix with a "~" to exclude the language instead')
    parser.add_argument('-d', '--dest_language', nargs='*', default='', type=str, help='Filter to only show courses to the DEST_LANGUAGE. Prefix with a "~" to exclude the language instead')
    parser.add_argument('-p', '--phase', nargs='*', type=int, default=[1,2,3], choices=[1,2,3], help='Only show courses in the selected phase(s)')
    parser.add_argument('--download', default='', action='store_const', const='Y', help='Download and display the API data for easy output to a file')
    parser.add_argument('-c', '--colours', nargs=3, metavar='COLOUR', type=str, default=['red','yellow','green'], help='Choose alternate colours for phase 1, 2 and 3')
    parser.add_argument('--diff', nargs=1, metavar='<FILENAME>', type=str, default='', help='Only display the differences vs a previous downloaded file of data')
    return parser.parse_args()

def main():
    args = get_arguments()

    if args.download == 'Y':
        print(download_api_data().text)
        return

    if not args.filename:
      data = get_api_data()
    else:
      data = get_file_data(args.filename)

    languages = {code:details['name'] for (code,details) in data['languages'].items()}

    course_data = parse_json(data)

    if args.diff:
        diff_data = parse_json(get_file_data(args.diff[0]))
        course_data = diff_courses(course_data, diff_data)

    if args.phase:
        course_data = filter_phases(course_data, args.phase)

    if args.source_language:
        course_data = filter_languages(course_data,
                            languages,
                            list(map(str.upper, args.source_language)),
                            'source')

    if args.dest_language:
        course_data = filter_languages(course_data,
                            languages,
                            list(map(str.upper, args.dest_language)),
                            'dest')

    colours = {phase:colour for (phase, colour) in zip([1,2,3], args.colours)}

    produce_graph(course_data, languages, colours)

if __name__ == '__main__':
    main()
