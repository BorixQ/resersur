#orders/urls.py
from django.urls import path
from orders.views.workorder import WorkOrderListCreateView, WorkOrderDetailView
from orders.views.evaluations import DamageEvaluationListCreateView, DamageEvaluationDetailView
from orders.views.photos import OTPhotoListCreateView, OTPhotoDetailView

from orders.views.quotations import QuotationListView, QuotationDetailView
from orders.views.history import OTStatusHistoryListView, OTStatusHistoryDetailView

urlpatterns = [
    path('workorders/', WorkOrderListCreateView.as_view(), name='workorder-list'),
    path('workorders/<int:pk>/', WorkOrderDetailView.as_view(), name='workorder-detail'),

    path('evaluations/', DamageEvaluationListCreateView.as_view(), name='evaluation-list'),
    path('evaluations/<int:pk>/', DamageEvaluationDetailView.as_view(), name='evaluation-detail'),

    path('photos/', OTPhotoListCreateView.as_view(), name='photo-list'),
    path('photos/<int:pk>/', OTPhotoDetailView.as_view(), name='photo-detail'),

    path('quotations/', QuotationListView.as_view(), name='quotation-list'),
    path('quotations/<int:pk>/', QuotationDetailView.as_view(), name='quotation-detail'),

    path('history/', OTStatusHistoryListView.as_view(), name='history-list'),
    path('history/<int:pk>/', OTStatusHistoryDetailView.as_view(), name='history-detail'),

]

