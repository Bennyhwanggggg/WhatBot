import React, { Component } from 'react';
import Messages from './components/Messages';
import Input from './components/Input';
import './App.css';

function randomColor() {
  return '#' + Math.floor(Math.random() * 0xFFFFFF).toString(16);
}

class App extends Component {
  state = {
    messages: [],
    member: {
      username: "You",
      color: randomColor(),
    }
  }

  onSendMessage = (message) => {
    const messages = this.state.messages;
    messages.push({
      text: message,
      member: this.state.member
    })
    this.setState({messages: messages})
  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h1>WhatBot</h1>
        </div>
        <Messages 
          messages={this.state.messages}
          currentMember={this.state.member}
        />
        <Input
          onSendMessage={this.onSendMessage}
        />
        <p>My token = (window.token)</p>
      </div>
    );
  }
}

export default App;
