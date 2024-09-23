CREATE TABLE dataset_phishing (
	url TEXT,  -- URL string
    source TEXT,  -- Source of the URL
    label TEXT,  -- Category of URL
    url_length INTEGER,  -- URL length in characters
    starts_with_ip BOOLEAN,  -- Is the base URL an IP address?
    url_entropy FLOAT,  -- URL/hostname entropy
    has_punycode BOOLEAN,  -- Does the URL contain at least one punycode character?
    digit_letter_ratio FLOAT,  -- Digit-letter character ratio in URL
    dot_count INTEGER,  -- Count of occurrences of dot (.) inside URL
    at_count INTEGER,  -- Count of occurrences of dot (@) inside URL
    dash_count INTEGER,  -- Count of occurrences of dash (-) inside URL
    tld_count INTEGER,  -- Does the subdirectory in the URL contain top-level domains?
    domain_has_digits BOOLEAN,  -- Does the domain (base URL) contain digits?
    subdomain_count INTEGER,  -- Count of subdomains featured in the base URL
    nan_char_entropy FLOAT,  -- Character entropy of non-alphanumeric characters inside the URL
    has_internal_links BOOLEAN,  -- Does the URL subdirectory contain links?
    whois_data TEXT,  -- Domain WHOIS record
    domain_age_days FLOAT  -- Domain age in days, according to extracted WHOIS record
);

COPY dataset_phishing FROM '/out.csv' DELIMITER ',' CSV HEADER;