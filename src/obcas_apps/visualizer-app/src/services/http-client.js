export const OBCasHttpClient = () => {
    const setError = useSetRecoilState(commonError);
    const navigate = useNavigate();
    const Config = useConfig();
  
    const defaultOptions = {
      headers: {
        Accept: "application/json",
      },
    };
  
    const client = axios.create();
  
    client.interceptors.request.use((config) => {
      if (!config.tokenInterceptor?.disabled) {
        const token = SecurityUserService.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
  
        if (Config.REACT_APP_RQUEST_PROXY)
          config.url = Config.REACT_APP_RQUEST_PROXY + config.url;
      }
      return config;
    });
  
    client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (!error.response.config.errorInterceptor?.disabled) {
          const status = error.response ? error.response.status : null;
  
          switch (status) {
            case 401:
              console.error("Unauthorized access");
              navigate(SecurityUserService.doLogin());
              break;
            case 500:
              console.error("An error occurred:", error);
              navigate(`${Config.REACT_APP_CONTEXT_ROOT}/error`);
              break;
            default:
              setError({
                isVisible: true,
                message: `${error.code}: ${error.message}`,
              });
              break;
          }
        }
        return Promise.reject(error);
      }
    );
  
    return {
      get: (url, options = {}) =>
        client.get(url, { ...defaultOptions, ...options }),
      post: (url, data, options = {}) =>
        client.post(url, data, { ...defaultOptions, ...options }),
      put: (url, data, options = {}) =>
        client.put(url, data, { ...defaultOptions, ...options }),
      patch: (url, data, options = {}) =>
        client.patch(url, data, { ...defaultOptions, ...options }),
      delete: (url, options = {}) =>
        client.delete(url, { ...defaultOptions, ...options }),
    };
  };