import axios from 'axios';
import backendURL from './routes';

export default axios.create({
    baseURL: backendURL
});