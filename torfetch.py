import argparse
import sys
import requests
from pathlib import Path

# ✅ Check for SOCKS support
def check_socks_support():
    try:
        import socks  # PySocks
    except ImportError:
        print("❌ Missing dependency: PySocks is required for SOCKS proxy support.")
        print("💡 Fix it by running: pip install requests[socks]")
        sys.exit(1)

# 📥 Download logic
def download_files(base_url, path_file, output_dir, proxy_port):
    proxies = {
        'http': f'socks5h://127.0.0.1:{proxy_port}',
        'https': f'socks5h://127.0.0.1:{proxy_port}'
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(path_file, 'r') as f:
        paths = [line.strip() for line in f if line.strip()]

    for path in paths:
        full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        filename = path.split("/")[-1] or "downloaded_file"

        try:
            response = requests.get(full_url, proxies=proxies, timeout=30)
            response.raise_for_status()
            with open(output_path / filename, 'wb') as file:
                file.write(response.content)
            print(f"✅ Downloaded: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} — {e}")

# 🚀 CLI entry point
def main():
    check_socks_support()

    parser = argparse.ArgumentParser(description="Download files from .onion URLs via Tor")
    parser.add_argument("base_url", help="Base .onion URL (e.g. http://abc123.onion)")
    parser.add_argument("path_file", help="Text file containing relative paths")
    parser.add_argument("-o", "--output", default="tor_downloads", help="Output directory")
    parser.add_argument("-p", "--port", type=int, default=9050, help="Tor SOCKS proxy port (default: 9050)")

    args = parser.parse_args()
    download_files(args.base_url, args.path_file, args.output, args.port)

if __name__ == "__main__":
    main()