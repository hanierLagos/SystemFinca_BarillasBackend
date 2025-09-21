from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.detalleVenta.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion
from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from AppsFincaBarillas.Operaciones.detalleVenta.API.Serializer import DetalleVentaSerializer
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta
from AppsFincaBarillas.Operaciones.detalleVenta.API.Permission import IsAdminOrReadOnly

class DetalleVentaViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

    def list(self, request):
        data = request
        serializer = DetalleVentaSerializer(DetalleVenta.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = DetalleVentaSerializer(DetalleVenta.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        data = request.data
        if isinstance(data, list):
            detalles_creados = []
            errores = []

            for item in data:
                serializer = DetalleVentaSerializer(data=item)
                if serializer.is_valid():
                    producto = serializer.validated_data['producto']
                    cantidad = serializer.validated_data['cantidad_producto']
                    precio = serializer.validated_data['precio_producto']

                    # Validar stock
                    if producto.CantidadDisponible < cantidad:
                        errores.append({
                            'producto': str(producto),
                            'error': f'Sin stock suficiente. Disponible: {producto.CantidadDisponible}'
                        })
                        continue

                    # Calcular sub_total
                    sub_total = float(precio) * cantidad

                    # Restar cantidad al stock
                    producto.CantidadDisponible -= cantidad
                    producto.save()

                    # Crear detalle
                    detalle = DetalleVenta.objects.create(
                        venta=serializer.validated_data['venta'],
                        producto=producto,
                        descripcion=serializer.validated_data['descripcion'],
                        precio_producto=precio,
                        cantidad_producto=cantidad,
                        sub_total=sub_total
                    )
                    detalles_creados.append(DetalleVentaSerializer(detalle).data)
                else:
                    errores.append(serializer.errors)

            if errores:
                return Response({'errores': errores, 'detalles_creados': detalles_creados}, status=status.HTTP_207_MULTI_STATUS)

            return Response(detalles_creados, status=status.HTTP_201_CREATED)

        # Si no es una lista (solo un detalle), tratamos como individual
        serializer = DetalleVentaSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad_producto']
        precio = serializer.validated_data['precio_producto']

        if producto.CantidadDisponible < cantidad:
            raise ValidationError(f'Sin stock suficiente. Disponible: {producto.CantidadDisponible}')

        sub_total = float(precio) * cantidad
        producto.CantidadDisponible -= cantidad
        producto.save()

        detalle = DetalleVenta.objects.create(
            venta=serializer.validated_data['venta'],
            producto=producto,
            descripcion=serializer.validated_data['descripcion'],
            precio_producto=precio,
            cantidad_producto=cantidad,
            sub_total=sub_total
        )

        return Response(DetalleVentaSerializer(detalle).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='top-productos', url_name='top_productos')
    def top_productos_mas_vendidos(self, request):
        top_productos = (
            DetalleVenta.objects
            .values('producto__nombre')
            .annotate(cantidad_vendida=Sum('cantidad_producto'))
            .order_by('-cantidad_vendida')[:10]
        )

        return Response(
            status=status.HTTP_200_OK,
            data={
                'reporte': list(top_productos),
                'mensaje': 'Top 10 productos más vendidos'
            }
        )









