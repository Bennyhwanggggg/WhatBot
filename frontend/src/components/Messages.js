import React, { Component } from 'react';
import { connect } from 'react-redux';


class Messages extends Component {

    renderMessages() {
        return this.props.messages.map( message => {
            const isUser = message.inputValue != null;
            const currentMember = isUser ?  "Messages-message currentMember" : "Messages-message";
            const currentMemberColor = isUser ? "blue" : "red";
            const currentUserName = isUser ? "You" : "WhatBot";
            const msg = isUser ? message.inputValue : message.message;
            return (
                <li className={currentMember} key={message.id}> 
                    <span className="avatar" 
                    style={{backgroundColor: {currentMemberColor}}}/>
                    <div className="Message-content">
                        <div className="username">
                            {currentUserName}
                        </div>
                        <div className="text">{msg}</div>
                    </div>
                </li>
            )
        });
    }

    render() {
        return (
            <ul className="Messages-list">
                {this.renderMessages()}
            </ul>
        );  
    }
    // // get list of message from redux store?
    // renderMsg(message) {
    //     const {member, text} = message;
    //     const {currentMember} = this.props;
    //     const messageFromMe = currentMember.username === member.username;
    //     const className = messageFromMe ?  "Messages-message currentMember" : "Messages-message";
    //     return (
    //         <li className={className}>
    //             <span className="avatar" 
    //             style={{backgroundColor: member.color}}/>
    //             <div className="Message-content">
    //                 <div className="username">
    //                     {member.username}
    //                 </div>
    //                 <div className="text">{text}</div>
    //             </div>
    //         </li>
    //     )
    // }
}

const mapStateToProps = (state) => {
    return {messages: Object.values(state.messages) }
}

export default connect(mapStateToProps)(Messages);