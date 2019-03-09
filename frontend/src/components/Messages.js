import React, { Component } from 'react';

class Messages extends Component {
    render() {
        const {messages} = this.props;
        if (messages){
            return (
                <ul className="Messages-list">
                    {messages.map(m => this.renderMsg(m))}
                </ul>
            );
        } else {
            return (
                <ul className="Messages-list">
                </ul>
            );
        }
    }

    renderMsg(message) {
        const {member, text} = message;
        const {currentMember} = this.props;
        const messageFromMe = currentMember.username === member.username;
        const className = messageFromMe ?  "Messages-message currentMember" : "Messages-message";
        return (
            <li className={className}>
                <span className="avatar" 
                style={{backgroundColor: member.color}}/>
                <div className="Message-content">
                    <div className="username">
                        {member.username}
                    </div>
                    <div className="text">{text}</div>
                </div>
            </li>
        )
    }
}

export default Messages;