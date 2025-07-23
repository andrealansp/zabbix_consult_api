import traceback

from rest_framework import views, response, status
from rest_framework.permissions import IsAuthenticated

from .common.zabbixhandler import ZabbixHandler


# Create your views here.
class TriggersActivesView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            zapi = ZabbixHandler()
            token = zapi.login()
            triggers = zapi.get_only_true_triggers(token)
            triggers_actives_host: str = ""

            for trigger in triggers:
                triggers_actives_host[trigger["hosts"][0]["host"]] = []

            if triggers:
                for trigger in triggers:
                    host = trigger["hosts"][0]["host"] if trigger.get("hosts") else "Desconhecido"
                    triggers_actives_host = f"*{host}* \n {trigger['description']} - Status: {trigger['value']} \n "

                return response.Response(
                    data={
                        "message": "Triggers ativas encontradas com sucesso.",
                        "triggers": triggers_actives_host
                    },
                    status=status.HTTP_200_OK)
            else:
                return response.Response(
                    data={
                        "message": "Nenhuma trigger ativa encontrada.",
                        "triggers": {}
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return response.Response(
                data={"message": f"Erro interno do servidor:{e.__str__()}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TriggersDescriptionView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            dados = request.data
            zapi = ZabbixHandler()
            token = zapi.login()
            triggers = zapi.get_active_triggers_by_description(token, partial_description=dados["partial_description"])
            triggers_by_description: str = ""

            if triggers:
                for trigger in triggers:
                    host = trigger["hosts"][0]["host"] if trigger.get("hosts") else "Desconhecido"
                    triggers_by_description += f"*{host}* \n {trigger['description']} - Status: {trigger['value']} \n "
                return response.Response(
                    data={
                        "message": "Triggers encontradas pela descrição parcial com sucesso.",
                        "triggers": triggers_by_description
                    },
                    status=status.HTTP_200_OK)
            else:
                return response.Response(
                    data={
                        "message": "Nenhuma trigger ativa encontrada com a descrição fornecida.",
                        "triggers": {}
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            erro_str = traceback.format_exc()
            print(erro_str)
            return response.Response(
                data={"message": f"Erro interno do servidor: {e.__str__()}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TriggersHostView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            dados = request.data
            zapi = ZabbixHandler()
            token = zapi.login()
            triggers = zapi.get_triggers_by_host(token, host=dados["host"])
            triggers_actives_host: dict[str:any] = []
            mensagem_retorno = ""

            for trigger in triggers:
                triggers_actives_host[trigger["hosts"][0]["host"]] = []

            if triggers:
                for trigger in triggers:
                    mensagem_retorno += f"{trigger['description']} - Status: {trigger['value']} \n "

                return response.Response(
                    data={
                        "message": "Triggers ativas encontradas com sucesso.",
                        "triggers": mensagem_retorno
                    },
                    status=status.HTTP_200_OK)
            else:
                return response.Response(
                    data={
                        "message": "Nenhuma trigger ativa encontrada.",
                        "triggers": {}
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return response.Response(
                data={"message": f"Erro interno do servidor:{e.__str__()}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
