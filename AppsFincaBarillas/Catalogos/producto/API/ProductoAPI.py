from argparse import Action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from AppsFincaBarillas.Catalogos.producto.models import producto
from AppsFincaBarillas.Catalogos.producto.API.Serializer import ProductoSerializer
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto
from rest_framework.decorators import action

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Marca como inactivo en lugar de eliminar
        instance = self.get_object()
        instance.estado = 'Inactivo'
        instance.save()
        return Response({'message': 'Producto marcado como inactivo'}, status=status.HTTP_200_OK)
     
    def delete(self, request, pk: int):
        try:
            prod = producto.objects.get(pk=pk)
            prod.estado = "Inactivo"  # Cambia el estado a Inactivo
            prod.save()
            return Response({"detail": "Producto desactivado correctamente."}, status=status.HTTP_200_OK)
        except producto.DoesNotExist:
            return Response({"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    
    # Rutas adicionales...
    @action(methods=['post'], detail=False)
    def CambiarEstadoProducto(self, request):
        id_producto = request.data.get('IdProducto')
        prod = producto.objects.filter(pk=id_producto).first()
        if prod:
            prod.estado = 'Descontinuado'
            prod.save()
            return Response({'mensaje': 'Producto descontinuado'}, status=status.HTTP_200_OK)
        return Response({'mensaje': 'Producto no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def FiltrarNombreProducto(self, request):
        letra = request.data.get('letra_inicial')
        if letra not in ['P', 'F']:
            return Response({'mensaje': 'La letra inicial debe ser P o F.'}, status=status.HTTP_400_BAD_REQUEST)
        productos = producto.objects.filter(nombre__startswith=letra)
        serializer = ProductoSerializer(productos, many=True)
        return Response({'resultado': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def ReporteProductosDisponibles(self, request):
        total = producto.objects.filter(estado='DISPONIBLE').count()
        return Response({'reporte': {'productos_disponibles': total}}, status=status.HTTP_200_OK)
