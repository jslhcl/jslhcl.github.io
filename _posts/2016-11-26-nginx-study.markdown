---
layout:	post
title:	"Nginx study"
date:	2016-11-26
---
# Reference
1. [Nginx开发从入门到精通](http://tengine.taobao.org/book/)
2. [Lenky](http://www.lenky.info/archives/category/%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90/nginx)
3. [nginx核心讲解](http://lenky.info/ebook/)
4. [nginx debug](http://blog.csdn.net/xiajun07061225/article/details/9383883)

# Compile

1. sudo auto/configure

This step will configure some variables and create objs/Makefile

Install PCRE, zlib if you haven't 

2. sudo make -f objs/Makefile

# Add new module

add a new folder containing config and ngx_http_xxx_module.c (for example, hello/config, hello/ngx_http_hello_module.c), then configure with this argument:

{% highlight bash %}
sudo auto/configure --add-module=./src/http/modules/hello

sudo auto/configure --add-module=./src/http/modules/hello --add-module=./src/http/modules/post
{% endhighlight %}

then 

{% highlight bash %}
sudo make -f objs/Makefile
{% endhighlight %}

change nginx.conf if necessary, and reload it:

{% highlight bash %}
sudo objs/nginx -s reload
{% endhighlight %}

# Debug

1. using GDB to attach nginx process

{% highlight bash %}
sudo gdb
(gdb) attach 16288 
{% endhighlight %}

2. in configuration file:

{% highlight bash %}
master_process off;
{% endhighlight %}

this will leave only one process for nginx

{% highlight bash %}
daemon off;
{% endhighlight %}

daemon off means it is no longer a daemon process. Use this setting when debug so we can use

{% highlight bash %}
sudo gdb objs/nginx
{% endhighlight %}

and comment out this setting when run nginx.

# Misc

ngx_cycle_modules() initialize cycle->modules from ngx_modules

ngx_preinit_modules() initialize ngx_modules from ngx_module_names

## handle request

ngx_http_read_request_header(), then ngx_http_parse_request_line()

ngx_http_process_request_headers(), ngx_http_process_request_line()

## upload module

ngx_http_core_main_conf_t

ngx_http.c, ngx_http_init_phase_handlers()

# Questions

1. How is the settings in config file related with the code?

2. Will all the modules be linked in runtime? 

No, in the function ngx_load_module(), it uses the system function dlsym() to load modules from binary. So only the modules linked during compiling will be involved. 

# How to work with PHP

Refer [this link](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04)

1. install PHP

{% highlight bash %}
sudo apt-get install php5-fpm
{% endhighlight %}

2. change nginx configuration file

add the following lines in the "server" block:

{% highlight bash %}
index index.php index.html index.htm;

location ~ \.php$ {
                try_files $uri =404;
                fastcgi_pass unix:/var/run/php5-fpm.sock;
                fastcgi_index index.php;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;                
        }
{% endhighlight %}

Notice: If you build nginx from source code, you need to copy fastcgi.conf and fastcgi_params into the conf/ folder manually.

3. create a php file to test

{% highlight bash %}
sudo vim /usr/local/nginx/html/info.php
{% endhighlight %}

its contents:

{% highlight php %}
<?php
phpinfo();
?>
{% endhighlight %}

and check it out. 
