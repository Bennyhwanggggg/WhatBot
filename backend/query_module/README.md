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
`display_name` : The name of the intent  
`message_texts` : How the intent should respond. If returning multiple entities, each field should be separated by ` @@@ `. e.g `$course @@@ $time`  
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
