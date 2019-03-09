import React from 'react';
import { connect } from 'react-redux';
import Header from './Header';
import Messages from './Messages';
import Input from './Input';
import { sendMessage } from '../actions';
import './App.css';


class App extends React.Component {
  state = {
    messages: [],
    member: {
      username: "You",
      color: "#fb7f0a"
    }
  }

  onSendMessage = (message) => {
    const messages = this.state.messages;
    messages.push({
      text: message,
      member: this.state.member
    })
    this.setState({messages: messages})
    this.props.sendMessage(message)
  }

  render() {
    return (
      <div className="App">
        <Header/>
        <Messages 
          messages={this.state.messages}
          currentMember={this.state.member}
        />
        <Input
          onSendMessage={this.onSendMessage}
        />
      </div>
    );
  }
}

export default connect(
  null,
  { sendMessage }
)(App);

