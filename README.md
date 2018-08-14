# Namecheap host updater

Simple Python script to update a host DNS record on [Namecheap](https://www.namecheap.com).


## How it works

* Set the following environment variables
    * `NAMECHEAP_HOST`: host part of a FQDN.
    * `NAMECHEAP_DOMAIN`: domain part of a FQDN.
    * `NAMECHEAP_TOKEN`: Token, get it from Namecheap after enabling the dynamic DNS feature on your domain.
* After setting those three variables, just run it.
