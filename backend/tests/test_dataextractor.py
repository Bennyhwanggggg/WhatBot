from data_extractor.DataExtractor import DataExtractor


def test_data_extractor():
    data_extractor = DataExtractor('undergraduate', 'comp3900')
    data_extractor.extract()
    result = data_extractor.details
    for key, value in result.items():
        if key == 'Title':
            assert value == "Handbook 2019 - Course - Computer Science Project - COMP3900"
        if key == 'Description':
            assert value == "A capstone software project. Students work in teams to define, " \
                            "implement and evaluate a real-world software system. Most of the work " \
                            "in this course is team-based project work, although there are some introductory " \
                            "lectures on software project management and teamwork strategies. Project teams meet " \
                            "fortnightly with project mentors to report on the progress of the project. Assessment " \
                            "is based on a project proposal, a final project demonstration and report, and on the " \
                            "quality of the software system itself. Students are also required to reflect on their " \
                            "work and to provide peer assessment of their team-mates' contributions to the project."
        if key == 'Credit':
            assert value == "6 Units of Credit"
        if key == 'Prerequisite':
            assert value == "Prerequisite: COMP1531, and COMP2521 or COMP1927, and enrolled in a BSc Computer " \
                            "Science major with completion of 120 uoc."
        if key == 'Course Outline':
            assert value == "https://www.engineering.unsw.edu.au/computer-science-engineering"
        if key == 'Faculty':
            assert value == "http://www.eng.unsw.edu.au"
        if key == 'School':
            assert value == "http://www.cse.unsw.edu.au/"
        if key == 'Offering Terms':
            assert value == "Term 1, Term 2, Term 3"
        if key == 'Campus':
            assert value == "Kensington"
        if key == 'PDF':
            assert value == "https://itq9q5ny14.execute-api.ap-southeast-2.amazonaws.com/prod/pdf?url=https:" \
                            "//www.handbook.unsw.edu.au/undergraduate/courses/2019/comp3900/"
        if key == 'Indicative contact hours':
            assert value == "10"
        if key == 'Commonwealth Supported Student':
            assert value == "$1170"
        if key == 'Domestic Student':
            assert value == "$5790"
        if key == 'International Student':
            assert value == "$5790"

