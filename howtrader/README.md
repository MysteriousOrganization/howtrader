1. cta_strategy_setting.json 
当前使用的策略配置
2. cta_strategy_data.json 
当前各个策略保存的变量信息
3. vt_setting.json
数据库，邮箱地址等配置
```json
{
    "font.family": "Arial",
    "font.size": 12,
    "order_update_interval": 120,
    "position_update_interval": 120,
    "account_update_interval": 120,
    "log.active": True,
    "log.level": CRITICAL,
    "log.console": True,
    "log.file": True,

    "email.server": "smtp.qq.com",
    "email.port": 465,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",

    "database.timezone": get_localzone().zone,
    "database.driver": "sqlite",                # see database.Driver
    "database.database": "database.db",         # for sqlite, use this as filepath
    "database.host": "localhost",
    "database.port": 3306,
    "database.user": "root",
    "database.password": "",
    "database.authentication_source": "admin",  # for mongodb
}
```
4. binance_settings.json  
用户币安账号配置
```json
{
    "key": "ndvHAirHVicXaxqxvqUZjOIlD8PuwSFGZafU2IC3gMloUMGiZ7rSTNeOuuP0D83c",
    "secret": "RaFdLIr1skrz1TWzXfFE9CprzfYWJXOBrYnmxbrNiZaFfPLCAtAM3IuJV1uQDyNV",
    "session_number": 3,
    "proxy_host": "127.0.0.1",
    "proxy_port": 7890
}
```
