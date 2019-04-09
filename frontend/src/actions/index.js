import backend from '../apis/backend'
import { SIGN_IN, SIGN_OUT, MESSAGE_SENT, MESSAGE_RECIEVED } from './types'

export const sendMessage = message => async dispatch => {
    dispatch({type: MESSAGE_SENT, payload: message}); 
    const response = await backend.post('message', message);
    dispatch({type: MESSAGE_RECIEVED, payload: response.data}) ;
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
