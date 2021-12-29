from ExtractIndicatorsTransformer import *
import pytest


data_test_main = [
    (
        {'value': 'test@test.com'},
        '{"Email": "test@test.com", "Domain": ["test.com", "test2.com"]}',
        {"Email": "test@test.com", "Domain": ["test.com", "test2.com"]}
    ),
    (
        {'value': 'test@test.com'},
        '{"Email": "test@test.com"}',
        {"Email": "test@test.com"}
    ),
    (
        {'value': 'test@test.com', 'indicator_type': 'email'},
        '{"Email": "test@test.com", "Domain": ["test.com", "test2.com"]}',
        {"Email": "test@test.com"}
    ),
    (
        {'value': 'test@test.com', 'indicator_type': 'email', 'context_path': 'test'},
        '{"Email": "test@test.com", "Domain": ["test.com", "test2.com"]}',
        {"Email": "test@test.com"}
    ),

]


@pytest.mark.parametrize('args, command_outputs, expected_indicators', data_test_main)
def test_main(args, command_outputs, expected_indicators, mocker):
    mocker.patch.object(demisto, 'args', return_value=args)
    mocker.patch('ExtractIndicatorsTransformer.execute_command', return_value=command_outputs)
    set_context_mocker = mocker.patch.object(demisto, 'setContext')
    results_mocker = mocker.patch.object(demisto, 'results')
    main()
    set_context_mocker.assert_called_once_with(args.get('context_path', 'ExtractedIndicators'), expected_indicators)
    results_mocker.assert_called_once_with(expected_indicators)
