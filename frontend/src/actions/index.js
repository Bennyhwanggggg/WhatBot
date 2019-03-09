import backend from '../apis/backend';
import {
    SIGN_IN,
    SIGN_OUT,
} from './types';

export const sendMessage = async (message) => {
    console .log(message);
    console .log({message: message});
    // const response = backend.post('send', {message: message});
}

export const signIn = userId => {
    return {
      type: SIGN_IN,
      payload: userId
    };
  };
  
  export const signOut = () => {
    return {
      type: SIGN_OUT
    };
  };