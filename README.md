```
            d8,               d8b  d8b      
           `8P                88P  ?88      
                             d88    88b     
 d888b8b    88b  88bd88b d888888    888888b 
d8P' ?88    88P  88P'  `d8P' ?88    88P `?8b
88b  ,88b  d88  d88     88b  ,88b  d88,  d88
`?88P'`88bd88' d88'     `?88P'`88bd88'`?88P'                                             

an airline simulation for CPSC 304
```

### prerequisites
- python2.7  
- pip  
- flask  

### setup
- Clone this repo however you like: `$ git clone https://github.com/maknoon/airdb.git`  
- Install everything by executing `$ pip install -r requirements.txt`  

### develop on server
- Add our private SSH key `cpsc304.pem` to your `~/.ssh` directory  
- Change permissions on key to read-only: `$ chmod 400 ~/.ssh/cpsc304.pem`
- Add the following to your `~/.ssh/config` file (create one if it does not exist):  
  ```.ssh/config
  Host air
  	Hostname [ipv4 addr]
  	User ubuntu
  	IdentityFile ~/.ssh/cpsc304.pem
  ```
- rsync your (**tested!**) changes to EC2 instance:
  - in parent directory of repo, execute: `$ rsync -av --exclude-from 'airdb/excl.txt' airdb/ air:airdb/`  
- SSH into instance and type: `$ sudo apachectl restart`  
- Restart the server and exit to see your changes live  
