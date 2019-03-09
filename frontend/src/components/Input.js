import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { sendMessage } from '../actions';


// redux-form #224, redux-form.com for docs
// validation #231
class Input extends React.Component {

    renderInput = ({input}) => {
        // destructure input and load its props into input
        console.log(input)
        return (
            <div>
                <input 
                    {...input} 
                    placeholder="Enter message here and press ENTER to send"
                    autoComplete="off"
                />
                <button>Send</button>
            </div>
        );
    };

    // redux-form uses handleSubmit which already calls e.preventDefault #238 send req
    onSubmit = (formValues) => {
        console.log(formValues);
        // send message, 
        // TODO: if no value, just do nothing
        // this.setState({text: ""}); // TODO: Check this
        this.props.sendMessage(formValues);
        console.log(this.props);
    }

    render() {
        return (
            <div className="Input">
                <form onSubmit={this.props.handleSubmit(this.onSubmit)}>
                    <Field 
                        name="inputValue" 
                        component={this.renderInput} 
                    />
                </form>
            </div>
        );
    }
}

const formWrapped = reduxForm({
                        form: "formValues"
                    })(Input);

export default connect(
    null,
    { sendMessage }
)(formWrapped);