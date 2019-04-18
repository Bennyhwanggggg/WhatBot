const dev = 'http://localhost:9999';
const prod = `http://localhost:9999`;
const backendURL = process.env.NODE_ENV === 'development' ? dev : prod;

export default backendURL;