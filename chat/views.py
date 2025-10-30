from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

# WARNING: Insecure to store key in code for production.
# Use environment variable or user-specific keys.
AES_KEY = os.environ.get("AES_KEY", "ThisIsASecretKey").encode("utf-8")  # 16/24/32 bytes

def index(request):
    # Render page with client encryption UI
    return render(request, "index.html", {"aes_key_hint": "16-char secret (for demo). Do not hardcode in prod."})

@csrf_exempt
def receive_encrypted(request):
    # POST JSON: { "payload": "<base64 iv+ciphertext>" }
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    try:
        import json
        body = json.loads(request.body.decode("utf-8"))
        payload_b64 = body.get("payload")
        if not payload_b64:
            return HttpResponseBadRequest("payload missing")

        raw = base64.b64decode(payload_b64)
        if len(raw) < AES.block_size:
            return HttpResponseBadRequest("invalid payload")

        iv = raw[:AES.block_size]
        ciphertext = raw[AES.block_size:]

        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        text = decrypted.decode("utf-8")

        # For demo, return plaintext. In a real app store or process it securely.
        return JsonResponse({"status": "ok", "plaintext": text})
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)}, status=400)
