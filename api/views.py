# from rest_framework.decorators import api_view#, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.models import Group
# from rest_framework import viewsets, permissions
from api import models, serializers
from django.db import connection
import pandas, json
from django.utils.safestring import SafeString



def index(request):

    df_local = pandas.read_csv('SHEETS.csv', header=1)
    df_local['Date'] = pandas.to_datetime(df_local['Date'], format='%d-%m-%y')

    df_table = df_local[df_local['Date'] == df_local['Date'].max()].groupby('Province').sum()
    df_table = df_table[['Suspected_Cum','Tested_Cum','Confirmed_Cum','Admitted_Cum','Discharged_Cum','Expired_Cum']]

    df_dates = df_local.groupby('Date').sum()

    df_intl = pandas.read_csv('INTL.csv', header=1)
    
    return render(request, 'api/index.html', {
        'summary': dict(df_local.groupby(['Date']).sum().iloc[-1, :][['Suspected_Cum','Tested_Cum','Confirmed_Cum','Admitted_Cum','Discharged_Cum','Expired_Cum']]),
        'table': df_table.to_json(orient='split'),
        'today': df_local['Date'].max().strftime('%d-%m-%Y'),
        'dates': list(df_local['Date'].sort_values().dt.strftime('%d-%m-%Y').unique()),
        'Balochistan': list(df_local[df_local['Province']=='Balochistan'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Pakhtunkhwa': list(df_local[df_local['Province']=='Khyber Pakhtunkhwa'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Punjab': list(df_local[df_local['Province']=='Punjab'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Sindh': list(df_local[df_local['Province']=='Sindh'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Islamabad': list(df_local[df_local['Province']=='Islamabad'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Gilgit': list(df_local[df_local['Province']=='Gilgit-Baltistan'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Kashmir': list(df_local[df_local['Province']=='Azad Kashmir'].groupby(['Date']).sum()['Confirmed_Cum']),
        'Tribal': list(df_local[df_local['Province']=='KP Tribal Districts'].groupby(['Date']).sum()['Confirmed_Cum']),

        'comparison': df_intl.to_json(orient='columns')

    })


# @api_view()
# @permission_classes([IsAuthenticated])
# def cases(request):
#     df_local = pandas.read_sql(query, connection)
#     return Response(df_local.to_json(orient='columns'))

# @api_view()
# @permission_classes([IsAuthenticated])
# def province_status(request):
#     df_local = pandas.read_sql(query, connection)
#     df_local = pandas.crosstab(df_local['Province'], df_local['Status'])
#     return Response(df_local.to_json(orient='columns'))

# @api_view()
# @permission_classes([IsAuthenticated])
# def map(request):
#     df_local = pandas.read_sql(query, connection)
#     c = df_local.groupby('Province').size()
#     return Response(c)

# @api_view()
# @permission_classes([IsAuthenticated])
# def age_gender(request):
#     df_local = pandas.read_sql(query, connection)
#     bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#     labels = ['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100']
#     df_local['binned'] = pandas.cut(df_local['Age'], bins=bins, labels=labels)
#     df_local = pandas.crosstab(df_local.binned, df_local.Gender)
#     return Response(df_local.to_json(orient='columns'))


# @api_view()
# @permission_classes([IsAuthenticated])
# def status(request):
#     df_local = pandas.read_sql(query, connection)
#     return Response(dict(pandas.value_counts(df_local['Status'])))


# @api_view()
# @permission_classes([IsAuthenticated])
# def gender(request):
#     df_local = pandas.read_sql(query, connection)
#     return Response(dict(pandas.value_counts(df_local['Gender'])))


# @api_view()
# @permission_classes([IsAuthenticated])
# def source(request):
#     df_local = pandas.read_sql(query, connection)
#     return Response(dict(pandas.value_counts(df_local['Source'])))

# @api_view()
# @permission_classes([IsAuthenticated])
# def province(request):
#     df_local = pandas.read_sql(query, connection)
#     hist = dict(pandas.value_counts(df_local['Province'], normalize=True))
#     hist.update((x, int(y*100)) for x, y in hist.items())
#     return Response(hist)

# @api_view()
# # @permission_classes([IsAuthenticated])
# def query(request):
#     df_local = pandas.read_csv('SHEETS.csv', header=1)
#     df_local['Date'] = pandas.to_datetime(df_local['Date'], format='%d-%m-%y')

#     if (request.GET):
#         if 'date' in request.GET:
#             df_local = df_local[df_local['Date'] == request.GET.get('date')]
#         if 'province' in request.GET:
#             df_local = df_local[df_local['Province'] == request.GET.get('province')]
#         if 'groupby' in request.GET:
#             df_local = df_local.groupby([request.GET.get('groupby')])

#         if 'measure' in request.GET:
#             if 'aggregate' in request.GET:
#                 aggregate = request.GET.get('aggregate')
#                 if aggregate == 'Sum':
#                     df_local = df_local.sum()[request.GET.get('measure')]
#                 elif aggregate == 'Mean':
#                     df_local = df_local.mean()[request.GET.get('measure')]
#                 else:
#                     return Response('Invalid aggregate method', status=400)
#             else: 
#                 return Response('No aggregate selected', status=400)
#         else:
#             return Response('No measure selected', status=400)

#         if 'groupby' in request.GET:
#             if request.GET.get('groupby') == 'Date':
#                 return Response({x.strftime("%Y-%m-%d"):y for (x,y) in dict(df_local).items()})
#             else:
#                 return Response(dict(df_local))
#         else:
#             return Response(df_local)

#     return Response('No inputs provided', status=400)
    

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = models.User.objects.all().order_by('-date_joined')
#     serializer_class = serializers.UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = serializers.GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = models.Patient.objects.all()
#     serializer_class = serializers.PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class HospitalViewSet(viewsets.ModelViewSet):
#     queryset = models.Hospital.objects.all()
#     serializer_class = serializers.HospitalSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class ProvinceViewSet(viewsets.ModelViewSet):
#     queryset = models.Province.objects.all()
#     serializer_class = serializers.ProvinceSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class CityViewSet(viewsets.ModelViewSet):
#     queryset = models.City.objects.all()
#     serializer_class = serializers.CitySerializer
#     permission_classes = [permissions.IsAuthenticated]


# class StatusViewSet(viewsets.ModelViewSet):
#     queryset = models.Status.objects.all()
#     serializer_class = serializers.StatusSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class SourceViewSet(viewsets.ModelViewSet):
#     queryset = models.Source.objects.all()
#     serializer_class = serializers.SourceSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GenderViewSet(viewsets.ModelViewSet):
#     queryset = models.Gender.objects.all()
#     serializer_class = serializers.GenderSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class LaboratoryViewSet(viewsets.ModelViewSet):
#     queryset = models.Laboratory.objects.all()
#     serializer_class = serializers.LaboratorySerializer
#     permission_classes = [permissions.IsAuthenticated]
