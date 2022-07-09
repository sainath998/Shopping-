from django.urls import path

from .views import (
    renderDashboard,
    renderCustomerPage,
    renderProductsPage,
    createOrder,
    updateOrder,
    deleteOrder,
    loginView,
    register,
    logoutView,
    userHome,
    updateProfile,
    customerCreateOrder,
    updateCustomerProfile,
)

urlpatterns = [
    path('', renderDashboard, name='dashboard'),
    path('userHome/', userHome, name='user-home'),
    path('products/', renderProductsPage, name='products'),
    path('customer/<str:cust_pk_id>/', renderCustomerPage, name='customer-unique'),
    path('createOrder/<str:cust_pk_id>/', createOrder, name='create-order'),
    path('customerCreateOrder/<str:customerId>/', customerCreateOrder, name='customer-create-order'),
    path('updateOrder/<str:order_pk_id>/', updateOrder, name='update-order'),
    path('deleteOrder/<str:order_pk_id>/', deleteOrder, name='delete-order'),
    path('logout/', logoutView, name='logout'),
    path('login/', loginView, name='login'),
    path('register/', register, name='register'),
    path('updateProfile/', updateProfile, name='update-profile'),
    path('updateCustomerProfile/<str:customerId>', updateCustomerProfile, name='update-customer-profile'),
]