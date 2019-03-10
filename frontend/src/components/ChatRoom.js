import React from 'react';
import Header from './Header';
import Messages from './Messages';
import Input from './Input';

class ChatRoom extends React.Component {
    render() {
        return (
            <div className="ui container">
                {/* <Header/>
                <Messages 
                messages={this.state.messages}
                currentMember={this.state.member}
                /> */}
                <Messages/>
                <Input/>
            </div>
        );
    }
}

export default ChatRoom;