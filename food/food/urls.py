"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from food_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index,name='index'),
    path('index1',views.index1,name='index1'),

    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_nav',views.admin_nav,name='admin_nav'),
    path('register',views.register,name='register'),
    path('register_list',views.register_list,name='register_list'),
    path('delete_register/<int:pk>', views.delete_register, name='delete_register'),


    path('add_item',views.add_item,name='add_item'),
    path('view_item/', views.view_item, name='view_item'),
    path('edit_item/<int:pk>', views.edit_item, name='edit_item'),
    path('delete_item_list/<int:pk>', views.delete_item_list, name='delete_item_list'),

    path('add_table', views.add_table, name='add_table'),
    path('view_table', views.view_table, name='view_table'),
    path('edit_table/<int:pk>', views.edit_table, name='edit_table'),

    path('add_company', views.add_company, name='add_company'),
    path('view_company', views.view_company, name='view_company'),
    path('edit_company/<int:pk>', views.edit_company, name='edit_company'),
    path('delete_company/<int:pk>', views.delete_company, name='delete_company'),

    path('add_order',views.add_order,name='add_order'),
    path('fetch_table_data/', views.fetch_table_data, name='fetch_table_data'),
    path('item/<str:item_code>/', views.fetch_item_details, name='fetch_item_details'),
    path('save_order',views.save_order,name='save_order'),

    path('exchange_tbl/',views.exchange_tbl,name='exchange_tbl'),
    path('print_table/',views.print_table,name='print_table'),
    path('print_bill/',views.print_bill,name='print_bill'),

    path('settle_table', views.settle_table, name='settle_table'),
    path('settle_bill/<str:table_name>', views.settle_bill, name='settle_bill'),

    path('userHome', views.userHome, name='userHome'),
    path('add_order_user',views.add_order_user,name='add_order_user'),
    path('save_order_user',views.save_order_user,name='save_order_user'),
    path('parcel',views.parcel,name='parcel'),
    path('save_pracel_user',views.save_pracel_user,name='save_pracel_user'),
    path('print_pracel/<int:bill_no>/', views.print_pracel, name='print_pracel'),

    path('delete_print_bill/<int:bill_no>/', views.print_bill_delete, name='print_bill_delete'),
    path('delete_print_bill_user/<int:bill_no>/', views.print_bill_delete_user, name='print_bill_delete_user'),
    path('settle_bill_delete/<int:bill_no>/', views.settle_bill_delete, name='settle_bill_delete'),
    path('settle_bill_delete_user/<int:bill_no>/', views.settle_bill_delete_user, name='settle_bill_delete_user'),


    path('sales_report',views.sales_report,name='sales_report'),
    path('parcelReport',views.parcelReport,name='parcelReport'),
    path('item_report',views.item_report,name='item_report'),
    path('daily_report',views.daily_report,name='daily_report'),

    path('exchange_tbl_user',views.exchange_tbl_user,name='exchange_tbl_user'),
    path('print_table_user/',views.print_table_user,name='print_table_user'),
    path('print_bill_user/',views.print_bill_user,name='print_bill_user'),

    path('settle_table_user', views.settle_table_user, name='settle_table_user'),
    path('settle_bill_user/<str:table_name>', views.settle_bill_user, name='settle_bill_user'),

    path('checkTablesUser', views.checkTablesUser, name='checkTablesUser'),
    path('checkItemsUser/', views.checkItemsUser, name='checkItemsUser'),

    path('checkTables', views.checkTables, name='checkTables'),
    path('checkItems/', views.checkItems, name='checkItems'),

    path('addExpenses', views.addExpenses, name='addExpenses'),
    path('saveExpenses', views.saveExpenses, name='saveExpenses'),
    path('viewExpenses', views.viewExpenses, name='viewExpenses'),

    path('get_staff_name', views.get_staff_name, name='get_staff_name'),
    path('salary', views.salary, name='salary'),
    path('saveSalary', views.saveSalary, name='saveSalary'),
    path('viewSalary', views.viewSalary, name='viewSalary'),

    path('profit_report', views.profit_report, name='profit_report'),

    path('purchase', views.purchase, name='purchase'),
    path('purchaseUpdate', views.purchaseUpdate, name='purchaseUpdate'),
    path('purchaseList', views.purchaseList, name='purchaseList'),
    path('updateStock/<int:pk>', views.updateStock, name='updateStock'),
    path('purchaseEdit/<int:pk>', views.purchaseEdit, name='purchaseEdit'),
    path('delete_purchase/<int:pk>/', views.delete_purchase, name='delete_purchase'),

    path('get_table_details/', views.get_table_details, name='get_table_details'),
    path('billPending/', views.billPending, name='billPending'),
    path('billPendingUser/', views.billPendingUser, name='billPendingUser'),

    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('delete_item_user/<int:item_id>/', views.delete_item_user, name='delete_item_user'),
    path('editStaff/<int:pk>/', views.editStaff, name='editStaff'),

    path('pending-bills_user/', views.pending_bills_view_user, name='pending_bills_user'),
    path('edit-bill_user/<int:pk>/', views.edit_bill_user, name='edit_bill_user'),
    path('delete-bill_user/<int:pk>/', views.delete_bill_user, name='delete_bill_user'),
    path('viewSalaryHistory/<str:pk>/', views.viewSalaryHistory, name='viewSalaryHistory'),
    path('pendingReport', views.pendingReport, name='pendingReport'),
    path('get_name', views.get_name, name='get_name'),
    path('get-item-suggestions/', views.get_item_suggestions, name='get_item_suggestions'),
    path('get-item-details/', views.get_item_details, name='get_item_details'),

    path('update-bill-status/<int:bill_id>/', views.update_bill_status, name='update_bill_status'),
    path('purchaseReport', views.purchaseReport, name='purchaseReport'),
    path('pending-bills/', views.pending_bills_view, name='pending_bills'),
    path('edit-bill/<int:pk>/', views.edit_bill, name='edit_bill'),
    path('delete-bill/<int:pk>/', views.delete_bill, name='delete_bill'),
    path('usersaveExpenses', views.usersaveExpenses, name='usersaveExpenses'),
    path('userExpenses', views.userExpenses, name='userExpenses'),
    path('userViewExpenses', views.userViewExpenses, name='userViewExpenses'),
    path('deleteReport', views.deleteReport, name='deleteReport'),
    path('usersalesReport', views.usersalesReport, name='usersalesReport'),
    path('itempurchaseReport',views.itempurchaseReport,name='itempurchaseReport'),
    path('update_qty/<int:item_id>/', views.update_qty, name='update_qty'),
    path('tableReport', views.tableReport, name='tableReport'),
    path('itemReportUser', views.itemReportUser, name='itemReportUser'),
    path('purchaseUser', views.purchaseUser, name='purchaseUser'),
    path('purchaseListUser', views.purchaseListUser, name='purchaseListUser'),
    path('purchaseUpdateUser', views.purchaseUpdateUser, name='purchaseUpdateUser'),
    path('updatestockUser/<int:pk>', views.updatestockUser, name='updatestockUser'),
    path('delete_table/', views.delete_table, name='delete_table'),
    path('delete_table/<int:pk>', views.delete_table_record, name='delete_table_record'),
    path('deleteTable',views.deleteTable,name='deleteTable'),
    path('staffdelete_table/', views.staffdelete_table, name='staffdelete_table'),
    path('staffdeleteTable',views.staffdeleteTable,name='staffdeleteTable'),

    path('',views.homepage,name='homepage'),
    path('hotelslist',views.hotelslist,name='hotelslist'),
    path('food_view',views.food_view,name='food_view'),
    path('room_view',views.room_view,name='room_view'),
    path('order_room',views.order_room,name='order_room'),

    path('adminregister', views.adminregister, name='adminregister'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('admin_reg', views.admin_reg, name='admin_reg'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admins', views.admins, name='admins'),
    path('delete/1/<int:id>/', views.delete_admins, name='delete_admins'),
    path('edit/16/<int:id>', views.edit_admin, name='edit_admin'),

    path('userlogin', views.userlogin, name='userlogin'),
    path('userregister', views.userregister, name='userregister'),
    path('user_reg', views.user_reg, name='user_reg'),
    path('user_login', views.user_login, name='user_login'),
    path('users', views.users, name='users'),
    path('delete/2/<int:id>/', views.delete_users, name='delete_users'),
    path('edit/3/<int:id>', views.edit_user, name='edit_user'),

    path('nav',views.nav,name='nav'),
    path('index2',views.index2,name='index2'),

    path('bookregister',views.bookregister,name='bookregister'),
    path('bookregister_form', views.bookregister_form, name='bookregister_form'),
    path('bookregister/list/', views.bookregister_list, name='bookregister_list'),
    # path('bookregister/edit/<int:pk>/', views.bookregister_edit, name='bookregister_edit'),
    path('bookregister/delete/<int:pk>/', views.bookregister_delete, name='bookregister_delete'),
    path('bookregister/edit/1/<int:pk>/', views.bookregister_edit, name='bookregister_edit'),

    path('booklogin',views.booklogin,name='booklogin'),
    path('book_login',views.book_login,name='book_login'),

    path('register/', views.register_room, name='register_room'),
    path('list/', views.room_list, name='room_list'),
    path('bookings/<int:pk>/delete/', views.delete_booking, name='delete_booking'),
    path('bookings/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('room_register',views.room_register,name='room_register'),
    path('booking_success',views.booking_success,name='booking_success'),

    path('addroom', views.addroom, name='addroom'),
    path('admin_room', views.admin_room, name='admin_room'),
    path('room', views.room, name='room'),
    path('rooms/<int:id>/delete/', views.delete_inventory_room, name='delete_inventory_room'),
    path('rooms/<int:id>/edit/', views.edit_inventory_room, name='edit_inventory_room'),

]
