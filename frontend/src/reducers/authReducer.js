import { SIGN_IN, SIGN_OUT } from '../actions/types';

const INTIAL_STATE = {
  isSignedIn: null,
  userId: null,
  accessLevel: null
};

/**Let this action creator be the only thing responsible for all 
login components */
export default (state = INTIAL_STATE, action) => {
  switch (action.type) {
    case SIGN_IN:
      return { ...state, isSignedIn: true, userId: action.payload.id, accessLevel: userId.payload.authority };
    case SIGN_OUT:
      return { ...state, isSignedIn: false, userId: null, accessLevel: null };
    default:
      return state;
  }
};