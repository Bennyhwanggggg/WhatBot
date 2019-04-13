import React from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { sendMessage } from '../actions';


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

    onSubmit = (formValues) => {
        if (Object.keys(formValues).length === 0){
            return;
        }
        this.props.sendMessage(formValues, this.props.userId);
        this.props.reset();
    }

    render() {
        return (
            <div className="Input">
                <form name="Input-box" onSubmit={this.props.handleSubmit(this.onSubmit)}>
                    <Field 
                        name="inputValue" 
                        component={this.renderInput} 
                    />
                    <button className="SendMessageButton">Send</button>
                </form>
            </div>
        );
    }
}

const formWrapped = reduxForm({
                        form: "formValues"
                    })(Input);

const mapStateToProps = (state) => {
    return { 
        userId: state.auth.userId,
    }
}

export default connect(
    mapStateToProps,
    { sendMessage }
)(formWrapped);