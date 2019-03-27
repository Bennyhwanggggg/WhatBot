from utility_module.WamCalculator import WamCalculator


def test_wam_calculation():
    courses = [
        {'course_name': 'COMP9900', 'number_of_credits': 6, 'score': 79.2},
        {'course_name': 'COMP9321', 'number_of_credits': 6, 'score': 89.0},
        {'course_name': 'COMP9415', 'number_of_credits': 6, 'score': 39.21},
        {'course_name': 'COMP9101', 'number_of_credits': 6, 'score': 92.}
    ]
    wam_calculator = WamCalculator(courses)
    result = wam_calculator.calculate_wam()
    expected = 'Course name: COMP9900\nNumber of credits: 6\nResult: 79.2\n' \
               'Course name: COMP9321\nNumber of credits: 6\nResult: 89.0\n' \
               'Course name: COMP9415\nNumber of credits: 6\nResult: 39.2\n' \
               'Course name: COMP9101\nNumber of credits: 6\nResult: 92.0\n' \
               'Wam is: 74.9\nGrade is: CR'
    assert expected == result
