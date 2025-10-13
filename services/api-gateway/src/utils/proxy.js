const axios = require('axios');
const logger = require('./logger');

const createServiceProxy = (serviceName, serviceUrl) => {
  return async (req, res, next) => {
    try {
      const url = `${serviceUrl}${req.path}`;
      const config = {
        method: req.method,
        url,
        headers: {
          ...req.headers,
          host: new URL(serviceUrl).host
        },
        ...(req.body && Object.keys(req.body).length > 0 && { data: req.body }),
        ...(req.query && Object.keys(req.query).length > 0 && { params: req.query })
      };

      logger.info(`Proxying ${req.method} ${req.path} to ${serviceName}`);
      
      const response = await axios(config);
      
      res.status(response.status).json(response.data);
    } catch (error) {
      logger.error(`Error proxying to ${serviceName}:`, error.message);
      
      if (error.response) {
        res.status(error.response.status).json(error.response.data);
      } else if (error.request) {
        res.status(503).json({
          error: 'Service Unavailable',
          message: `${serviceName} is not responding`,
          service: serviceName
        });
      } else {
        next(error);
      }
    }
  };
};

module.exports = { createServiceProxy };
