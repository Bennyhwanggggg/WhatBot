import backend from '../apis/backend'
import { SIGN_IN, SIGN_OUT, MESSAGE_SENT, MESSAGE_RECIEVED, MESSAGE_LOADING } from './types'
import uuid from 'uuid';

export const sendMessage = message => async dispatch => {
    const id = uuid.v4();
    dispatch({type: MESSAGE_SENT, payload: message, id: id}); 
    const loading = {message: 'loading'}
    dispatch({type: MESSAGE_LOADING, payload: loading, id: id});
    const response = await backend.post('message', message, id);
    dispatch({type: MESSAGE_RECIEVED, payload: response.data, id: id});
}

export const signIn = (username, password) => async dispatch => {
    const response = await backend.post('/login', username, password);
    if (response.status != 200) {
        // TODO: notify user wrong username and password
        return {
            type: SIGN_OUT
        }
    } 
    window.localStorage.setItem('token', response.data.token)
    return {
      type: SIGN_IN,
      payload: response.data
    }
}

export const signOut = () => {
    return {
      type: SIGN_OUT
    }
}
