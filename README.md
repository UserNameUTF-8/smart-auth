# smart-auth

## API
### get baseUrl/admins/
GET ALL ADMINS
### post baseUrl/admin/
     ADD ADMIN
#### body

``` yaml
{
  "admin_fullname": "Admin_one__",
  "admin_password": "Admin_one_password",
  "admin_email": "admin__@go.com",
  "admin_ip": "localhost"
} 
```
### patch baseUrl/admins/
UPDATE ADMIN NAME OR IP

#### body

``` yaml
{
  "admin_id": 0, [req]
  "admin_name": "string",
  "admin_ip": "string"
}
[req] admin_name or admin_id
```

### put baseUrl/pass-update/

#### body

``` yaml
{
  "admin_id": 0, [req]
  "admin_password": "string" [req]
}
```


### get baseUrl/admins/id_ 
GET ADMIN BY ID
#### path param
``` yaml
{
  id_: int
}
```


### get baseUrl/admins/mail 
GET ADMIN BY MAIL
#### path param
``` yaml
{
  mail: str
}
```











