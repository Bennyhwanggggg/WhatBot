import React, { Component } from 'react';

class Messages extends Component {
    render() {
        const {messages} = this.props;
        return (
            <ul className="message-list">
                {messages.map(m => this.renderMessage(m))}
            </ul>
        );
    }
}

export default Messaages;