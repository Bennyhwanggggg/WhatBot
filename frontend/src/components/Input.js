import React, {Component} from 'react';
import { Field, reduxForm } from 'redux-form';


// redux-form #224, redux-form.com for docs
class Input extends Component {

    renderInput({input}) {
        // destructure input and load its props into input
        return (
            <div>
                <input {...input}/>
                <button>Send</button>
            </div>
        );
    };

    // redux-form uses handleSubmit which already calls e.preventDefault
    onSubmit(formValues) {
        console.log(formValues);
        // send message
        this.setState({text: ""}); // TODO: Check this
        this.props.onSendMessage(formValues); // TODO: change this to an action?
    }

    render() {
        return (
            <div className="Input">
                <form onSubmit={this.props.handleSubmit(this.onSubmit)}>
                    <Field 
                        name="inputValue" 
                        component={this.renderInput} 
                        placeholder="Enter message here and press ENTER to send"
                    />
                </form>
            </div>
        );
    }
}

export default reduxForm({
    form: formValues
})(Input);