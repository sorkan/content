import io
import json
from copy import deepcopy

import GetAwayUsers

import demistomock as demisto


def util_load_json(path):
    with io.open(path, mode='r', encoding='utf-8') as f:
        return json.loads(f.read())


away_user_data = util_load_json('test_data/away_user.json')


def test_script_valid(mocker):
    """
    Given:

    When:
    - Calling to GetAwayUsers Script.

    Then:
    - Ensure expected outputs are returned.

    """
    from GetAwayUsers import main
    return_results_mock = mocker.patch.object(GetAwayUsers, 'return_results')
    away_user = away_user_data
    not_away_user = deepcopy(away_user_data)
    not_away_user['isAway'] = False
    mocker.patch.object(demisto, 'executeCommand', return_value=[{'Type': '1', 'Contents': [away_user, not_away_user]}])
    main()
    command_results = return_results_mock.call_args[0][0]
    assert command_results.outputs == [{'email': '',
                                        'id': 'admin',
                                        'name': 'Admin',
                                        'phone': '+650-123456',
                                        'roles': {'demisto': ['Administrator']},
                                        'username': 'admin'}]


def test_script_invalid(mocker):
    """
    Given:

    When:
    - Calling to GetAwayUsers Script. Error during the demisto.executeCommand to getUsers.

    Then:
    - Ensure error is returned.

    """
    from GetAwayUsers import main
    error_entry_type: int = 4
    mocker.patch.object(GetAwayUsers, 'return_error')
    mocker.patch.object(demisto, 'error')
    away_user = away_user_data
    not_away_user = deepcopy(away_user_data)
    not_away_user['isAway'] = False
    mocker.patch.object(demisto, 'executeCommand',
                        return_value=[{'Type': error_entry_type, 'Contents': [away_user, not_away_user]}])
    main()
    assert GetAwayUsers.return_error.called
