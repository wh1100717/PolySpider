CREATE TABLE ps_app(
    id INTEGER PRIMARY KEY,
    app_name VARCHAR(32),
    author VARCHAR(32),
    category VARCHAR(32),
);
CREATE TABLE ps_app_detail(
    app_id INTEGER
    version VARCHAR(32),
    platform VARCHAR(32),
    apk_url TEXT,
    apk_size VARCHAR(32),
    pakage_name VARCHAR(32),
    cover VARCHAR(32),
    rating_point VARCHAR(32),
    rating_count VARCHAR(32),
    android_version VARCHAR(32),
    download_times VARCHAR(32),
    description TEXT,
    imgs_url TEXT,
    last_update TEXT,
    primary key (app_id, version, platform)
);

CREATE TABLE ps_status(
    id INTEGER PRIMARY KEY,
    platform VARCHAR(32),
    create_date TEXT,
    crawled_app_count INTEGER,
    new_app_count INTEGER,
    update_app_count INTEGER
);