import React from 'react';
import { Link } from 'react-router-dom';
import Modal from './Modal';
import history from '../history';
import Markdown from 'react-markdown';

class TrainUsageInfo extends React.Component {
    
    renderActions() {
        return (
            <React.Fragment>
                <button className="ui button"><Link to="/upload" className="ui button">Close</Link></button>
            </React.Fragment>
        );
    }

    renderContent() {
        var src = "#### Intents\nIntents training data should have the following lines:\n`display_name` : The name of the intent. If an intent is expected to have a follow up, it should end with `_with_follow_up`.\n`message_texts` : How the intent should respond. If returning multiple entities, each field should be separated by ` @@@ `. e.g `$course @@@ $time`\n`intent_type` : The type of intent. This should match a key in `self.intent_entity_map` and is an indication of what type of entities will be inside the intent.\n`reset_contexts`: If an intent is to mark an end of a conversation, this line should be present.\n`parent_followup`: If an intent is a followup intent, this field should specify the name of the intent it is following up from.\n`input_context`: If context is required for an intent, this field should be the context name of the context it is getting values from, which is another intent's `output context`.\n`output_context`: If the intent is outputing information for another intent to use, this is used. Followup context have to follow the format of ending with `-followup`.\n`action`: Used to create an action. This is required for passing value between contexts. `action` has to follow the format of `{parent_followup}.{followup_intent_name}`\nNotes:\n- The entities inside data themselves should also be wrapped with curly brackets `{}`.\n- Context is only required if you want to pass information from an intent to another.\n\nBasic example (An intent with no followup and context):\n```\ndisplay_name course_fee_queries\nmessage_texts $course\nintent_types course_fee\nreset_contexts\nHow much does {course code} cost?\nHow much does {course code} cost to do?\nWhat is the cost of {course code}?\n```\nAdvance example (An intent with followup but no context):\nParent intent\n```\ndisplay_name course_fee_queries_with_followup\nmessage_texts Sure! What is the course code of the course you want to know course fee for?\nintent_types course_fee\noutput_context course_fee_queries_with_followup-followup\nI want to find out the course fee for a course\nI have a question about course fee\n```\nFollowup intent\n```\ndisplay_name course_fee_queries_with_followup-user_input_course_code\nmessage_texts $course\nintent_types course_fee\nparent_followup course_fee_queries_with_followup\ninput_context course_fee_queries_with_followup-followup\nreset_contexts\n{course code}\n{course code} please\n```\n\nAdvance example (An intent with followup and context):\nParent intent to trigger context (May not be necessary depending on your usage case, but this example aims to show a case where you want to just output an context initially in an intent).\n```\ndisplay_name consultation_booking_with_followup\nmessage_texts Sure! What is the course code of the course you would like to book it for? Also, what time and date?\nintent_types consultation_booking\noutput_context consultation_booking_with_followup-followup\nI want to book a consultation\n```\nFollowup intent that takes in the context to recognize the situation and output the information it gets\n```\ndisplay_name consultation_booking_with_followup-user_input_course_code_with_followup\nmessage_texts Sure! Please tell me which date and time you would like to book a course consultation for $course.\nintent_types consultation_booking\nparent_followup consultation_booking_with_followup\ninput_context consultation_booking_with_followup-followup\noutput_context consultation_booking_with_followup-user_input_course_code_with_followup-followup\naction consultation_booking_with_followup.consultation_booking_with_followup-user_course_code_with_followup\n{course code}\n{course code} please\n```\nFinal followup that retrieves missing information that user didn't provide and also gather information from the previous followup's context\n```\ndisplay_name consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date\nmessage_texts #consultation_booking_with_followup-user_input_course_code_with_followup-followup.course  @@@ $time @@@ $date\nintent_types consultation_booking\nparent_followup consultation_booking_with_followup-user_input_course_code_with_followup\ninput_context consultation_booking_with_followup-user_input_course_code_with_followup-followup\naction consultation_booking_with_followup.consultation_booking_with_followup-user_course_code_with_followup\nreset_contexts\nI want to book on {date} at {time}\n{time} {date}\n```\n\n#### Entities\nThe first line of any entities training data should be the name of the entity and all following lines are the data themselves. If an entity has a synonym, it should be separated with `@@@` on the same line.\n\nFor example:\n```\ncourse\nCOMP6441@@@Security Engineering and Cyber Security\nCOMP9020@@@Foundations of Computer Science\nCOMP9021@@@Principles of Programming\nCOMP9032@@@Microprocessors and Interfacing\nCOMP9311@@@Database Systems\n```"
        return (
            <Markdown source={src} />
        )
    }

    render() {
        return (
            <Modal
                title="How to train"
                content={this.renderContent()}
                actions={this.renderActions()}
                onDismiss={() => history.push('/upload')}
            />
        );
    }
}

export default TrainUsageInfo;