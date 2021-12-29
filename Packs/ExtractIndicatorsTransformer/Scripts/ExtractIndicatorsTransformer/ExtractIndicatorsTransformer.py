from typing import Text
import demistomock as demisto
from CommonServerPython import *


def filter_types(extracted_indicators: Dict[str, Dict], indicators_types: Text) -> Dict[str, Dict]:
    list(map(lambda x: x.lower(), argToList(indicators_types)))
    return {ind_type: ind_values for ind_type,
            ind_values in extracted_indicators.items() if ind_type.lower() in indicators_types}


def main():
    try:
        args = demisto.args()
        extracted_indicators = json.loads(execute_command('extractIndicators', {'text': args.get('value', '')}))
        extart_types = args.get('indicator_type')
        if extart_types:
            extracted_indicators = filter_types(extracted_indicators, extart_types)
        demisto.setContext(args.get('context_path', 'ExtractedIndicators'), extracted_indicators)
        demisto.results(extracted_indicators)
    except Exception as error:
        return_error(str(error), error)


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
