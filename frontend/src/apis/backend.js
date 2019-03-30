import axios from 'axios';

const dev = 'http://localhost:9999';
const prod = `https://${process.env.REACT_APP_BACKEND_NAME}.herokuapp.com`
const backendURL = process.env.NODE_ENV === 'development' ? dev : prod

export default axios.create({
    baseURL: backendURL
});