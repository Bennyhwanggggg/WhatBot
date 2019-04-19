import React from 'react';
import { connect } from 'react-redux';
import ScrollableFeed from 'react-scrollable-feed';
import uuid from 'uuid'

class Messages extends React.Component {

    renderText = (txt) => {
        return txt.split('\n').map((t) => {
            return (
                <React.Fragment key={uuid.v4()}>{t}<br/></React.Fragment>
            )
        })
    } 

    renderMessages() {
        var messageList = this.props.messages.map( msgList => msgList.filter( message => {
            return message.message !== 'loading'
        }))
        var loadingMessages = this.props.messages.map( msgList => msgList.filter( message => {
            const isUser = message.inputValue != null;
            return !isUser && message.message === 'loading'
        }))
        if (loadingMessages[0].length) {
            messageList[0] = messageList[0].concat(loadingMessages[0][0])
        }
        return messageList.map( msgList => msgList.map( message => {
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
                            <div className="text">{this.renderText(msg)}</div>
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