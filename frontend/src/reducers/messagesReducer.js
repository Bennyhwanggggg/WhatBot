import _ from 'lodash'
import { MESSAGE_SENT, MESSAGE_RECIEVED } from '../actions/types'

export default (state = {}, action) => {
    switch (action.type) {
        case MESSAGE_SENT:
            return { ...state, [action.payload.id]: action.payload }
        case MESSAGE_RECIEVED:
            return { ...state, [action.payload.id]: action.payload }
        default:
            return state
    }
}
