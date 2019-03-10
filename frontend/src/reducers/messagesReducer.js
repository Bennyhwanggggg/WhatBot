import _ from 'lodash'
import { MESSAGE_SENT, MESSAGE_RECIEVED } from '../actions/types'
import uuid from 'uuid';

export default (state = {}, action) => {
    switch (action.type) {
        case MESSAGE_SENT:
            console.log(state)
            const id = uuid.v4();
            action.payload.id = id;
            return { ...state, [id]: action.payload }
            // return { ...state, [action.payload.id]: action.payload }
        case MESSAGE_RECIEVED:
            return { ...state, [uuid.v4()]: action.payload }
            // return { ...state, [action.payload.id]: action.payload }
        default:
            return state
    }
}
