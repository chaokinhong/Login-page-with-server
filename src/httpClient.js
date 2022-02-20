import axios from 'axios';

// will send all the cookies here

export default axios.create({
    withCredentials: true,
})