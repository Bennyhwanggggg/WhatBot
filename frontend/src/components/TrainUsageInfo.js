import React from 'react';
import { Link } from 'react-router-dom';
import Modal from './Modal';
import history from '../history';

class TrainUsageInfo extends React.Component {
    renderActions() {
        return (
            <React.Fragment>
                <button className="ui button"><Link to="/upload" className="ui button">Close</Link></button>
            </React.Fragment>
        );
    }

    renderContent() {
        return (
            <React.Fragment>
                Training data configuration
                Intents
                Intents training data should have the following lines:
                display_name : The name of the intent. If an intent is expected to have a follow up, it should end with _with_follow_up.
                message_texts : How the intent should respond. If returning multiple entities, each field should be separated by @@@. e.g $course @@@ $time
                intent_type : The type of intent. This should match a key in self.intent_entity_map and is an indication of what type of entities will be inside the intent.
                reset_contexts: If an intent is to mark an end of a conversation, this line should be present.
                parent_followup: If an intent is a followup intent, this field should specify the name of the intent it is following up from.
                input_context: If context is required for an intent, this field should be the context name of the context it is getting values from, which is another intent's output context.
                output_context: If the intent is outputing information for another intent to use, this is used. Followup context have to follow the format of ending with -followup.
                action: Used to create an action. This is required for passing value between contexts. action has to follow the format of {'{parent_followup}'}.{'{followup_intent_name}'}

                Notes:

                The entities inside data themselves should also be wrapped with curly brackets {'{}'}.
                Context is only required if you want to pass information from an intent to another.
            </React.Fragment>
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