import backend from '../apis/backend';
import { SIGN_IN, SIGN_OUT, IS_SIGNED_IN, MESSAGE_SENT, MESSAGE_RECIEVED, MESSAGE_LOADING } from './types';
import uuid from 'uuid';
import history from '../history';

export const sendMessage = message => async dispatch => {
    const id = uuid.v4();
    dispatch({type: MESSAGE_SENT, payload: message, id: id}); 
    const loading = {message: 'loading'}
    dispatch({type: MESSAGE_LOADING, payload: loading, id: id});
    const response = await backend.post('/message', message, id);
    dispatch({type: MESSAGE_RECIEVED, payload: response.data, id: id});
}

export const signIn = (username, password) => async dispatch => {
    console.log('trying to sign in with ', username, password)
    const data = { username: username, password: password }

    try {
        const response = await backend.post('/login', data);
        window.localStorage.setItem('token', response.data.token);
        console.log(window.localStorage)
        dispatch ({
                type: SIGN_IN,
                payload: response.data
            }
        )
        history.push('/chatroom');
    } catch (err) {
        console.log(err)
        // TODO: notify user wrong username and password
        dispatch({
            type: SIGN_OUT
        })
    } 
}

export const signOut = () => {
    window.localStorage.removeItem('token');
    return {
      type: SIGN_OUT
    }
}

export const checkSignedIn = () => async dispatch => {
    let token = window.localStorage.getItem('token');
    console.log(token)
    const notSignedInData = { status: false, id: null, authority: null }
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