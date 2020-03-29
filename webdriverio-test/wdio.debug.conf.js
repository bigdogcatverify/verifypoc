const wdio = require('./wdio.conf')

const chromeConfig = {
    maxInstances: 1,
    jasmineNodeOpts: {
        defaultTimeoutInterval: (24 * 60 * 60 * 1000)
    },
    automationProtocol: 'devtools',
    capabilities: [{
        'browserName': 'chrome',
        'goog:chromeOptions': {
            // @ts-ignore
            headless: process.env.CHROME_HEADLESS === 'true'
        }
    }],
    mochaOpts: {
        ui: 'bdd',
        require: ['@babel/register'],
        timeout: (24 * 60 * 60 * 1000)
    },
    waitforTimeout: (24 * 60 * 60 * 1000)
};

exports.config = Object.assign(wdio.config, chromeConfig);
