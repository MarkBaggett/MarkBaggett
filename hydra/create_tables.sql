CREATE TABLE classes (
 class text PRIMARY KEY,
 interface text NOT NULL,
 addresses text NOT NULL,
);

CREATE TABLE rooms (
 room text PRIMARY KEY,
 subnet text NOT NULL
);

CREATE TABLE enabled (
 roomclass text PRIMARY KEY
);

