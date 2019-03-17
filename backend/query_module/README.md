# Query Module

The query module is reponsible for all communication related with Dialogflow. Messages are passed into this module for it to be processed by Dialogflow such that the intent and entites detected will be returned in the response, which will be used by the response module to do further processing.

## How to train
The Dialogflow agent can be trained using the supplied data inside `training_data` folder.

To train an entity:
```
python3 train.py --retrain_entities
```
To train an intent:
```
python3 train.py --retrain_intents
```
To train the agent completely:
```
python3 train.py --retrain_all
```

Note: If just training entities and an entity being trained is currently being used by another intent, Dialogflow will throw an error, so make sure you delete that intent first.

### Training data configuration
#### Intents
Intents training data should have the following lines:
`display_name` : The name of the intent
`message_texts` : How the intent should respond
`intent_type` : The type of intent. This should match a key in `self.intent_entity_map` and is an indication of what type of entities will be inside the intent.
The entities inside data themselves should also be wrapped with curly brackets `{}`.

For example:
```
display_name course_fee_queries
message_texts $course
intent_types course_fee
How much does {course code} cost?
How much does {course code} cost to do?
What is the cost of {course code}?
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
