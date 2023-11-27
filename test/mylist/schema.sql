
CREATE TABLE IF NOT EXISTS item (
        item_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
		priority_value INTEGER,
        FOREIGN KEY (user_id)
                REFERENCES users (user_id)
);
