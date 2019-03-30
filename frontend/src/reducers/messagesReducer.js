import { MESSAGE_SENT, MESSAGE_RECIEVED } from '../actions/types'
import uuid from 'uuid';

export default (state = {}, action) => {
    switch (action.type) {
        case MESSAGE_SENT:
            console.log(MESSAGE_SENT, action.payload)
            const id = uuid.v4();
            action.payload.id = id;
            return { ...state, [id]: action.payload }
        case MESSAGE_RECIEVED:
            console.log(MESSAGE_RECIEVED, action.payload)
            return { ...state, [action.payload.id]: action.payload }
        default:
            return state
    }
}
