#!/usr/bin/env python3

import unittest
from collections import namedtuple
import duo_to_graphviz
from json import loads

class TestFilterMethods(unittest.TestCase):

    Language = namedtuple('Language', ['phase', 'source', 'dest'])
    course_data = [Language(1, 'a', 'b'),
                   Language(2, 'c', 'd'),
                   Language(2, 'e', 'f'),
                   Language(3, 'g', 'h'),
                   Language(3, 'i', 'j'),
                   Language(3, 'k', 'l')]
    languages = {'a':'ALPHA', 'b':'BETA', 'c':'KAPPA', 'd':'DELTA', 'e':'EPSILON', 'f':'FOXTROT', 'g':'GAMMA', 'h':'HARPO', 'i':'IO', 'j':'JUPITER', 'k':'KILO', 'l':'LIMA'}

    def test_filter_no_phases(self):
        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [])
        self.assertEqual(len(list(filtered_course_data)), 0)

    def test_filter_single_phases(self):
        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [1])
        self.assertEqual(len(list(filtered_course_data)), 1)

        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [2])
        self.assertEqual(len(list(filtered_course_data)), 2)

        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [3])
        self.assertEqual(len(list(filtered_course_data)), 3)

    def test_filter_multi_phses(self):
        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [1, 2])
        self.assertEqual(len(list(filtered_course_data)), 3)

        filtered_course_data = duo_to_graphviz.filter_phases(self.course_data, [1, 2, 3])
        self.assertEqual(len(list(filtered_course_data)), 6)

    def test_filter_langauges(self):
        filtered_course_data = duo_to_graphviz.filter_languages(self.course_data, self.languages, ['ALPHA'], 'source')
        self.assertEqual(len(list(filtered_course_data)), 1)

    def test_filter_out_languages(self):
        filtered_course_data = duo_to_graphviz.filter_languages(self.course_data, self.languages, ['~ALPHA'], 'source')
        self.assertEqual(len(list(filtered_course_data)), 5)

    def test_parse_json(self):
        course_data = duo_to_graphviz.parse_json(loads('{"directions":[{"num_contrib":3,"from_language_id":"tr","learner_count":{"num_learners":499553,"learner_string":"499K"},"progress":100,"phase":3,"learning_language_id":"de","id":"5b6075c9cc8c6ddfd1efd1f56724b0b2"}]}'))
        self.assertEqual(course_data[0], duo_to_graphviz.Language(3, 'tr', 'de'))

    def test_diff(self):
        old_course_data = [duo_to_graphviz.Language(3, 'ALPHA', 'BETA')]
        new_course_data = [duo_to_graphviz.Language(3, 'ALPHA', 'BETA'), duo_to_graphviz.Language(2, 'DELTA', 'KAPPA')]
        course_data = duo_to_graphviz.diff_courses(new_course_data, old_course_data)

        self.assertEqual(course_data, [duo_to_graphviz.Language(2, 'DELTA', 'KAPPA')])


if __name__ == '__main__':
    unittest.main()
