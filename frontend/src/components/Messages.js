import React, { Component } from 'react'
import { connect } from 'react-redux'
import ScrollableFeed from 'react-scrollable-feed'

class Messages extends Component {

    renderMessages() {
        return this.props.messages.map( msgList => msgList.map( message => {
            const isUser = message.inputValue != null;
            const currentMember = isUser ?  "Messages-message currentMember" : "Messages-message";
            const currentMemberColor = isUser ? "blue" : "red";
            const currentUserName = isUser ? "You" : "WhatBot";
            const msg = isUser ? message.inputValue : message.message;
            if (msg && msg !== 'loading') {
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
            } else {
                return (
                    <li className={currentMember} key={message.id}> 
                        <span className="avatar" 
                        style={{backgroundColor: {currentMemberColor}}}/>
                        <div className="Message-content">
                            <div className="username">
                                {currentUserName}
                            </div>
                            <div className="typing-indicator">
                            </div>
                        </div>
                    </li>
                )
            }
        }));
    }

    render() {
        return (
            <ScrollableFeed forceScroll={true}>
                <ul className="Messages-list">
                    {this.renderMessages()}
                </ul>
            </ScrollableFeed>
        );  
    }
}

const mapStateToProps = (state) => {
    return {messages: Object.values(state.messages) }
}

export default connect(mapStateToProps)(Messages);