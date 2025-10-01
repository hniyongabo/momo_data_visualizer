from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from urllib.parse import urlparse
# import transactions
from dsa.parse_sms import parse_sms_backup   

# Load transactions from parsed XML
raw_transactions = parse_sms_backup("data/modified_sms_v2.xml")

# Add root-level 'id' field for easier API access
transactions = []
for tx in raw_transactions:
    if "transaction" in tx and "transaction_id" in tx["transaction"]:
        tx["id"] = tx["transaction"]["transaction_id"]
    transactions.append(tx)

# Hardcoded credentials used in this setup
USERS = {
    "admin": "password123",
    "user": "securepass"
}


def check_auth(header):
    """
    Check if Authorization header contains valid credentials
    for any allowed user.
    """
    if not header or not header.startswith("Basic "):
        return False

    encoded = header.split(" ")[1]
    try:
        decoded = base64.b64decode(encoded).decode()
        user, pw = decoded.split(":", 1)
    except Exception:
        return False

    return USERS.get(user) == pw


class SimpleHandler(BaseHTTPRequestHandler):
    """Handles CRUD operations for MoMo transactions."""

    def _send_auth_required(self):
        """Send 401 Unauthorized response."""
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="MoMo API Transactions"')
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "error": "Unauthorized",
            "message": "Incorrect credentials"
        }).encode())

    # Utility methods

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def _parse_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            raw = self.rfile.read(length)
            return json.loads(raw.decode())
        return {}

    def _parse_path(self):
        """Split path like /transactions/1 into parts."""
        return urlparse(self.path).path.strip("/").split("/")

    
    # GET → Retrieve transactions
    
    def do_GET(self):
        # Check authentication first
        if not check_auth(self.headers.get("Authorization")):
            self._send_auth_required()
            return

        parts = self._parse_path()

        # GET /transactions → all
        if len(parts) == 1 and parts[0] == "transactions":
            self._set_headers()
            self.wfile.write(json.dumps(transactions).encode())

        # GET /transactions/{id} → 1
        elif len(parts) == 2 and parts[0] == "transactions":
            txid = parts[1]
            tx = next((t for t in transactions if t.get("id") == txid), None)
            if tx:
                self._set_headers()
                self.wfile.write(json.dumps(tx).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    
    # POST → Create new transaction
    
    def do_POST(self):
        # Check authentication first
        if not check_auth(self.headers.get("Authorization")):
            self._send_auth_required()
            return
        
        parts = self._parse_path()
        if len(parts) == 1 and parts[0] == "transactions":
            data = self._parse_json_body()
            # Assign next available ID
            existing_ids = [int(t.get("id", 0)) for t in transactions if t.get("id", "").isdigit()]
            new_id = str(max(existing_ids, default=0) + 1)
            data["id"] = new_id
            
            # Setting transaction_id in nested structure if transaction object exists
            if "transaction" not in data:
                data["transaction"] = {}
            data["transaction"]["transaction_id"] = new_id
            
            transactions.append(data)

            self._set_headers(201)
            self.wfile.write(json.dumps(data).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    
    # PUT → Update existing transaction
    
    def do_PUT(self):
        # Check authentication first
        if not check_auth(self.headers.get("Authorization")):
            self._send_auth_required()
            return
        
        parts = self._parse_path()
        if len(parts) == 2 and parts[0] == "transactions":
            txid = parts[1]
            data = self._parse_json_body()
            tx = next((t for t in transactions if t.get("id") == txid), None)

            if tx:
                tx.update(data)  # Merge updates
                tx["id"] = txid
                if "transaction" in tx:
                    tx["transaction"]["transaction_id"] = txid
                    
                self._set_headers()
                self.wfile.write(json.dumps(tx).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    
    # DELETE → Remove transaction
    
    def do_DELETE(self):
        # Check authentication first
        if not check_auth(self.headers.get("Authorization")):
            self._send_auth_required()
            return
        
        parts = self._parse_path()
        if len(parts) == 2 and parts[0] == "transactions":
            txid = parts[1]
            global transactions
            new_transactions = [t for t in transactions if t.get("id") != txid]

            if len(new_transactions) != len(transactions):
                transactions[:] = new_transactions
                self._set_headers(204)  # No Content
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())



# Run the Server

def run(port=8000):
    server = HTTPServer(("", port), SimpleHandler)
    print(f"MoMo API running at http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
