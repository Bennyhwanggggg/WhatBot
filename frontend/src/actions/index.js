import backend from '../apis/backend'
import { SIGN_IN, SIGN_OUT } from './types'

export const sendMessage = message => async dispatch => {
    // backend.post('send', message);
    console.log(message)
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
