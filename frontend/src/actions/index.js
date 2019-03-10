import backend from '../apis/backend'
import { SIGN_IN, SIGN_OUT, MESSAGE_SENT } from './types'

export const sendMessage = message => async dispatch => {
    // const response = await backend.post('send', message);
    console.log('action: ',message)
    dispatch({type: MESSAGE_SENT}) // TODO: add response.data later
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
