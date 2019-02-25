import React, { Component } from 'react';
import Messages from "./components/Messages";
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
