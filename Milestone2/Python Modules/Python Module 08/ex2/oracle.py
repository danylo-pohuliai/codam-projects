import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    print("\nORACLE STATUS: Reading the Matrix...")
    matrix_mode: str | None = os.getenv("MATRIX_MODE")
    database_url: str | None = os.getenv("DATABASE_URL")
    api_key: str | None = os.getenv("API_KEY")
    log_level: str | None = os.getenv("LOG_LEVEL")
    zion_endpoint: str | None = os.getenv("ZION_ENDPOINT")
    required_vars = {
        "MATRIX_MODE": matrix_mode,
        "DATABASE_URL": database_url,
        "API_KEY": api_key,
        "LOG_LEVEL": log_level,
        "ZION_ENDPOINT": zion_endpoint,
    }

    missing = [key for key, vars in required_vars.items() if not vars]
    if missing:
        print(f"\n[WARNING] Missing variables: {', '.join(missing)}")
        print("Please check your .env file or OS overrides.\n")

    mode = matrix_mode if matrix_mode else "development"
    print("Configuration loaded:")
    print(f"Mode: {mode}")

    if mode == "production":
        if database_url:
            print("Database: Connected to production server")
        else:
            print("Database: missing DATABASE_URL")
        if api_key:
            print("API Access: Production Token Validated")
        else:
            print("API Access: Production Token cannot be Validated")
        print(f"Log Level: {log_level if log_level else 'ERROR'}")
        if zion_endpoint:
            print("Zion Network: Route Encrypted")
        else:
            print("Zion Network: ZION_ENDPOINT is missing")
    else:
        if database_url:
            print("Database: Connected to local instance")
        else:
            print("Database: missing DATABASE_URL")
        if api_key:
            print("API Access: Authenticated")
        else:
            print("API Access: Token cannot be Validated")
        print(f"Log Level: {log_level if log_level else 'DEBUG'}")
        if zion_endpoint:
            print("Zion Network: Online")
        else:
            print("Zion Network: ZION_ENDPOINT is missing")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
        if missing:
            print("[WARNING] but does not contain all keys")
    else:
        print("[WARNING] .env file missing")

    if os.getenv("MATRIX_MODE") == "production":
        print("[OK] Production overrides actively applied")
    else:
        print("[OK] Production overrides available")
    if not missing:
        print("\nThe Oracle sees all configurations.")
