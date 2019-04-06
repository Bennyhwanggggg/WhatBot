# Query Module

The query module is responsible for all communication related with Dialogflow. Messages are passed into this module for it to be processed by Dialogflow such that the intent and entites detected will be returned in the response, which will be used by the response module to do further processing.

## How to train
The Dialogflow agent can be trained using the supplied data inside `training_data` folder.

To train an entity:
```
python3 train.py --retrain_entities True
```
To train an intent:
```
python3 train.py --retrain_intents True
```
To train the agent completely:
```
python3 train.py --retrain_all True
```
To train a single intent:
```
display_name, message_texts, intent_types, data = query_module_trainer.read_intents_data({Path to training data})
query_module_trainer.create_intent(display_name=display_name, message_texts=message_texts, intent_types=intent_types, training_data=data, data_is_parsed=True)
```
Note: Will throw an error if entity already exist, so make sure you call query_module_trainer.delete_intent(display_name)

To train a single entity:
```
display_name, entity_values, synonyms = query_module_trainer.read_entities_data({Path to training data})
query_module_trainer.create_entity(self, display_name=display_name, entity_values=entity_values, synonyms=synonyms)
```
Note: Will throw an error if entity already exist, so make sure you call query_module_trainer.delete_entity(display_name)

### Training data configuration
#### Intents
Intents training data should have the following lines:  
`display_name` : The name of the intent. If an intent is expected to have a follow up, it should end with `_with_follow_up`.  
`message_texts` : How the intent should respond. If returning multiple entities, each field should be separated by ` @@@ `. e.g `$course @@@ $time`  
`intent_type` : The type of intent. This should match a key in `self.intent_entity_map` and is an indication of what type of entities will be inside the intent. 
`reset_contexts`: If an intent is to mark an end of a conversation, this line should be present.  
`parent_followup`: If an intent is a followup intent, this field should specify the name of the intent it is following up from.  
`input_context`: If context is required for an intent, this field should be the context name of the context it is getting values from, which is another intent's `output context`.  
`output_context`: If the intent is outputing information for another intent to use, this is used. Followup context have to follow the format of ending with `-followup`.  
`action`: Used to create an action. This is required for passing value between contexts. `action` has to follow the format of `{parent_followup}.{followup_intent_name}`

Notes: 
- The entities inside data themselves should also be wrapped with curly brackets `{}`.  
- Context is only required if you want to pass information from an intent to another.  

Basic example (An intent with no followup and context):
```
display_name course_fee_queries
message_texts $course
intent_types course_fee
reset_contexts
How much does {course code} cost?
How much does {course code} cost to do?
What is the cost of {course code}?
```

Advance example (An intent with followup but no context):
Parent intent
```
display_name course_fee_queries_with_followup
message_texts Sure! What is the course code of the course you want to know course fee for?
intent_types course_fee
output_context course_fee_queries_with_followup-followup
I want to find out the course fee for a course
I have a question about course fee
I have a query regarding course fee
Course fee question
I want to find information about course fee
I want information for course fee
Information for course fee
Information for course fee please
Information for course fee thanks
Find information about course fee
Course fee info
Course fee info please
Course fee info thanks
```
Followup intent
```
display_name course_fee_queries_with_followup-user_input_course_code
message_texts $course
intent_types course_fee
parent_followup course_fee_queries_with_followup
input_context course_fee_queries_with_followup-followup
reset_contexts
{course code}
{course code} please
{course code} thanks
I want to get the course fee for {course code}
I want to get the course fee for {course code} thanks
I want to get the course fee for {course code} please
course fee for {course code} please
course fee for {course code} thanks
```

Advance example (An intent with followup and context):
Parent intent to trigger context (May not be necessary depending on your usage case, but this example aims to show a case where you want to just output an context initially in an intent).
```
display_name consultation_booking_with_followup
message_texts Sure! What is the course code of the course you would like to book it for? Also, what time and date?
intent_types consultation_booking
output_context consultation_booking_with_followup-followup
I want to book a consultation
I want to book a course consultation
Book course consultation
Make a course consultation booking
Book a course consultation
```
Followup intent that takes in the context to recognize the situation and output the information it gets
```
display_name consultation_booking_with_followup-user_input_course_code_with_followup
message_texts Sure! Please tell me which date and time you would like to book a course consultation for $course.
intent_types consultation_booking
parent_followup consultation_booking_with_followup
input_context consultation_booking_with_followup-followup
output_context consultation_booking_with_followup-user_input_course_code_with_followup-followup
action consultation_booking_with_followup.consultation_booking_with_followup-user_course_code_with_followup
{course code}
{course code} please
{course code} thanks
I want to book {course code}
```
Final followup that retrieves missing information that user didn't provide and also gather information from the previous followup's context
```
display_name consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date
message_texts #consultation_booking_with_followup-user_input_course_code_with_followup-followup.course  @@@ $time @@@ $date
intent_types consultation_booking
parent_followup consultation_booking_with_followup-user_input_course_code_with_followup
input_context consultation_booking_with_followup-user_input_course_code_with_followup-followup
action consultation_booking_with_followup.consultation_booking_with_followup-user_course_code_with_followup
reset_contexts
I want to book on {date} at {time}
{time} {date}
```

#### Entities
The first line of any entities training data should be the name of the entity and all following lines are the data themselves. If an entity has a synonym, it should be separated with `@@@` on the same line. 

For example:
```
course
COMP6441@@@Security Engineering and Cyber Security
COMP9020@@@Foundations of Computer Science
COMP9021@@@Principles of Programming
COMP9032@@@Microprocessors and Interfacing
COMP9311@@@Database Systems
```
