import React from 'react';
import { Router, Route, Switch } from 'react-router-dom';
import { connect } from 'react-redux';
import { checkSignedIn } from '../actions';
import Header from './Header';
import ChatRoom from './ChatRoom';
import Upload from './Upload';
import Dashboard from './Dashboard';
import TrainUsageInfo from './TrainUsageInfo';
import history from '../history';
import Login from './Login';
import './App.css';


class App extends React.Component {

    state = {
        messages: [],
        member: {
            username: "You",
            color: "#fb7f0a"
        }
    }

    componentDidMount() {
        this.props.checkSignedIn()
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
        console.log(isSignedIn, userId, accessLevel)
        return (
            <div className="App">
                <Router history={history}>
                <React.Fragment>
                    <Header/>
                    <Switch>
                        <Route path="/chatroom" exact component={ChatRoom} />
                        <Route path="/upload" exact component={Upload} />
                        <Route path="/dashboard" exact component={Dashboard} />
                        <Route path="/info" exact component={TrainUsageInfo} />
                        <Route path="/login" exact component={Login} />
                    </Switch>
                </React.Fragment>
                </Router>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    console.log(state)
    const isSignedIn = state.auth.isSignedIn;
    const userId = state.auth.userId;
    const accessLevel = state.auth.accessLevel
    return {
        isSignedIn: isSignedIn,
        userId: userId,
        accessLevel: accessLevel
    }
}

export default connect(
    mapStateToProps,
    {checkSignedIn
})(App);