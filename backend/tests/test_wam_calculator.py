from utility_module.WamCalculator import WamCalculator


def test_wam_calculation():
    wam = WamCalculator()
    result = wam.calculate_wam("z1234567")

    expected = 'Course name: COMP6441\n' \
               'Number of credits: 6\n' \
               'Result: 95.0\n' \
               'Course name: COMP9020\n' \
               'Number of credits: 6\n' \
               'Result: 98.0\n' \
               'Course name: COMP9021\n' \
               'Number of credits: 6\n' \
               'Result: 100.0\n' \
               'Course name: COMP9032\n' \
               'Number of credits: 6\n' \
               'Result: 78.0\n' \
               'Course name: COMP9311\n' \
               'Number of credits: 6\n' \
               'Result: 88.0\n' \
               'Course name: COMP9414\n' \
               'Number of credits: 6\n' \
               'Result: 66.0\n' \
               'Course name: COMP9814\n' \
               'Number of credits: 6\n' \
               'Result: 79.0\n' \
               'Course name: COMP9511\n' \
               'Number of credits: 6\n' \
               'Result: 85.0\n' \
               'Wam is: 86.1\n' \
               'Grade is: D'
    assert expected == result
