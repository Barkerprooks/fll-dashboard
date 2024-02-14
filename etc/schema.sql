CREATE TABLE IF NOT EXISTS team (
    group_name TEXT UNIQUE,
    robot_name TEXT UNIQUE,
    image TEXT,
    created INTEGER DEFAULT(UNIXEPOCH()),
    updated INTEGER DEFAULT(UNIXEPOCH())
);

CREATE TABLE IF NOT EXISTS member (
    name TEXT UNIQUE,
    color TEXT,
    teamid INTEGER, -- fk on team
    created INTEGER DEFAULT(UNIXEPOCH()),
    updated INTEGER DEFAULT(UNIXEPOCH())
);

CREATE TABLE IF NOT EXISTS run (
    robot_slot INTEGER,
    title TEXT,
    teamid INTEGER, -- fk on team
    version TEXT DEFAULT('1.0.0'),
    created INTEGER DEFAULT(UNIXEPOCH()),
    updated INTEGER DEFAULT(UNIXEPOCH()),
    CONSTRAINT UC_run UNIQUE(robot_slot, teamid)
);

-- join table for missions on runs
-- "a run's mission"
CREATE TABLE IF NOT EXISTS run_mission (
    missionid INTEGER,
    runid INTEGER,
    created INTEGER DEFAULT(UNIXEPOCH())
);

-- join table for runs and members of those runs
-- "a run's member"
CREATE TABLE IF NOT EXISTS run_member (
    memberid INTEGER,
    runid INTEGER,
    created INTEGER DEFAULT(UNIXEPOCH())
);