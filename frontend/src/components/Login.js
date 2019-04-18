import React from 'react';
import { connect } from 'react-redux';
import { signIn, checkSignedIn } from '../actions';
import { Button, Form, Grid, Header, Segment } from 'semantic-ui-react';
import backendURL from '../apis/routes';
import history from '../history';

class Login extends React.Component {

    componentDidMount() {
        fetch(`${backendURL}`)
    }

    componentDidUpdate() {
        this.props.checkSignedIn(this.props.errorMessage)
        if (this.props.isSignedIn) {
            history.push('/chatroom');
        }
    }

    renderErrorMessage = () => {
        if (this.props.errorMessage) {
            return (
                <div className="ui red message">
                    {this.props.errorMessage}
                </div>
            )
        }
    }

    onSubmit = () => {
        const username = this.state.username;
        const password = this.state.password;
        this.props.signIn(username, password);
    }

    onInputUsernameChange = (evt) => {
        this.setState({
            username: evt.target.value
        });
    }

    onInputPasswordChange = (evt) => {
        this.setState({
            password: evt.target.value
        });
    }

    render() {
        return (
            <div className='login-form'>
                <style>{`
                body > div,
                body > div > div,
                body > div > div > div.login-form {
                    height: 100%;
                }
                `}
                </style>
                <Grid textAlign='center' style={{ height: '100%' }} verticalAlign='middle'>
                <Grid.Column style={{ maxWidth: 450 }}>
                    {this.renderErrorMessage()}
                    <Header as='h2' color='teal' textAlign='center'>
                    Log in
                    </Header>
                    <Form size='large' onSubmit={this.onSubmit}>
                        <Segment stacked className='loginForm'>
                            <Form.Input 
                                required
                                fluid icon='user' 
                                iconPosition='left' 
                                placeholder='zID'
                                onChange={this.onInputUsernameChange}
                                />
                            <Form.Input
                                required
                                fluid
                                icon='lock'
                                iconPosition='left'
                                placeholder='Password'
                                type='password'
                                onChange={this.onInputPasswordChange}
                            />
                
                            <Button color='teal' 
                                    fluid size='large'>
                                Login
                            </Button>
                        </Segment>
                    </Form>
                </Grid.Column>
                </Grid>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return { 
        isSignedIn: state.auth.isSignedIn,
        userId: state.auth.userId,
        accessLevel: state.auth.accessLevel,
        errorMessage: state.auth.errorMessage
    }
}

export default connect(
    mapStateToProps,
    { signIn, checkSignedIn }
)(Login);