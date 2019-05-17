import axios from 'axios';

import { GET_ZHIHU, DELETE_ZHIHU } from './types';

export const getZhihu = () => dispatch => {
    axios.get('/zhihu')
    .then(res => {
        dispatch({
            type: GET_ZHIHU,
            payload: res.data.results
        });
    }).catch(err => console.log(err));
};

// Delete post
export const deleteZhihu = (id) => dispatch => {
    axios
        .delete(`/zhihu/${id}/`)
        .then(res => {
            dispatch({
                type: DELETE_ZHIHU,
                payload: id
            });
        })
        .catch(err => console.log(err));
};