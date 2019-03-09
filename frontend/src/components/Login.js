import React, { Component } from 'react';

import axios from 'axios';

const serverUrl = 'http://';
const http = axios.create({
    baseURL: serverUrl
});

class Login extends Component {

    constructor() {
        super();
        this.state = {
            firstName: "",
            password: ""
        }
        this.handleChange = this.handleChange.bind(this)
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }


    //onLogin: function() {
    //    user = this.state.username;
    //    if (!user) {
    //        http.post('/login', {username})
    //        .then(() => this.setState({isLoggedIn: true}))
    //        .catch((err) => console.log(err));
    //    }
    //}

    render() {
        const {messages} = this.props;
        return (
            <div>
                <form class='header item'>
                    <input type='text' name='firstName' placeholder='username' onChange={ this.handleChange }/>
                    <button>Login</button>
                </form>

            </div>

        );
    }
}

export default Login;