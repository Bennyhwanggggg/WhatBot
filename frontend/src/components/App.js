import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import { connect } from 'react-redux';
import Header from './Header';
import ChatRoom from './ChatRoom';

import history from '../history';
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
    // Add login page to route later
    return (
      <div className="App">
        <Router history={history}>
          <div>
            <Header/>
            <Switch>
              <Route path="/" exact component={ChatRoom} />
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

export default App;

