import React from 'react';
import { connect } from 'react-redux';
import { signIn, signOut } from '../actions';

class Authentication extends React.Component {

    componentDidMount() {
        // TODO: FIX
        this.onAuthChange(this.state.isSignedIn); // Detect current status #219 
  }

    // this is called when authentication status changes
    // TODO: FIX  
    onAuthChange = isSignedIn => {
        if (isSignedIn) {
            this.props.signIn(); // pass in credentials here? # 217
        } else {
            this.props.signOut();
        }
    };

    // TODO: FIX
    onSignInClick = () => {
        console.log("Replace this with login api")
    };

    // TODO: FIX
    onSignOutClick = () => {
        console.log("Replace this with login api")
    };

    renderAuthButton() {
        if (this.props.isSignedIn === null) {
        return null;
        } else if (this.props.isSignedIn) {
        return (
            <button onClick={this.onSignOutClick} className="ui button">
            Sign out
            </button>
        );
        } else {
        return (
            <button onClick={this.onSignInClick} className="ui button">
            Sign in
            </button>
        );
        }
    }

    render() {
        return <div>{this.renderAuthButton()}</div>;
    }
}

const mapStateToProps = state => {
  return { isSignedIn: state.isSignedIn };
};

export default connect(
  mapStateToProps,
  { signIn, signOut }
)(Authentication);