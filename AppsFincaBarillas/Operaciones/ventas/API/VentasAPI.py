from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny  
from django.db.models.functions import Concat, Coalesce
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum, Value, CharField, Case, When
from django.db.models import Max
from AppsFincaBarillas.Operaciones.ventas.API.Serializer import VentaSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta
from django.db.models import Count, Value
from django.db.models.functions import Concat


class VentaViewSet(ViewSet):
    permission_classes = [AllowAny]  # Endpoint libre, sin autenticación
    queryset = Venta.objects.all()
    serializer = VentaSerializer

    def list(self, request):
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        venta = Venta.objects.get(pk=pk)
        serializer = VentaSerializer(venta)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        serializer = VentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def update(self, request, pk: int):
        venta = Venta.objects.get(pk=pk)
        serializer = VentaSerializer(instance=venta, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, pk: int):
        venta = Venta.objects.get(pk=pk)
        venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Buscar ventas por método de pago
    @action(methods=['get'], detail=False, url_path='buscar-por-metodo-pago', url_name='buscar_metodo_pago')
    def buscar_por_metodo_pago(self, request):
        metodo = request.query_params.get('metodo', '')
        ventas = Venta.objects.filter(metodo_pago__icontains=metodo)
        serializer = VentaSerializer(ventas, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})

    

    @action(methods=['get'], detail=False, url_path='reporte-ventas-mensual', url_name='reporte_ventas_mes')
    def reporte_ventas_por_mes(self, request):
        # Obtener el último año con ventas
        ultimo_anio = Venta.objects.aggregate(ultimo=Max(ExtractYear('fecha_venta')))['ultimo']

        if not ultimo_anio:
            # No hay ventas registradas
            return Response(
                status=status.HTTP_200_OK,
                data={'reporte': [], 'mensaje': 'No hay ventas registradas.'}
            )

        ventas_mes = (
            Venta.objects
            .filter(fecha_venta__year=ultimo_anio)
            .annotate(
                anio=ExtractYear('fecha_venta'),
                mes_num=ExtractMonth('fecha_venta')
            )
            .values('anio', 'mes_num')
            .annotate(
                total=Sum('monto_total'),
                nombre_mes=Case(
                    When(mes_num=1, then=Value('Enero')),
                    When(mes_num=2, then=Value('Febrero')),
                    When(mes_num=3, then=Value('Marzo')),
                    When(mes_num=4, then=Value('Abril')),
                    When(mes_num=5, then=Value('Mayo')),
                    When(mes_num=6, then=Value('Junio')),
                    When(mes_num=7, then=Value('Julio')),
                    When(mes_num=8, then=Value('Agosto')),
                    When(mes_num=9, then=Value('Septiembre')),
                    When(mes_num=10, then=Value('Octubre')),
                    When(mes_num=11, then=Value('Noviembre')),
                    When(mes_num=12, then=Value('Diciembre')),
                    output_field=CharField(),
                )
            )
            .order_by('anio', 'mes_num')
        )

        return Response(
            status=status.HTTP_200_OK,
            data={'reporte': list(ventas_mes)}
        )

    # Reporte de ventas por método de pago
    @action(methods=['get'], detail=False, url_path='reporte-ventas-metodo', url_name='reporte_metodo_pago')
    def reporte_ventas_por_metodo_pago(self, request):
        ventas_metodo = Venta.objects.values('metodo_pago') \
            .annotate(total_ventas=Sum('monto_total')) \
            .order_by('-total_ventas')

        return Response(status=status.HTTP_200_OK, data={'reporte': ventas_metodo})
     
 
    @action(methods=['get'], detail=False, url_path='reporte-top-clientes', url_name='reporte_top_clientes')
    def reporte_top_clientes(self, request):
        top_clientes = (
            Venta.objects.annotate(
                cliente_concat=Concat(
                    Coalesce('cliente__codigo', Value('')),
                    Value(' - '),
                    Coalesce('cliente__nombres', Value('')),
                    Value(' '),
                    Coalesce('cliente__apellidos', Value(''))
                )
            )
            .values('cliente_concat')
            .annotate(total_ventas=Count('id_venta'))
            .order_by('-total_ventas')[:10]
        )

        return Response(
            status=status.HTTP_200_OK,
            data={
                'reporte': list(top_clientes),
                'mensaje': 'Top 10 clientes con mayor cantidad de ventas'
            }
        )