import { MESSAGE_SENT, MESSAGE_RECIEVED, MESSAGE_LOADING } from '../actions/types'
import uuid from 'uuid';

const INITIAL_STATE = { messages:[] }

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case MESSAGE_SENT:
            const id = uuid.v4();
            action.payload.id = id;
            return { ...state, messages: [...state.messages, action.payload] }
        case MESSAGE_RECIEVED:
            action.payload.id = action.id
            return { ...state, messages: state.messages.map(message => (message.id === action.id) ? action.payload : message) }
        case MESSAGE_LOADING:
            action.payload.id = action.id
            return { ...state, messages: [...state.messages, action.payload] }
        default:
            return state
    }
}
