import { INTENT_USAGE_PIECHART_GET, INTENT_USAGE_TIMELINE_GET, INTENT_USAGE_3D_GET, INTENT_AVG_CONFIDENCE_BARCHART_GET } from '../actions/types';

const INITIAL_STATE = { piechart: {}, timeline: {}, threeD:{}, barchart:{}}

export default (state = INITIAL_STATE, action) => {
    switch (action.type) {
        case INTENT_USAGE_PIECHART_GET:
            return {...state, piechart: action.payload};
        case INTENT_USAGE_TIMELINE_GET:
            return {...state, timeline: action.payload};
        case INTENT_USAGE_3D_GET:
            return {...state, threeD: action.payload};
        case INTENT_AVG_CONFIDENCE_BARCHART_GET:
            return {...state, barchart: action.payload};
        default:
            return state
    }
}