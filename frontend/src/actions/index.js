import backend from '../apis/backend';
import { SIGN_IN, SIGN_OUT, IS_SIGNED_IN, MESSAGE_SENT, MESSAGE_RECIEVED, MESSAGE_LOADING } from './types';
import uuid from 'uuid';
import history from '../history';

export const sendMessage = (message, username) => async dispatch => {
    const id = uuid.v4();
    dispatch({type: MESSAGE_SENT, payload: message, id: id}); 
    const loading = {message: 'loading'}
    dispatch({type: MESSAGE_LOADING, payload: loading, id: id});
    message = {...message, username: username}
    const response = await backend.post('/message', message);
    dispatch({type: MESSAGE_RECIEVED, payload: response.data, id: id});
}

export const signIn = (username, password) => async dispatch => {
    const data = { username: username, password: password }
    try {
        const response = await backend.post('/login', data);
        window.localStorage.setItem('token', response.data.token);
        dispatch ({
                type: SIGN_IN,
                payload: response.data
            }
        )
        history.push('/chatroom');
    } catch (err) {
        console.log(err)
        dispatch({
            type: SIGN_OUT,
            payload: {errorMessage: 'The username or password you entered is invalid'}
        })
    } 
}

export const signOut = () => dispatch => {
    window.localStorage.removeItem('token');
    dispatch ({
        type: SIGN_OUT,
        payload: { errorMessage: null }
    })
}

export const checkSignedIn = (message) => async dispatch => {
    let token = window.localStorage.getItem('token');
    const notSignedInData = { status: false, id: null, authority: null, errorMessage: message }
    if(!token || token === '') { //if there is no token, dont bother
        dispatch({
            type: IS_SIGNED_IN,
            payload: notSignedInData
        })
  	} else {
        const response = await fetch('http://localhost:9999/validation', {
            method: 'POST',
            headers: {
                Authorization: token
            }
        })
        if (response.status !== 200) {
            window.localStorage.removeItem('token');
            dispatch({
                type: IS_SIGNED_IN,
                payload: notSignedInData
            })
        } else {
            response.json().then(
                data => {
                    dispatch({
                        type: IS_SIGNED_IN,
                        payload: { status: true, id: data.id, authority: data.authority }
                    })
                }
            )
        }
    }
}