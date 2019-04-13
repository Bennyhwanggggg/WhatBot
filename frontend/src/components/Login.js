import React from 'react';
import { connect } from 'react-redux';
import { signIn, signOut} from '../actions';
import { Button, Form, Grid, Header, Segment } from 'semantic-ui-react';

class Login extends React.Component {

    onSubmit = () => {
        const username = this.state.username;
        const password = this.state.password;
        if (!username || !password) {
            // TODO: show error 
            return;
        }
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
                    <Header as='h2' color='teal' textAlign='center'>
                    Log in
                    </Header>
                    <Form size='large' onSubmit={this.onSubmit}>
                        <Segment stacked className='loginForm'>
                            <Form.Input 
                                fluid icon='user' 
                                iconPosition='left' 
                                placeholder='zID'
                                onChange={this.onInputUsernameChange}
                                />
                            <Form.Input
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
        accessLevel: state.auth.accessLevel
    }
}

export default connect(
    mapStateToProps,
    {signIn, signOut}
)(Login);