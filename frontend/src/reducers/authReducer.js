import { SIGN_IN, SIGN_OUT, IS_SIGNED_IN } from '../actions/types';

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
            console.log(SIGN_IN, action.payload)
            return { ...state, isSignedIn: true, userId: action.payload.id, accessLevel: action.payload.authority };
        case SIGN_OUT:
            console.log(SIGN_OUT)
            return { ...state, isSignedIn: false, userId: null, accessLevel: null };
        case IS_SIGNED_IN:
            console.log(IS_SIGNED_IN)
            console.log(action.payload)
            return { ...state, isSignedIn: action.payload.status, userId: action.payload.id, accessLevel: action.payload.authority}
        default:
            return state;
    }
};