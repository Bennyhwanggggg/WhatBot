from management_module.ManagementModule import ManagementModule
import os

PATH = os.path.dirname(os.path.realpath(__file__))
INTENT_VALIDATION_TEST_DATA_PATH = os.path.join(PATH, 'intent_validation_test_data')


def test_valid_intent_files():
    management_module = ManagementModule()
    test_files = [os.path.join(INTENT_VALIDATION_TEST_DATA_PATH, file) for file in os.listdir(INTENT_VALIDATION_TEST_DATA_PATH) if 'success' in file]
    for test_file in test_files:
        result = management_module.check_intent_file_format(test_file)
        assert True == result

