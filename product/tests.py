from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User, Product, Shop
from model_mommy import mommy

# Create your tests here.


class TestShopConfirmedList(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)

        mommy.make(Shop, seller=self.user,type='HY', is_confirmed=True)
        mommy.make(Shop, seller=self.user,type='CS', is_confirmed=True)
        mommy.make(Shop, seller=self.user,type='SU', is_confirmed=False)


    def test_shop_confirmed_show(self):
        url = reverse('shopConfirmed')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_confirmed_unauthorized(self):
        url = reverse('shopConfirmed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_confirmed_count(self):
        url = reverse('shopConfirmed')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)
    
    def test_shop_confirmed_filter_null(self):
        url = reverse('shopConfirmed')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'type': 'SU'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 0)

    def test_shop_confirmed_filter(self):
        url = reverse('shopConfirmed')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'type': 'CS'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)


class TestShoptypes(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)

        mommy.make(Shop, seller=self.user,type='HY', is_confirmed=True)
        mommy.make(Shop, seller=self.user,type='VS', is_confirmed=True)
        mommy.make(Shop, seller=self.user,type='CS', is_confirmed=True)
        mommy.make(Shop, seller=self.user,type='SU', is_confirmed=False)
        mommy.make(Shop, seller=self.user,type='FS', is_confirmed=False)
        mommy.make(Shop, seller=self.user,type='OS', is_confirmed=False)

    def test_shop_types(self):

        url = reverse('shopTypes')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_types_unauthorized(self):
        url = reverse('shopTypes')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_types_count(self):
        url = reverse('shopTypes')
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 3)


class TestShopProducts(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.shop1 = mommy.make(Shop, seller=self.user, name='Tehran', type = 'HY', is_confirmed=True)
        self.shop2 = mommy.make(Shop, seller=self.user, name='Iran',   type='OS', is_confirmed=True)
        self.shop3 = mommy.make(Shop, seller=self.user, name='Plus',   type='SU', is_confirmed=False)

        self.product1 = mommy.make(Product, price=5,  stock=5, shop=self.shop1, is_active=True)
        self.product2 = mommy.make(Product, price=15, stock=5, shop=self.shop1, is_active=True)
        self.product3 = mommy.make(Product, price=25, stock=5, shop=self.shop2, is_active=True)
        self.product4 = mommy.make(Product, price=35, stock=0, shop=self.shop2, is_active=True)
        self.product5 = mommy.make(Product, price=45, stock=5, shop=self.shop2, is_active=False)
        self.product6 = mommy.make(Product, price=55, stock=0, shop=self.shop3, is_active=False)

    def test_shop_product_list(self):
        url = reverse('shopProducts', args=['tehran_hy'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_product_list_unauthorized(self):
        url = reverse('shopProducts', args=['tehran_hy'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 401)
    
    def test_shop_product_count(self):
        url = reverse('shopProducts', args=['tehran_hy'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 2)

    def test_shop_product_filter_tag(self):
        url = reverse('shopProducts', args=['iran_os'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'tag':1})
        self.assertEqual(resp.status_code, 200)

    def test_shop_product_filter_gt(self):
        url = reverse('shopProducts', args=['iran_os'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'price__gt':20})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 3)

    def test_shop_product_filter_lt(self):
        url = reverse('shopProducts', args=['iran_os'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'price__lt':30})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_shop_product_filter_is_active_true(self):
        url = reverse('shopProducts', args=['iran_os'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'available':True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)

    def test_shop_product_filter_is_active_false(self):
        url = reverse('shopProducts', args=['plus_su'])
        self.client.force_authenticate(self.user)
        resp = self.client.get(url, {'available':True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 0)
