import backend from '../apis/backend';

export const sendMessage = async (message) => {
    console .log(message);
    console .log({message: message});
    // const response = backend.post('send', {message: message});
}
