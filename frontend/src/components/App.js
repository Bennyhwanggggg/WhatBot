import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import { connect } from 'react-redux';
import Header from './Header';
import ChatRoom from './ChatRoom';
import Upload from './Upload';
import Dashboard from './Dashboard';
import TrainUsageInfo from './TrainUsageInfo';
import history from '../history';
import Auth from './Auth';
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
        const { isSignedIn, userId, accessLevel } = this.props
        return (
            <div className="App">
                <Router history={history}>
                <React.Fragment>
                    <Header
                        isSignedIn={isSignedIn}
                        userId={userId}
                        accessLevel={accessLevel}
                    />
                    <Switch>
                        <Route path="/" exact component={ChatRoom} />
                        <Route path="/upload" exact component={Upload} />
                        <Route path="/dashboard" exact component={Dashboard} />
                        <Route path="/info" exact component={TrainUsageInfo} />
                        <Route path="/login" exact component={Auth} />
                    </Switch>
                </React.Fragment>
                </Router>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    const isSignedIn = state.auth.isSignedIn;
    const userId = state.auth.userId;
    const accessLevel = state.auth.accessLevel
    return {
        isSignedIn: isSignedIn,
        userId: userId,
        accessLevel: accessLevel
    }
}

export default connect(mapStateToProps)(App);