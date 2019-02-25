import React, {Component} from 'react';

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
                        autoFocus="true"
                    />
                </form>
                <button>Send</button>
            </div>
        );
    }

    /* Events */
    onChange(e) {
        this.setState({text: e.target.value});
    }

    onSubmit(e) {
        e.preventDefault(); // Prevent default so it doesn't refresh
        this.setState({text: ""});
        this.props.onSendMessage(this.state.text);
    }
}

export default Input;