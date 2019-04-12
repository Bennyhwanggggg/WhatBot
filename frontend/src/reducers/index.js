import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';
import authReducer from './authReducer';
import messagesReducer from './messagesReducer';
import dashboardReducer from './dashboardReducer';

export default combineReducers({
  auth: authReducer,
  form: formReducer,
  messages: messagesReducer,
  dashboard: dashboardReducer
});