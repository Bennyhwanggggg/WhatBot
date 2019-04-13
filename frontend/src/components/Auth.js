import React from 'react';
import { connect } from 'react-redux';
import { signIn, signOut} from '../actions';
import { Button, Form, Grid, Header, Image, Message, Segment } from 'semantic-ui-react';

class Auth extends React.Component {
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
                    <Form size='large'>
                        <Segment stacked className='loginForm'>
                            <Form.Input fluid icon='user' iconPosition='left' placeholder='zID'/>
                            <Form.Input
                                fluid
                                icon='lock'
                                iconPosition='left'
                                placeholder='Password'
                                type='password'
                            />
                
                            <Button color='teal' fluid size='large'>
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

export default Auth;