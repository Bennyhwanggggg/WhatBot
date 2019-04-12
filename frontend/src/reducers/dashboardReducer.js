import { PIECHART_GET } from '../actions/types';

const INITIAL_STATE = { piechart: {}}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case PIECHART_GET:
            console.log(action.payload)
            return {...state, piechart: action.payload};
        default:
            return state
    }
}