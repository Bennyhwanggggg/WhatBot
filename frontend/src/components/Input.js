import React from 'react';
import { Field, reduxForm, reset } from 'redux-form';
import { connect } from 'react-redux';
import { sendMessage } from '../actions';


// redux-form #224, redux-form.com for docs
// validation #231
class Input extends React.Component {

    renderInput = ({input}) => {
        // destructure input and load its props into input
        return (
                <input 
                    {...input} 
                    placeholder="Enter message here and press ENTER to send"
                    autoComplete="off"
                />
        );
    };

    // redux-form uses handleSubmit which already calls e.preventDefault #238 send req
    onSubmit = (formValues) => {
        // send message, 
        // TODO: if no value, just do nothing
        // this.setState({text: ""}); // TODO: Check this
        this.props.sendMessage(formValues);
        console.log(this.props);
    }

    render() {
        return (
            <div className="Input">
                <form name="Input-box" onSubmit={this.props.handleSubmit(this.onSubmit)}>
                    <Field 
                        name="inputValue" 
                        component={this.renderInput} 
                    />
                    <button>Send</button>
                </form>
            </div>
        );
    }
}

const afterSubmit = (result, dispatch) => {
    console.log("reset called");
    dispatch(reset('Input-box'));
}

const formWrapped = reduxForm({
                        form: "formValues",
                        onSubmitSuccess: afterSubmit
                    })(Input);

export default connect(
    null,
    { sendMessage }
)(formWrapped);