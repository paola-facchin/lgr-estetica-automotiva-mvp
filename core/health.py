"""Verificação de disponibilidade da aplicação e da conexão com o banco de dados."""
from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_safe


@require_safe
def health(request):
    """Retorna 200 somente se o Django e o banco responderem corretamente."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        response = JsonResponse({"status": "indisponivel"}, status=503)
    else:
        response = JsonResponse({"status": "ok"}, status=200)
    response["Cache-Control"] = "no-store"
    return response
