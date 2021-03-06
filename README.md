# DNS Auto Update Dynamic IP
It is possible to check the Public IP on the router, if the ISP provides a Private IP, this program will reconnect the PPOE until the ISP provides a Public IP, then update the DNS on your provider.

## To Do


## Supported Router
    Nokia G-240W-L => 'G-240W-L'
    ~ Soon ~

* Maybe another router can work if the system UI in Router settings is the same as one of the lists above

## Supported DNS Provider
    Cloudflare DNS => 'cloudflare'
    PowerDNS Cyberpanel => 'pdns_cyberpanel'
    ~ Soon ~

## Supported Operating System
* Windows
* Linux

## Supported Browser Driver
    Firefox => 'firefox'
    Chrome => 'chrome'
    Edge => 'msedge'

## Usage
### Requirements
* Python 3
* Browser Installed (Firefox, Chrome, Edge)
### Installation
* Make python virtual environment
    ```
    python3 -m venv <venv_location>
    cd <venv_location>
    ```
* Clone this repository inside venv
    ```
    git init
    git remote add origin https://github.com/Intprism-Technology/DNS-Dynamic-IP.git
    git fetch
    git branch master origin/main
    git checkout master
    ```
* Run using Cron (Linux)
    ```
    */5 * * * * /venv_location/bin/python /venv_location/start.py >> /var/log/DNS-Dynamic-IP.log 2>&1
    ```
* Run using Task Scheduler (Windows)
    ```
    1. Make sure you logged on as an administrator or you have the same access as an administrator.
    2. Start->Control Panel->System and Security->Administrative Tools->Task Scheduler
    3. Action->Create Basic Task->Type a name and Click Next
    4. Follow through the wizard.
    ```
### Configuration
* Edit at configuration.py, example you can see inside folder examples/configuration.py
    ```
    routerType              = ''    # required from lists
    routerIP                = ''    # required
    username                = ''    # required
    password                = ''    # required
    browserDriver           = ''    # required from lists
    headlessMode            = True  # required (True or False)
    dnsDriver               = ''    # required from lists

    # Cloudflare API
    cf_email                = ''    # required based on dnsDriver
    cf_token                = ''    # required based on dnsDriver
    cf_exceptListDnsUpdate  = []    # optional
    cf_ipType               = ''    # required based on dnsDriver (A or AAAA)
    cf_onlyDomain           = []    # optional
    cf_onlyDnsRecord        = []    # optional

    # PowerDNS Cyberpanel
    cyberpanel_dbHost       = ''    # required based on dnsDriver
    cyberpanel_dbUser       = ''    # required based on dnsDriver
    cyberpanel_dbPassword   = ''    # required based on dnsDriver
    cyberpanel_dbName       = ''    # required based on dnsDriver
    ```

## FAQ
* How is the performance of this program?
    ```
    Good performance according to supported routers !
    ```
* Does the computer have to run 24/7?
    ```
    Right, should run 24H, I suggest creating a small virtual machine on your host computer
    ```
* Is it possible to use linux server CLI?
    ```
    Yes you can, first install browser using command line, and run the service
    ```
* I want to contribute and add support router or DNS provider
    ```
    I really appreciate it, please fork and do a push request to this repository
    ```

## Support
<a href="https://www.buymeacoffee.com/habibulilalbaab" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>