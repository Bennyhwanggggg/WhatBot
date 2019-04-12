import backend from '../apis/backend'
import { SIGN_IN, 
         SIGN_OUT, 
         MESSAGE_SENT, 
         MESSAGE_RECIEVED, 
         MESSAGE_LOADING, 
         INTENT_USAGE_PIECHART_GET, 
         INTENT_USAGE_TIMELINE_GET, 
         INTENT_USAGE_3D_GET, 
         INTENT_AVG_CONFIDENCE_BARCHART_GET } from './types'
import uuid from 'uuid';

export const sendMessage = message => async dispatch => {
    const id = uuid.v4();
    dispatch({type: MESSAGE_SENT, payload: message, id: id}); 
    const loading = {message: 'loading'}
    dispatch({type: MESSAGE_LOADING, payload: loading, id: id});
    const response = await backend.post('message', message, id);
    dispatch({type: MESSAGE_RECIEVED, payload: response.data, id: id});
}

export const getPiechartData = () => async dispatch => {
    const response = await backend.get('dashboard/piechart');
    dispatch({type: INTENT_USAGE_PIECHART_GET, payload: response.data})
}

export const get3DData = () => async dispatch => {
    const response = await backend.get('dashboard/threeD');
    dispatch({type: INTENT_USAGE_3D_GET, payload: response.data})
}

export const getTimelineData = () => async dispatch => {
    const response = await backend.get('dashboard/timeline');
    dispatch({type: INTENT_USAGE_TIMELINE_GET, payload: response.data})
}

export const getBarchartData = () => async dispatch => {
    const response = await backend.get('dashboard/barchart');
    dispatch({type: INTENT_AVG_CONFIDENCE_BARCHART_GET, payload: response.data})
}

export const signIn = userId => {
    return {
      type: SIGN_IN,
      payload: userId
    }
}

export const signOut = () => {
    return {
      type: SIGN_OUT
    }
}
