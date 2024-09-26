-- Cuenta cuántos registros hay en la tabla dataset_phishing
-- Cuenta un total de 2500000 de registros
SELECT COUNT(*) FROM dataset_phishing;

-- Cuenta cuántos registros tienen valores nulos en la tabla dataset_phishing
-- Cuenta un total de 750689 registros con valores nulos en la tabla dataset_phishing

SELECT COUNT(*) FROM dataset_phishing
        WHERE url IS NULL OR 
              source IS NULL OR 
              label IS NULL OR 
              url_length IS NULL OR 
              starts_with_ip IS NULL OR 
              url_entropy IS NULL OR 
              has_punycode IS NULL OR 
              digit_letter_ratio IS NULL OR 
              dot_count IS NULL OR 
              at_count IS NULL OR 
              dash_count IS NULL OR 
              tld_count IS NULL OR 
              domain_has_digits IS NULL OR 
              subdomain_count IS NULL OR 
              nan_char_entropy IS NULL OR 
              has_internal_links IS NULL OR 
              whois_data IS NULL OR 
              domain_age_days IS NULL;


-- Elimina los registros con valores nulos en la tabla dataset_phishing
DELETE FROM dataset_phishing
        WHERE url IS NULL OR 
              source IS NULL OR 
              label IS NULL OR 
              url_length IS NULL OR 
              starts_with_ip IS NULL OR 
              url_entropy IS NULL OR 
              has_punycode IS NULL OR 
              digit_letter_ratio IS NULL OR 
              dot_count IS NULL OR 
              at_count IS NULL OR 
              dash_count IS NULL OR 
              tld_count IS NULL OR 
              domain_has_digits IS NULL OR 
              subdomain_count IS NULL OR 
              nan_char_entropy IS NULL OR 
              has_internal_links IS NULL OR 
              whois_data IS NULL OR 
              domain_age_days IS NULL;


-- Luego de ejecutar el DELETE, se verifica que no haya registros con valores nulos dando un total de 0 nulos
-- Además, se verifica que el total de registros en la tabla dataset_phishing sea de 1749311 