import React from 'react';
import Header from './Header';
import Messages from './Messages';
import Input from './Input';

class ChatRoom extends React.Component {
    render() {
        return (
            <React.Fragment>
                <Messages/>
                <Input/>
            </React.Fragment>
        );
    }
}

export default ChatRoom;