from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .client import BrowserClient
from .serializers import CommandSerializer, NavigateSerializer, \
    ControlSerializer


client = BrowserClient()
client.connect()


class NavigateView(APIView):
    """View for browser navigation"""
    serializer_class = NavigateSerializer
    
    def get(self, _):
        """Get the current url of the browser"""
        data = {
            'command': BrowserClient.GET
        }
        browser_response = client.send(data)
        return Response(browser_response)
    
    def post(self, request):
        """Go to a given url"""
        data = {
            'command': BrowserClient.GOTO,
            'value': request.data.get('url'),
        }
        browser_response = client.send(data)
        if not browser_response.get('ok'):
            return Response(browser_response,
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(browser_response)
    
    
class CommandView(APIView):
    """View for controlling the browser's lifecycle"""
    serializer_class = CommandSerializer
    
    def post(self, request):
        """Send a command to the server
        
        Available commands:
        - Start: start a browser
        - End: close a browser
        - Connect: connect to a server
        """
        command = request.data.get('command')
        
        # Connect command
        if command == 'con':
            try:
                client.connect()
                return Response(dict(ok=True))
            except ConnectionRefusedError:
                return Response(dict(ok=False),
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # Commands handled by the browser server
        else:
            browser_response = client.send(request.data)
            if not browser_response.get('ok'):
                return Response(browser_response,
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(browser_response)
        
        
class ControlView(APIView):
    """View for issuing commands to the media controller"""
    
    serializer_class = ControlSerializer
    
    def post(self, request):
        data = dict(command=BrowserClient.CONTROL)
        data['value'] = request.data.get('action')
        browser_response = client.send(data)
        if not browser_response.get('ok'):
            return Response(browser_response,
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(browser_response)
