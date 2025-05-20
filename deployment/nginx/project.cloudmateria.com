server {
  listen 443 ssl;
http2 on;
  server_name project.cloudmateria.com;

  root /var/www/project;

  # Enable cache control headers for static files
  location / {
    try_files $uri $uri/ /index.html;
    set $allow_origin '';
    if ($http_origin ~* "^https?://([a-zA-Z0-9-]+)\.cloudmateria\.com$") {
        set $allow_origin $http_origin;
    }

    if ($allow_origin) {
        add_header 'Access-Control-Allow-Origin' $allow_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, X-Requested-With, Authorization' always;
    }
    
    # Cache all static assets
    add_header Cache-Control 'public, max-age=31536000, immutable';  # Cache for one year
  }

  # Cache for static files (JavaScript, CSS, Images)
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|webp|ttf|woff|woff2|eot|otf|json|html|xml)$ {
    set $allow_origin '';
    if ($http_origin ~* "^https?://([a-zA-Z0-9-]+)\.cloudmateria\.com$") {
        set $allow_origin $http_origin;
    }

    if ($allow_origin) {
        add_header 'Access-Control-Allow-Origin' $allow_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, X-Requested-With, Authorization' always;
    }

    # Cache static files (for a year)
    add_header Cache-Control 'public, max-age=31536000, immutable';  # Cache for 1 year
    try_files $uri =404;
  }

  # Handle preflight OPTIONS request
  location ~ ^/.*\.(js|css|json|html|xml)$ {
    set $allow_origin '';
    if ($http_origin ~* "^https?://([a-zA-Z0-9-]+)\.cloudmateria\.com$") {
        set $allow_origin $http_origin;
    }

    if ($allow_origin) {
        add_header 'Access-Control-Allow-Origin' $allow_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, X-Requested-With, Authorization' always;
        add_header 'Access-Control-Max-Age' 1728000;  # Cache preflight response for 20 days
    }
    if ($request_method = 'OPTIONS') {
        return 204;
    }
  }

  # Fallback for 404
  error_page 404 /index.html;
}














