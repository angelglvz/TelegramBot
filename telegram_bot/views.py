import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .services import send_telegram_message

@csrf_exempt
@require_POST
def telegram_webhook(funct, request):
    """Endpoint que recibe los eventos (updates) enviados por Telegram."""
    try:
        data = json.loads(request.body.decode("utf-8"))
        
        # Verificar si el mensaje contiene texto
        if "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            user_text = message.get("text", "")
            user_first_name = message["from"].get("first_name", "User")

            # Lógica básica de respuestas
            if user_text.startswith("/start"):
                response_text = f"¡Hola, {user_first_name}! Bienvenido a tu bot moderno impulsado por **Django** 🚀."
            elif user_text.startswith("/help"):
                response_text = "Comandos disponibles:\n/start - Iniciar el bot\n/help - Ver esta ayuda"
            else:
                response_text = f"Has dicho: *{user_text}*. ¡Procesado correctamente desde el backend!"

            send_telegram_message(chat_id, response_text)

        return JsonResponse({"status": "ok"}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)