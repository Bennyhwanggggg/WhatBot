import backend from '../apis/backend'
import { SIGN_IN, SIGN_OUT, MESSAGE_SENT, MESSAGE_RECIEVED } from './types'

export const sendMessage = message => async dispatch => {
    // const response = await backend.post('send', message);
    console.log('action: ',message)
    dispatch({type: MESSAGE_SENT, payload: message}) 
    // dispatch({type: MESSAGE_RECIEVED, payload: message}) // TODO: change to response.data later
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
