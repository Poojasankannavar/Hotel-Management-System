from django.db import models

# Create your models here.


class UserReg(models.Model):
    usertype=models.CharField(max_length=50,null=True)
    username=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    number=models.CharField(max_length=50,null=True)

class AddItem(models.Model):
    qty=models.IntegerField(null=True, blank=True)
    dqty=models.IntegerField(null=True, blank=True)
    Item_name=models.CharField(max_length=20,null=True)
    Item_code=models.CharField(max_length=10,null=True)
    Item_price=models.FloatField(max_length=10,null=True)
    item_cat=models.CharField(max_length=10,null=True)

class Purchase(models.Model):
    qty=models.IntegerField(null=True)
    Item_name=models.CharField(max_length=20,null=True)
    Item_price=models.FloatField(max_length=10,null=True)
    Item_code=models.CharField(max_length=10,null=True)
    item_cat=models.CharField(max_length=10,null=True)
    date = models.DateField(null=True)


class AddTable(models.Model):
    Table_name=models.CharField(max_length=10,null=True)
    Category=models.CharField(max_length=10,null=True)



class AddCompany(models.Model):
    Company_name=models.CharField(max_length=20,null=True)
    Company_address=models.CharField(max_length=50,null=True)
    Company_GST=models.CharField(max_length=10,null=True)
    Company_number=models.CharField(max_length=10,null=True)

class ItemOrder(models.Model):
    table_name = models.CharField(max_length=10,null=True)
    bill_no = models.CharField(max_length=10,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=10,null=True)
    item_name = models.CharField(max_length=10,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    item_cat= models.CharField(max_length=10,null=True)

class Orders(models.Model):
    table_name = models.CharField(max_length=10,null=True)
    bill_no = models.CharField(max_length=10,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=10,null=True)
    item_name = models.CharField(max_length=10,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.FloatField(null=True)
    item_cat = models.CharField(max_length=10, null=True)

class Printorders(models.Model):
    table_name = models.CharField(max_length=10,null=True)
    bill_no = models.CharField(max_length=10,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=10,null=True)
    item_name = models.CharField(max_length=10,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    item_cat = models.CharField(max_length=10, null=True)


class Pracel(models.Model):
    bill_no = models.CharField(max_length=10,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=10,null=True)
    item_name = models.CharField(max_length=10,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    pracel_charge = models.DecimalField(max_digits=10, decimal_places=2,null=True)

class Expenses(models.Model):
    Date=models.DateField(null=True)
    Reason=models.CharField(max_length=150,null=True)
    Amount=models.CharField(max_length=20,null=True)
    staffname = models.CharField(max_length=20, null=True)

class Salary(models.Model):
    Date=models.DateField(null=True)
    desc=models.CharField(max_length=150,null=True)
    Amount=models.CharField(max_length=20,null=True)
    staffname = models.CharField(max_length=20, null=True)

class Billpending(models.Model):
    date=models.DateField(null=True)
    billNo = models.IntegerField(null=True)
    name = models.CharField(max_length=10,null=True)
    satus = models.CharField(max_length=20,null=True)
    amount = models.FloatField(max_length=10,null=True)
    table = models.CharField(max_length=10,null=True)

class pendingBill(models.Model):
    date=models.DateField(null=True)
    billNo = models.IntegerField(null=True)
    phone = models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=10,null=True)
    status = models.CharField(max_length=20,null=True)
    table = models.CharField(max_length=10,null=True)
    amount = models.FloatField(max_length=10,null=True)

class Deletedata(models.Model):
    date = models.DateField(null=True)
    billNo = models.IntegerField(null=True)
    item = models.CharField(max_length=20,null=True)
    item_code = models.CharField(max_length=10,null=True)
    qty = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    taxAmt = models.FloatField(null=True)
    remark = models.CharField(max_length=20,null=True)

class admin_register(models.Model):
    admin_name=models.CharField(max_length=20)
    mobile_number=models.CharField(max_length=10)
    admin_id=models.CharField(max_length=10)
    password=models.CharField(max_length=20)

class user_register(models.Model):
    user_name=models.CharField(max_length=20)
    mobil_number=models.CharField(max_length=10)
    password=models.CharField(max_length=20)

class BookRegister(models.Model):
    name = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=10)

class RoomBooking(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    check_in = models.DateField()
    check_out = models.DateField()
    room_type = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Double', 'Double')])
    category = models.CharField(max_length=20, choices=[('AC', 'AC'), ('Non-AC', 'Non-AC')])

class add_room(models.Model):
    room_no=models.CharField(max_length=10)
    catagory=models.CharField(max_length=10)
    type=models.CharField(max_length=10)
