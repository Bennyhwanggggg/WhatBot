outline_url = "https://webcms3.cse.unsw.edu.au/COMP{}/19T1/outline"

q1 = {"tell me more about COMP9900",
      "what is COMP9900 about?",
      "what can I learn from COMP9900?",
      "give me the outline about COMP9900?"}

a1 = """
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


q2 = {"what is the prerequisite of COMP9900",
      "give me the the prerequisite of COMP9900?",
      "what are the conditions for enrolment?",
      "what course do I need to do prior to/before this class?", }
a2 = "Completion of at least 72 UOC towards MIT program 8543. Students must be in their final semester of study"    



def get_reply(question):
    if question in q1:
        return a1.format(url=outline_url.format(9900))
    if question in q2:
        return a2
    else:
        return "what ???"
