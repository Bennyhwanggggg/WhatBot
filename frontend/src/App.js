import React, { Component } from 'react';
import MessageList from './components/messageList';
import './App.css';

class App extends Component {
  render() {
    // constructor
    return (
      <div className="app">
        <MessageList />
      </div>
    );
  }
}

export default App;
