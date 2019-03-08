import React from 'react';
import Header from './Header';
import Messages from './Messages';
import Input from './Input';
import './App.css';

function randomColor() {
  return '#' + Math.floor(Math.random() * 0xFFFFFF).toString(16);
}

class App extends React.Component {
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

export default App;
