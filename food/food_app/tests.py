from django.test import TestCase
from django.urls import reverse

from .models import AddTable, ItemOrder, Orders, admin_register, user_register


class PublicFlowTests(TestCase):
    def test_public_pages_and_table_delete_pages_render(self):
        for url_name in ('homepage', 'adminregister', 'adminlogin', 'userregister', 'userlogin'):
            with self.subTest(url_name=url_name):
                self.assertLess(self.client.get(reverse(url_name)).status_code, 500)

        self.assertLess(self.client.get(reverse('deleteTable')).status_code, 500)
        self.assertLess(self.client.get(reverse('staffdeleteTable')).status_code, 500)

    def test_admin_and_user_login_get_requests_redirect_to_forms(self):
        self.assertRedirects(self.client.get(reverse('admin_reg')), reverse('adminregister'))
        self.assertRedirects(self.client.get(reverse('admin_login')), reverse('adminlogin'))
        self.assertRedirects(self.client.get(reverse('user_reg')), reverse('userregister'))
        self.assertRedirects(self.client.get(reverse('user_login')), reverse('userlogin'))

    def test_admin_registration_and_login(self):
        response = self.client.post(reverse('admin_reg'), {
            'adminname': 'Test Admin', 'number': '1234567890',
            'adminid': 'admin01', 'password': 'secret',
        })
        self.assertRedirects(response, reverse('adminlogin'))
        self.assertEqual(admin_register.objects.count(), 1)
        response = self.client.post(reverse('admin_login'), {
            'adminname': 'Test Admin', 'password': 'secret',
        })
        self.assertRedirects(response, reverse('admin_home'))
        self.assertEqual(self.client.session['adminname'], 'Test Admin')

    def test_user_registration_and_login(self):
        response = self.client.post(reverse('user_reg'), {
            'username': 'Test User', 'number': '1234567890', 'password': 'secret',
        })
        self.assertRedirects(response, reverse('userlogin'))
        self.assertEqual(user_register.objects.count(), 1)
        response = self.client.post(reverse('user_login'), {
            'username': 'Test User', 'password': 'secret',
        })
        self.assertRedirects(response, reverse('userHome'))
        self.assertEqual(self.client.session['username'], 'Test User')

    def test_parcel_print_page_renders_without_a_parcel(self):
        response = self.client.get(reverse('print_pracel', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_admin_and_user_dashboards_explain_missing_table_setup(self):
        admin_response = self.client.get(reverse('admin_home'))
        user_response = self.client.get(reverse('userHome'))

        self.assertContains(admin_response, 'No dining tables are configured yet.')
        self.assertContains(admin_response, reverse('add_table'))
        self.assertContains(user_response, 'No dining tables are available yet.')

    def test_open_table_deletion_endpoint(self):
        ItemOrder.objects.create(
            table_name='T1', bill_no='B1', bill_date='2026-01-01', qty=1,
        )
        Orders.objects.create(
            table_name='T1', bill_no='B1', bill_date='2026-01-01', qty=1,
        )
        response = self.client.post(reverse('delete_table'), {'table_name': 'T1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertFalse(ItemOrder.objects.exists())
        self.assertFalse(Orders.objects.exists())

    def test_inventory_table_delete_route_remains_available(self):
        table = AddTable.objects.create(Table_name='T1', Category='Dining')
        response = self.client.get(reverse('delete_table_record', args=[table.pk]))
        self.assertRedirects(response, reverse('view_table'))
        self.assertFalse(AddTable.objects.filter(pk=table.pk).exists())
