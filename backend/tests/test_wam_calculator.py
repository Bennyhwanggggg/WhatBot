from utility_module.WamCalculator import WamCalculator

def test_wam_calculation():
    wam = WamCalculator()
    result = wam.calculate_wam("z8888888")

    expected = 'Course name: COMP6441\n' \
               'Number of credits: 6\n' \
               'Result: 85.0\n' \
               'Course name: COMP9020\n' \
               'Number of credits: 6\n' \
               'Result: 95.0\n' \
               'Course name: COMP9021\n' \
               'Number of credits: 6\n' \
               'Result: 99.0\n' \
               'Course name: COMP9032\n' \
               'Number of credits: 6\n' \
               'Result: 67.0\n' \
               'Course name: COMP9311\n' \
               'Number of credits: 6\n' \
               'Result: 77.0\n' \
               'Course name: COMP9414\n' \
               'Number of credits: 6\n' \
               'Result: 66.0\n' \
               'Course name: COMP9814\n' \
               'Number of credits: 6\n' \
               'Result: 86.0\n' \
               'Course name: COMP9511\n' \
               'Number of credits: 6\n' \
               'Result: 74.0\n' \
               'Wam is: 81.1\n' \
               'Grade is: D'


    assert expected == result
