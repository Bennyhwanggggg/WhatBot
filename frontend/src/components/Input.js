import React, {Component} from 'react';
import { Field, reduxForm } from 'redux-form';


// redux-form #224, redux-form.com for docs
class Input extends Component {

    renderInput({input}) {
        return (
            <div>
                <input {...input}/>
                <button>Send</button>
            </div>
        );
    };

    render() {
        return (
            <div className="Input">
                <form>
                    <Field name="inputValue" 
                        component={this.renderInput} 
                        placeholder="Enter message here and press ENTER to send"
                    />
                </form>
            </div>
        );
    }

    /* Events */
    onChange = (e) => {
        this.setState({text: e.target.value});
    }

    onSubmit = (formValues) => {
        // e.preventDefault(); // Prevent default so it doesn't refresh
        console.log(formValues);
        this.setState({text: ""});
        this.props.onSendMessage(formValues);
    }
}

export default reduxForm({
    form: formValues
})(Input);