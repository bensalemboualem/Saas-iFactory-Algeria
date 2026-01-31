FROM php:8.2-fpm

# Arguments
ARG user=iafactory
ARG uid=1000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    nginx \
    supervisor

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PHP extensions INCLUDING OPCACHE for performance
RUN docker-php-ext-install pdo_mysql mysqli mbstring exif pcntl bcmath gd zip opcache

# Copy PHP production configuration
COPY docker/php.ini /usr/local/etc/php/conf.d/99-production.ini

# Copy PHP-FPM pool configuration
COPY docker/www.conf /usr/local/etc/php-fpm.d/zz-performance.conf

# Configure PHP-FPM to pass environment variables
RUN echo "clear_env = no" >> /usr/local/etc/php-fpm.d/www.conf

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Create system user
RUN useradd -G www-data,root -u $uid -d /home/$user $user
RUN mkdir -p /home/$user/.composer && \
    chown -R $user:$user /home/$user

# Set working directory
WORKDIR /var/www

# Copy existing application
COPY --chown=$user:$user . /var/www

# Copy nginx config
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Copy supervisor config
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set permissions
RUN chown -R www-data:www-data /var/www/storage /var/www/bootstrap/cache
RUN chmod -R 775 /var/www/storage /var/www/bootstrap/cache

# Expose port
EXPOSE 80

# Start supervisor (manages nginx + php-fpm)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
