import React, { Component } from 'react';
import MessageList from './components/MessageList';
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
