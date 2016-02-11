import mock
import pytest
from recheck import requirements


def assert_direct_requirements(requirements_file_lines, expected_direct_requirements):
    with mock.patch('recheck.requirements._read_lines_from_file') as mock_read_lines_from_file:
        mock_read_lines_from_file.return_value = requirements_file_lines
        requirements_parser = requirements.RequirementsParser('requirements.txt')
        assert requirements_parser.direct_requirements == expected_direct_requirements
        assert [mock.call('requirements.txt')] == mock_read_lines_from_file.call_args_list


@mock.patch('recheck.requirements._read_lines_from_file')
def test_no_direct_requirements(mock_read_lines_from_file):
    assert_direct_requirements([], set())


@mock.patch('recheck.requirements._read_lines_from_file')
def test_direct_requirements_single_file(mock_read_lines_from_file):
    assert_direct_requirements(['requests==1.3'], set(['requests']))


@mock.patch('recheck.requirements._read_lines_from_file')
def test_multiple_direct_requirements_single_file(mock_read_lines_from_file):
    assert_direct_requirements(['requests==1.3',
                                'mock==0.1'], set(['requests', 'mock']))


@mock.patch('recheck.requirements._read_lines_from_file')
def test_direct_requirements_no_version_single_file(mock_read_lines_from_file):
    assert_direct_requirements(['requests'], set(['requests']))
