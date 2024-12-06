import axios from "axios";
import qs from 'qs'

const api = axios.create({
    baseURL: 'http://localhost:5000',  // 后端 API 根路径
    timeout: 5000 * 10,  // 设置请求超时
});

// 请求拦截器
api.interceptors.request.use(config => {
    // 可以在这里添加请求头，或做其他请求前的处理
    return config;
}, error => {
    return Promise.reject(error);
});


// 响应拦截器
api.interceptors.response.use(response => {
    return response.data;  // 返回响应的数据
}, error => {
    return Promise.reject(error);
});

export const chart1Data = (area, year) => {
    return api.get('/chart1', {
        params: {area, year},
        paramsSerializer: (params) => {
            // 使用 'qs' 库序列化参数，确保格式为 'year=2020&year=2021'
            return qs.stringify(params, {arrayFormat: 'repeat'});
        }
    });
};

export const chart2Data = (area, year) => {
    return api.get('/chart2', {
        params: {area, year},
        paramsSerializer: (params) => {
            return qs.stringify(params, {arrayFormat: 'repeat'});
        }
    });
};

export const chart3Data = (area) => {
    return api.get('/chart3', {
        params: {area},
        paramsSerializer: (params) => {
            return qs.stringify(params, {arrayFormat: 'repeat'});
        }
    });
};

export const chart4Data = (year) => {
    return api.get('/chart4', {
        params: {year},
        paramsSerializer: (params) => {
            return qs.stringify(params, {arrayFormat: 'repeat'});
        }
    });
};

export const chart5Data = (year) => {
    return api.get('/chart5', {
        params: {year},
        paramsSerializer: (params) => {
            return qs.stringify(params, {arrayFormat: 'repeat'});
        }
    });
};

export const chart6Data = (checkPoint) => {
    return api.get('/chart6', {
        params: {checkPoint}
    });
};

export const chart7Data = () => {
    return api.get('/chart7', {});
}

export const getTimeLine = () => {
    return api.get('/timeline', {});
};

export const getArea = () => {
    return api.get('/areas', {});
}

export const getMapData = () => {
    return api.get('/map', {});
}