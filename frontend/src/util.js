// 根据当前环境自动选择API地址
let API_BASE_URL;

if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  // 本地开发环境
  API_BASE_URL = "/api";
} else {
  // 生产环境
  API_BASE_URL = "/choreo-apis/choose-your-adv/backend/v1/api";
}

export { API_BASE_URL };