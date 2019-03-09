import React, {Component} from 'react';
import { Field, reduxForm } from 'redux-form';

class Input extends Component {
    state = {
        text: ""
    }

    render() {
        return (
            <div className="Input">
                <form onSubmit={e => this.onSubmit(e)}>
                    <input
                        onChange={e => this.onChange(e)}
                        value={this.state.text}
                        type="text"
                        placeholder="Enter message here and press ENTER to send"
                        autoFocus={true}
                    />
                    <button>Send</button>
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

export default Input;