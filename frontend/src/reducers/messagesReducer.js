import { MESSAGE_SENT, MESSAGE_RECIEVED, MESSAGE_LOADING } from '../actions/types'
import uuid from 'uuid';

export default (state = {}, action) => {
    switch (action.type) {
        case MESSAGE_SENT:
            const id = uuid.v4();
            action.payload.id = id;
            console.log(MESSAGE_SENT, id, action.payload)
            return { ...state, [id]: action.payload }
        case MESSAGE_RECIEVED:
            console.log(MESSAGE_RECIEVED, action.payload)
            return { ...state, [action.id]: action.payload }
        case MESSAGE_LOADING:
            console.log(MESSAGE_LOADING, action.id, action.payload)
            return { ...state, [action.id]: action.payload }
        default:
            return state
    }
}
