import { SIGN_IN, SIGN_OUT, IS_SIGNED_IN } from '../actions/types';

const INTIAL_STATE = {
    isSignedIn: null,
    userId: null,
    accessLevel: null,
    errorMessage: null
};

/**Let this action creator be the only thing responsible for all 
login components */
export default (state = INTIAL_STATE, action) => {
    switch (action.type) {
        case SIGN_IN:
            return { ...state, 
                    isSignedIn: true, 
                    userId: action.payload.id, 
                    accessLevel: action.payload.authority, 
                    errorMessage: null };
        case SIGN_OUT:
            return { ...state, 
                    isSignedIn: false, 
                    userId: null, 
                    accessLevel: null,
                    errorMessage: action.payload.errorMessage };
        case IS_SIGNED_IN:
            return { ...state, 
                    isSignedIn: action.payload.status, 
                    userId: action.payload.id, 
                    accessLevel: action.payload.authority,
                    errorMessage: action.payload.errorMessage };
        default:
            return state;
    }
};