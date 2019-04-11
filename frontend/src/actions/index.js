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

export const signIn = userId => {
    return {
      type: SIGN_IN,
      payload: userId
    }
}

export const signOut = () => {
    return {
      type: SIGN_OUT
    }
}
