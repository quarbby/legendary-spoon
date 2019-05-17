import { GET_ZHIHU, DELETE_ZHIHU } from "../actions/types.js";

const initialState={
    zhihu: []
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_ZHIHU:
            return {
                ...state,
                zhihu: action.payload
            };
        case DELETE_ZHIHU:
            return {
                ...state,
                zhihu: state.zhihu.filter(zhihu => zhihu.id !== action.payload)
            };
        default:
            return state;
    }
}