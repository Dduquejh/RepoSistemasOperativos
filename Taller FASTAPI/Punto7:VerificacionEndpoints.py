import requests

BASE_URL = "http://127.0.0.1:8000"

# Verificar endpoint GET /dataset
def test_get_dataset(page, limit, age_days=None):
    url = f"{BASE_URL}/dataset?page={page}&limit={limit}"

    # Agregar el parámetro age_days a la URL si se proporciona
    if age_days is not None:
        url += f"&age_days={age_days}"

    response = requests.get(url)

    print(f"STATUS: GET /dataset?page={page}&limit={limit}{'&age_days=' + str(age_days) if age_days is not None else ''} - Status Code: {response.status_code}")

    if response.status_code == 200:
        print("GET /dataset: OK")
    elif response.status_code == 404:
        print("GET /dataset: No records found")
    elif response.status_code == 422:
        print("GET /dataset: Invalid request body")
    else:
        print("GET /dataset: Error")

# Verificar endpoint POST /dataset
def test_post_dataset(datasets):
    url = f"{BASE_URL}/dataset"
    response = requests.post(url, json=datasets)

    print(f"STATUS: POST /dataset - Status Code: {response.status_code}")
    print("Response:", response.json() if response.status_code in (200, 400, 422) else response.text)

    if response.status_code == 200:
        print("POST /dataset: OK")
    elif response.status_code == 400:
        print("POST /dataset: No dataset provided")
    elif response.status_code == 422:
        print("POST /dataset: Invalid request body")
    else:
        print("POST /dataset: Error")

# Run tests
def run_test():
    print("Running tests...")

    print("\nTEST GET /dataset")
    # Test GET /dataset correcto
    print("Correcto")
    test_get_dataset(1, 100)

    # Test GET /dataset sin registros
    print("Sin obtener registros")
    test_get_dataset(19000, 100)

    # Test GET /dataset con errores en el request body
    # No hay página -1 y el máximo de registros es 100
    print("Con errores en el request body")
    test_get_dataset(-1, 200) 

    # Test GET /dataset con filtro age_days
    print("Correcto")
    test_get_dataset(1, 100, 30)

    # Test GET /dataset con un valor de age_days muy grande (devuelve vacío)
    print("Sin dataset")
    test_get_dataset(1, 100, 100000)

    # Test GET /dataset con un valor de age_days inválido
    print("Incorrecto")
    test_get_dataset(1, 100, -1)

    print("\nTEST POST /dataset")
    # Test POST /dataset correcto
    valid_dataset = [
            {
                "url": "http://malicious-site.org",
                "source": "automatic",
                "label": "phishing",
                "url_length": 25,
                "starts_with_ip": False,
                "url_entropy": 3.8,
                "has_punycode": False,
                "digit_letter_ratio": 1.5,
                "dot_count": 3,
                "at_count": 0,
                "dash_count": 0,
                "tld_count": 1,
                "domain_has_digits": True,
                "subdomain_count": 0,
                "nan_char_entropy": 0.30,
                "has_internal_links": False,
                "whois_data": "invalid",
                "domain_age_days": 120
            },
            {
                "url": "http://safe-site.org",
                "source": "manual",
                "label": "safe",
                "url_length": 20,
                "starts_with_ip": False,
                "url_entropy": 3.2,
                "has_punycode": False,
                "digit_letter_ratio": 1.0,
                "dot_count": 2,
                "at_count": 0,
                "dash_count": 0,
                "tld_count": 1,
                "domain_has_digits": False,
                "subdomain_count": 0,
                "nan_char_entropy": 0.20,
                "has_internal_links": False,
                "whois_data": "valid",
                "domain_age_days": 365
            }
        ]
    print("Correcto")
    test_post_dataset(valid_dataset)

    # Test POST /dataset sin dataset
    no_dataset = []
    print("Sin dataset")
    test_post_dataset(no_dataset)

    # Test POST /dataset con errores en el request body
    invalid_dataset = [
            {
                "url": "http://malicious-site.org",
                "source": "automatic",
                "label": "phishing",
                "url_length": 25,
                "starts_with_ip": False,
                "url_entropy": 3.8,
                "has_punycode": False,
                "digit_letter_ratio": 1.5,
                "domain_has_digits": True,
                "subdomain_count": 0,
                "nan_char_entropy": 0.30,
                "has_internal_links": False
            },
        ]
    print("Con errores en el request body")
    test_post_dataset(invalid_dataset)

    print("\nTests finished")

    


if __name__ == "__main__":
    run_test()

    
        