import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import authReducer from './authReducer';
import messagesReducer from './messagesReducer'

export default combineReducers({
  auth: authReducer,
  form: formReducer,
  messages: messagesReducer 
});