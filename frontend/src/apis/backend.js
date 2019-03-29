import axios from 'axios';

const backendURL = process.env.NODE_ENV === 'development' ? 'http://localhost:9999' : `http://${process.env.REACT_APP_BACKEND_NAME}:${process.env.REACT_APP_BACKEND_PORT}`

export default axios.create({
    baseURL: backendURL
});