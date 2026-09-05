-- APCafeteria MySQL schema. Keep synchronized with models and Alembic revisions.
CREATE DATABASE IF NOT EXISTS cafeteria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cafeteria;

CREATE TABLE roles (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_roles_name (name)
) ENGINE=InnoDB;

CREATE TABLE users (
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    role_id BIGINT NOT NULL,
    department_id BIGINT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    type VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email),
    KEY ix_users_role_id (role_id),
    KEY ix_users_department_id (department_id),
    CONSTRAINT fk_users_role_id FOREIGN KEY (role_id) REFERENCES roles (id)
) ENGINE=InnoDB;

CREATE TABLE shops (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    description TEXT NULL,
    logo_url VARCHAR(500) NULL,
    domain_url VARCHAR(500) NOT NULL,
    login_url TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    open_at TIME NULL,
    close_at TIME NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_shops_email (email)
) ENGINE=InnoDB;

CREATE TABLE categories (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    description TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_categories_name (name)
) ENGINE=InnoDB;

CREATE TABLE shop_categories (
    id BIGINT NOT NULL AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_shop_categories_pair (shop_id, category_id),
    KEY ix_shop_categories_shop_id (shop_id),
    KEY ix_shop_categories_category_id (category_id),
    CONSTRAINT fk_shop_categories_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id),
    CONSTRAINT fk_shop_categories_category_id FOREIGN KEY (category_id) REFERENCES categories (id)
) ENGINE=InnoDB;

CREATE TABLE shop_staffs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'staff',
    email VARCHAR(255) NULL,
    phone VARCHAR(30) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_shop_staffs_email (email),
    KEY ix_shop_staffs_shop_id (shop_id),
    CONSTRAINT fk_shop_staffs_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id)
) ENGINE=InnoDB;

CREATE TABLE genres (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_genres_name (name)
) ENGINE=InnoDB;

CREATE TABLE menus (
    id BIGINT NOT NULL AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    cost DECIMAL(12,2) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    image VARCHAR(500) NULL,
    description TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_menus_shop_id (shop_id),
    CONSTRAINT fk_menus_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id)
) ENGINE=InnoDB;

CREATE TABLE menu_genres (
    id BIGINT NOT NULL AUTO_INCREMENT,
    menu_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_menu_genres_pair (menu_id, genre_id),
    KEY ix_menu_genres_menu_id (menu_id),
    KEY ix_menu_genres_genre_id (genre_id),
    CONSTRAINT fk_menu_genres_menu_id FOREIGN KEY (menu_id) REFERENCES menus (id),
    CONSTRAINT fk_menu_genres_genre_id FOREIGN KEY (genre_id) REFERENCES genres (id)
) ENGINE=InnoDB;

CREATE TABLE payment_methods (
    id BIGINT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,
    logo VARCHAR(500) NULL,
    domain_url VARCHAR(500) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_payment_methods_name (name)
) ENGINE=InnoDB;

CREATE TABLE payment_accounts (
    id BIGINT NOT NULL AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    payment_method_id BIGINT NOT NULL,
    account_holder_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    image VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_payment_accounts_shop_id (shop_id),
    KEY ix_payment_accounts_payment_method_id (payment_method_id),
    CONSTRAINT fk_payment_accounts_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id),
    CONSTRAINT fk_payment_accounts_payment_method_id FOREIGN KEY (payment_method_id) REFERENCES payment_methods (id)
) ENGINE=InnoDB;

CREATE TABLE orders (
    id BIGINT NOT NULL AUTO_INCREMENT,
    shop_id BIGINT NOT NULL,
    user_id BIGINT NULL,
    shop_id BIGINT NULL,
    user_email VARCHAR(255) NOT NULL,
    order_code VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal_amount DECIMAL(12,2) NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    remark TEXT NULL,
    payment_account_id BIGINT NOT NULL,
    tax_fee DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    is_pickup BOOLEAN NOT NULL DEFAULT TRUE,
    delivery_location VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_orders_order_code (order_code),
    KEY ix_orders_shop_id (shop_id), KEY ix_orders_user_id (user_id),
    KEY ix_orders_payment_account_id (payment_account_id),
    CONSTRAINT fk_orders_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id),
    CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_orders_payment_account_id FOREIGN KEY (payment_account_id) REFERENCES payment_accounts (id)
) ENGINE=InnoDB;

CREATE TABLE order_menus (
    id BIGINT NOT NULL AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    menu_id BIGINT NOT NULL,
    quantity BIGINT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), UNIQUE KEY uq_order_menus_pair (order_id, menu_id),
    KEY ix_order_menus_order_id (order_id), KEY ix_order_menus_menu_id (menu_id),
    CONSTRAINT fk_order_menus_order_id FOREIGN KEY (order_id) REFERENCES orders (id),
    CONSTRAINT fk_order_menus_menu_id FOREIGN KEY (menu_id) REFERENCES menus (id)
) ENGINE=InnoDB;

CREATE TABLE order_logs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    status VARCHAR(50) NOT NULL,
    user_id BIGINT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), KEY ix_order_logs_order_id (order_id), KEY ix_order_logs_user_id (user_id),
    CONSTRAINT fk_order_logs_order_id FOREIGN KEY (order_id) REFERENCES orders (id),
    CONSTRAINT fk_order_logs_user_id FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE=InnoDB;

CREATE TABLE user_activities (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    activity TEXT NOT NULL,
    active_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id), KEY ix_user_activities_user_id (user_id),
    CONSTRAINT fk_user_activities_user_id FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE=InnoDB;

CREATE TABLE revoked_tokens (
    id BIGINT NOT NULL AUTO_INCREMENT,
    jti VARCHAR(36) NOT NULL,
    user_id BIGINT NOT NULL,
    expires_at DATETIME NOT NULL,
    revoked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_revoked_tokens_jti (jti),
    KEY ix_revoked_tokens_user_id (user_id),
    KEY ix_revoked_tokens_shop_id (shop_id),
    KEY ix_revoked_tokens_expires_at (expires_at),
    CONSTRAINT fk_revoked_tokens_user_id FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_revoked_tokens_shop_id FOREIGN KEY (shop_id) REFERENCES shops (id)
) ENGINE=InnoDB;
