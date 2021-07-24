"""Runs a set of testcases for the autocomplete exercise.

Usage:
  python test.py <path-to-test-definitions-file> <path-to-test-input-root-dir>

Test definition file is an ASCII file containing multiple test cases.
Each test case is defined as follows:

TEST: <name-of-test>
<relative-path-to-input-files-dir>
<query>
<expected-result-1>
<expected-result-2>
<expected-result-3>
<expected-result-4>
<expected-result-5>

Blank lines between tests are ignored.
EMPTY is used to denote no expected result, for example when only 3 results are
expected.

Example:

TEST: simple one word test
english/simple/
this is
This is a good day.
I am happy because this is fun.
Why do you think this difficult?
EMPTY
EMPTY

"""

import sys, getopt

#TODO
#import <YOUR_CLASS_FILE>

from typing import Sequence


class AutoComplete:

  # Runs a test.
  #
  # Initializes data with input from the directory named by absolute_input_path.
  # Runs the given query.
  #
  # Returns up to 5 results.
  def Run(self, absolute_input_path: str, query: str) -> Sequence[str]:
    # TODO replace with instatiation of your class and call to your
    #      autocomplete initialization and query methods.
    return ['wrong 0', 'wrong 1', 'wrong 2', 'wrong 3', 'wrong 4']


def BadTest(line_index, error):
  print('--------------------------')
  print('Bad test at line: ' + str(line_index + 1) + ': ' + str(error))
  sys.exit(2)


def RunTest(test_name: str, absolute_input_path: str, query: str,
            expected_results: Sequence[str]):
  print('--------------------------')
  errors = []
  auto_complete = AutoComplete()
  results = auto_complete.Run(
      absolute_input_path=absolute_input_path, query=query)
  if len(results) != len(expected_results):
    errors.append('')
    errors.append('Expected %d results, got %d' %
                  (len(expected_results), len(results)))
  else:
    for index, (expected, actual) in enumerate(zip(expected_results, results)):
      if expected != actual:
        errors.append('')
        errors.append('Wrong %d result' % index)
        errors.append('Expected: %s' % expected)
        errors.append('!=')
        errors.append('  Actual: %s' % actual)
  print('%s: %s' % ('FAIL' if errors else 'OK', test_name))
  for e in errors:
    print(e)
  print()


def RunTests(tests_dir: str, input_dir: str):
  with open(tests_dir) as t:
    lines = t.readlines()
    line_index = 0
    while line_index < len(lines):
      while line_index < len(lines) and not lines[line_index].strip():
        line_index += 1
        continue
      if line_index >= len(lines):
        break

      line = lines[line_index]
      if not line.startswith('TEST:'):
        BadTest(line_index, 'Does not start with TEST:')
      try:
        test_name = line[5:].strip()

        line_index += 1
        path_name = lines[line_index].strip()

        line_index += 1
        query = lines[line_index].strip()

        expected_results = []
        for _ in range(5):
          line_index += 1
          r = lines[line_index].strip()
          if not r:
            BadTest(line_index, 'Empty expected result')
          if r != 'EMPTY':
            expected_results.append(r)

        RunTest(
            test_name=test_name,
            absolute_input_path=input_dir + '/' + path_name,
            query=query,
            expected_results=expected_results)

        line_index += 1
      except Exception as e:
        BadTest(line_index, str(e))


def main(argv):
  _, args = getopt.getopt(argv, '')
  if len(args) != 2:
    print(
        'Usage: python test.py <path-to-test-definitions-file> <path-to-test-input-root-dir>'
    )
    sys.exit(1)
  RunTests(argv[0], argv[1])


if __name__ == '__main__':
  main(sys.argv[1:])
