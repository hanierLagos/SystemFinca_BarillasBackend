from xml.dom import NotFoundErr
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.cliente.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Catalogos.cliente.API.Serializer import ClienteSerializer
from AppsFincaBarillas.Catalogos.cliente.models import Cliente
from AppsFincaBarillas.Catalogos.cliente.API.Permission import IsAdminOrReadOnly
from rest_framework.renderers import JSONRenderer




class ClienteViewSet(ViewSet):
    #permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Cliente.objects.all()
    serializer = ClienteSerializer

    renderer_classes = [JSONRenderer]


    def list(self, request):
        serializer = ClienteSerializer(Cliente.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        try:
         cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
         raise NotFoundErr(detail="Cliente no encontrado")
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)


    def create(self, request):
        codigo = request.data.get('codigo')
        if Cliente.objects.filter(codigo=codigo).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'mensaje': f'Ya existe un cliente con el código {codigo}.'}
            )
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    
    # Actualizar Cliente
    def update(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(instance=cliente, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        try:
            cliente = Cliente.objects.get(pk=pk)
            cliente.estado = 0  # Cambia el estado a 0
            cliente.save()
            return Response({"detail": "Cliente desactivado correctamente."}, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    #LOS MIOS allan

    # Actualizar nombre de cliente por código
    @action(methods=['post'], detail=False, url_path='actualizar-nombre-por-codigo')
    def actualizar_nombre_por_codigo(self, request):
        codigo = request.data.get('codigo')
        nuevo_nombre = request.data.get('Nombre')
        cliente = Cliente.objects.filter(codigo=codigo).first()
        if cliente:
            cliente.Nombre = nuevo_nombre
            cliente.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Nombre actualizado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Cliente no encontrado'})

   # ✅ Buscar por nombre
    @action(detail=False, methods=['get'], url_path='buscar-por-nombre')
    def buscar_por_nombre(self, request):
        nombre = request.query_params.get('nombre')
        if not nombre:
            return Response({'mensaje': 'Debe proporcionar un nombre.'}, status=status.HTTP_400_BAD_REQUEST)
        clientes = Cliente.objects.filter(Nombre__icontains=nombre)
        if clientes.exists():
            return Response(ClienteSerializer(clientes, many=True).data)
        return Response({'mensaje': 'No se encontraron clientes con ese nombre.'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Buscar por dirección
    @action(detail=False, methods=['get'], url_path='buscar-por-direccion')
    def buscar_por_direccion(self, request):
        direccion = request.query_params.get('direccion')
        if not direccion:
            return Response({'mensaje': 'Debe proporcionar una dirección.'}, status=status.HTTP_400_BAD_REQUEST)
        clientes = Cliente.objects.filter(Direccion__icontains=direccion)
        if clientes.exists():
            return Response(ClienteSerializer(clientes, many=True).data)
        return Response({'mensaje': 'No se encontraron clientes con esa dirección.'}, status=status.HTTP_404_NOT_FOUND)










