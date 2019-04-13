import React from 'react';
import { Link } from 'react-router-dom';
import { signOut } from '../actions';

class Header extends React.Component {

    logout = () => {
        this.props.signOut();
    }

    renderAdmin() {
        // TODO: update logout
        return (
            <div className="ui pointing menu App-header">
                <div className="header item">
                    <Link to="/chatroom">
                        WhatBot
                    </Link>
                </div>
                <div className="item">
                    <Link to="/upload">
                        Upload training data
                    </Link>
                </div>
                <div className="item">
                    <Link to="/dashboard">
                        Dashboard
                    </Link>
                </div>
                <div className="right item">
                    <Link to="/login" onClick={this.logout}>
                        Logout
                    </Link>
                </div>
            </div>
        );
    }

    renderStudent() {
        // TODO: update logout
        return (
            <div className="ui pointing menu App-header">
                <div className="header item">
                    <Link to="/chatroom">
                        WhatBot
                    </Link>
                </div>
                <div className="right item">
                    <Link to="/login" onClick={this.logout}>
                        Logout
                    </Link>
                </div>
            </div>
        );
    }

    renderDefault() {
        // TODO: check how to handle this
        return (
            <div className="ui pointing menu App-header">
                <div className="header item">
                    <Link to="/">
                        WhatBot
                    </Link>
                </div>
                <div className="right item">
                    <Link to="/login">
                        Login
                    </Link>
                </div>
            </div>
        );
    }
    
    render () {
        if (this.props.isSignedIn && this.props.accessLevel === 'admin') {
            return this.renderAdmin();
        } else if (this.props.isSignedIn && this.props.accessLevel === 'student') {
            return this.renderStudent();
        } else {
            return this.renderDefault();
        }
    }
};

const mapStateToProps = (state) => {
    return { 
        isSignedIn: state.auth.isSignedIn,
        userId: state.auth.userId,
        accessLevel: state.auth.accessLevel
    }
}

export default connect(
    mapStateToProps,
    {signOut}
)(Header);