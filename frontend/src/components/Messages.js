import React, { Component } from 'react';

class Messages extends Component {
    render() {
        const {messages} = this.props;
        return (
            <ul className="Message-list">
                {messages.map(m => this.renderMsg(m))}
            </ul>
        );
    }

    renderMsg(msg) {
        const {member, text} = message;
        const {curMember} = this.props;
        const myMsg = member.id ===curMember.id;
        const className = myMsg ?  "Messages-message currentMember" : "Messages-message";
        return (
            <li className={className}>
                <span className="avatar" style={{backgroundColor: member.clientData.color}}/>
                <div className="Message-content">
                    <div className="username">
                        {member.clientData.username}
                    </div>
                    <div className="text">{text}</div>
                </div>
            </li>
        )
    }
}

export default Messaages;