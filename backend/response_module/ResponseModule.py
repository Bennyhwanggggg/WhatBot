
class ResponseModule():
    def __init__(self):
        self.queryMap = {
            'course_outline': self.respond_to_course_outline_queries
        }

    def respond(self, queryType):
        return self.queryMap[queryType]()


    def respond_to_course_outline_queries(self):
        return """
                A capstone software project. 
                Students work in teams to define, 
                implement and evaluate a real-world software system. 
                Most of the work in this course is team-based project work, 
                although there are some introductory lectures on software project management and teamwork strategies. 
                Project teams meet fortnightly with project mentors to report on the progress of the project. 
                Assessment is based on a project proposal, 
                a final project demonstration and report, 
                and on the quality of the software system 
                for more details, goto outline {url}
                """

