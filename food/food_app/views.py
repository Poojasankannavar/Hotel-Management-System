from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from food_app.models import  UserReg, AddTable, AddItem, AddCompany, ItemOrder, Orders, Pracel, Printorders, \
    Expenses, Salary, Purchase, Billpending, Deletedata,pendingBill


# Create your views here.

def index(request):
    return render(request, 'index.html')


def admin_nav(request):
    return render(request, 'admin_nav.html')

def homepage(request):
    return render(request,'homepage.html')

def hotelslist(request):
    return render(request,'hotelslist.html')

def food_view(request):
    return render(request,'food_view.html')

def room_view(request):
    return render(request,'room_view.html')

def order_room(request):
    return render(request,'order_room.html')

def nav(request):
    return render(request,'nav.html')




def admin_home(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # List of stored table names
    return render(request, 'admin_home.html',
                  {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})


def userHome(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # Example: list of stored table names

    return render(request, 'userHome.html',
                  {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})



def get_item_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        items = AddItem.objects.filter(Item_name__icontains=query).values('Item_name', 'Item_code', 'Item_price', 'item_cat')
        return JsonResponse(list(items), safe=False)
    return JsonResponse([], safe=False)

def get_item_details(request):
    item_name = request.GET.get('item_name', '')
    if item_name:
        try:
            item = AddItem.objects.get(Item_name=item_name)
            return JsonResponse({
                'Item_code': item.Item_code,
                'Item_price': item.Item_price,
                'item_cat': item.item_cat
            })
        except AddItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):
    if request.method == "POST":
        email = request.POST.get('t1')
        number = request.POST.get('t2')
        username = request.POST.get('t4')
        utype = request.POST.get('utype')
        ucount = UserReg.objects.filter(email=email).count()
        if ucount >= 1:
            return render(request, 'register.html', {'msg': 'This is already exists'})
        else:
            UserReg.objects.create(email=email, number=number, usertype=utype, username=username)
            return render(request, 'register.html', {'msg': 'Thank you for registration'})
    return render(request, 'register.html')


def register_list(request):
    userdata = UserReg.objects.all()
    return render(request, 'register_list.html', {'userdata': userdata})


def delete_register(request, pk):
    udata = get_object_or_404(UserReg, id=pk)

    udata.delete()
    base_url = reverse('register_list')
    return redirect(base_url)



def pending_bills_view_user(request):
    table = AddTable.objects.all()
    query = request.GET.get('q')  # Get the search query

    if query:
        bills = pendingBill.objects.filter(
            billNo__icontains=query
        ) | pendingBill.objects.filter(
            name__icontains=query
        ) | pendingBill.objects.filter(
            table__icontains=query
        ) | pendingBill.objects.filter(
            status__icontains=query
        ) | pendingBill.objects.filter(
            amount__icontains=query
        ) | pendingBill.objects.filter(
            phone__icontains=query
        )| pendingBill.objects.filter(
            date__icontains=query
        )
    else:
        bills = pendingBill.objects.all()

    # Calculate the grand total of the amount field
    grand_total = bills.aggregate(Sum('amount'))['amount__sum'] or 0

    # Add new bill
    if request.method == 'POST':
        con_date = request.POST.get('date')
        bill_no = request.POST.get('billNo')
        name = request.POST.get('name')
        phone = request.POST.get('phone') or None
        table = request.POST.get('table')
        status = request.POST.get('status')
        amount = request.POST.get('amount')

        pendingBill.objects.create(
            billNo=bill_no,
            name=name,
            phone=phone,
            table=table,
            status=status,
            amount=amount,
            date=con_date,
        )
        return redirect('pending_bills_user')

    return render(request, 'pending_bills_user.html', {'bills': bills, 'table': table, 'grand_total': grand_total})



# Edit bill
def edit_bill_user(request, pk):
    bill = get_object_or_404(pendingBill, pk=pk)
    if request.method == 'POST':
        bill.billNo = request.POST.get('billNo')
        bill.name = request.POST.get('name')
        bill.phone = request.POST.get('phone')
        bill.table = request.POST.get('table')
        bill.status = request.POST.get('status')
        bill.amount = request.POST.get('amount')
        bill.save()
        return redirect('pending_bills_user')

    return render(request, 'edit_bill_user.html', {'bill': bill})


# Delete bill
def delete_bill_user(request, pk):
    bill = get_object_or_404(pendingBill, pk=pk)
    bill.delete()
    return redirect('pending_bills_user')

def add_item(request):
    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        # Get the form values
        item_name = request.POST.get('t2')
        item_code = request.POST.get('t1')
        qty = request.POST.get('qty')
        item_price = request.POST.get('t4')
        category = request.POST.get('t5')

        # If qty is not provided, set it to None (null)
        if qty == '':
            qty = None
        else:
            qty = int(qty)  # Convert to integer if a valid number is provided

        # Create the item entry in the database
        item = AddItem.objects.create(
            Item_name=item_name,
            qty=qty,
            Item_price=item_price,
            Item_code=item_code,
            item_cat=category
        )

        # Return a success message
        return render(request, 'add_item.html', {'msg': 'Item added successfully!'})

    return render(request, 'add_item.html')


def view_item(request):
    # Fetch all items from AddItem
    userdata = AddItem.objects.all()
    # Fetch all purchases from Purchase
    userdata1 = Purchase.objects.all()

    grand_total = 0
    userdata_with_totals = []

    for item in userdata:
        # Filter the Purchase table to get the matching qty based on Item_code
        matching_purchase = userdata1.filter(Item_code=item.Item_code).first()  # Get the first match

        # Get the qty from the matching Purchase, or default to 0 if no match is found
        purchase_qty = matching_purchase.qty if matching_purchase else 0

        # Make sure qty is not None, if it is, default to 0 for item_total calculation
        item_qty = item.qty if item.qty is not None else 0

        # Calculate item total (Ensure qty is 0 if None)
        item_total = item_qty * item.Item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': item.id,
            'Item_code': item.Item_code,
            'item_cat': item.item_cat,
            'Item_name': item.Item_name,
            'qty': item.qty,
            'purchase_qty': purchase_qty,  # Qty from Purchase model
            'Item_price': item.Item_price,
            'item_total': item_total  # Add item total
        })

    return render(request, 'view_item.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total
    })


def delete_item_list(request, pk):
    udata = get_object_or_404(AddItem, id=pk)
    udata.delete()
    base_url = reverse('view_item')
    return redirect(base_url)


def delete_purchase(request, pk):
    udata = Purchase.objects.get(id=pk)
    udata.delete()
    base_url = reverse('purchaseList')
    return redirect(base_url)


def edit_item(request, pk):
    rdata = get_object_or_404(AddItem, id=pk)
    if request.method == "POST":
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        qty = request.POST.get('t5')
        item_price = request.POST.get('t4')
        category = request.POST.get('t6')
        AddItem.objects.filter(id=pk).update(
            Item_code=item_code,
            Item_name=item_name,
            qty=qty,
            Item_price=item_price,
            item_cat=category
        )
        base_url = reverse('view_item')
        return redirect(base_url)
    return render(request, 'edit_item.html', {'rdata': rdata})



def updateStock(request, pk):
    # Fetch the existing item details
    rdata = get_object_or_404(AddItem, id=pk)

    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        # Retrieve data from the POST request
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        new_qty = int(request.POST.get('t5'))  # New quantity to be added
        item_price = request.POST.get('t4')
        selling = request.POST.get('selling')

        # Add the new quantity to the existing quantity
        updated_qty = rdata.qty + new_qty

        # Update the AddItem record
        AddItem.objects.filter(id=pk).update(
            Item_code=item_code,
            Item_name=item_name,
            qty=updated_qty,
            Item_price=selling,
        )

        # Record the purchase in the Purchase table
        Purchase.objects.create(
            qty=new_qty,  # Save only the newly added quantity
            Item_name=item_name,
            Item_price=item_price,
            date=con_date,
            Item_code=item_code,
            item_cat=rdata.item_cat,  # Fetch and save item_cat
        )

        # Redirect to the view item page
        base_url = reverse('purchaseUpdate')
        return redirect(base_url)

    return render(request, 'updateStock.html', {'rdata': rdata})




def purchase(request):
    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")
        item_name = request.POST.get('t2')
        item_code = request.POST.get('t1')
        qty = int(request.POST.get('qty'))  # Ensure qty is an integer
        item_price = request.POST.get('t4')
        selling = request.POST.get('selling')
        item_cat = request.POST.get('t5')

        # Attempt to find an existing item by Item_code
        try:
            item = AddItem.objects.get(Item_code=item_code)

            # Add the new qty to the existing qty and dqty
            item.qty += qty

            # Save the updated item
            item.save()

            message = 'Item updated successfully with new quantity!'
        except AddItem.DoesNotExist:
            # If item does not exist, create a new one
            item = AddItem.objects.create(
                Item_code=item_code,
                Item_name=item_name,
                qty=qty,
                Item_price=selling,
                item_cat=item_cat
            )
            message = 'New item added successfully!'

        # Now create a purchase record (a new entry)
        purchase = Purchase.objects.create(
            qty=qty,
            Item_name=item_name,
            Item_price=item_price,
            date=con_date,
            Item_code=item_code,
            item_cat=item_cat
        )

        return render(request, 'purchase.html', {'msg': message})

    return render(request, 'purchase.html')


def purchaseList(request):
    # Fetch all items from AddItem
    userdata = Purchase.objects.all()
    # Fetch all purchases from Purchase
    userdata1 = AddItem.objects.all()

    grand_total = 0
    userdata_with_totals = []

    for item in userdata:
        # Filter the Purchase table to get the matching qty based on Item_code
        matching_item = userdata1.filter(Item_code=item.Item_code).first()  # Get the first match

        # Get the qty from the matching Purchase, or default to 0 if no match is found
        item_qty = matching_item.qty if matching_item else 0

        # Calculate item total
        item_total = item.qty * item.Item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': item.id,
            'date': item.date,
            'Item_code': item.Item_code,
            'Item_name': item.Item_name,
            'item_cat': item.item_cat,
            'qty': item.qty,
            'item_qty': item_qty,  # Qty from Purchase model
            'Item_price': item.Item_price,
            'item_total': item_total  # Add item total
        })

    return render(request, 'purchaseList.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total,
        'userdata1': userdata1
    })


def purchaseEdit(request, pk):
    # Fetch the existing item details
    rdata = get_object_or_404(Purchase, id=pk)

    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        # Retrieve data from the POST request
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        item_price = request.POST.get('t4')
        item_cat = request.POST.get('t6')

        # Add the new quantity to the existing quantity
        # Record the purchase in the Purchase table
        Purchase.objects.filter(id=pk).update(
            Item_name=item_name,
            Item_price=item_price,
            date=con_date,
            Item_code=item_code,
            item_cat=item_cat
        )

        # Redirect to the view item page
        base_url = reverse('purchaseList')
        return redirect(base_url)

    return render(request, 'purchaseEdit.html', {'rdata': rdata})


def add_table(request):
    if request.method == "POST":
        table_name = request.POST.get('t1')
        cat = request.POST.get('t2')
        AddTable.objects.create(Table_name=table_name, Category=cat)
        return render(request, 'add_table.html', {'msg': 'Added'})
    return render(request, 'add_table.html')


def view_table(request):
    udata = AddTable.objects.all()
    return render(request, 'view_table.html', {'udata': udata})


# def delete_table(request, pk):
#     udata = AddTable.objects.get(pk=pk)
#     udata.delete()
#     base_url = reverse('view_table')
#     return redirect(base_url)


def edit_table(request, pk):
    rdata = get_object_or_404(AddTable, id=pk)
    if request.method == "POST":
        table_name = request.POST.get('t1')
        cat = request.POST.get('t2')
        AddTable.objects.filter(id=pk).update(
            Table_name=table_name,
            Category=cat
        )
        base_url = reverse('view_table')
        return redirect(base_url)
    return render(request, 'edit_table.html', {'rdata': rdata})


def add_company(request):
    if request.method == "POST":
        company_name = request.POST.get('t1')
        company_addres = request.POST.get('t2')
        company_gst = request.POST.get('t3')
        company_number = request.POST.get('t4')
        AddCompany.objects.create(Company_name=company_name, Company_address=company_addres, Company_GST=company_gst,
                                  Company_number=company_number)
        return render(request, 'add_company.html', {'msg': 'Added'})
    return render(request, 'add_company.html')


def view_company(request):
    udata = AddCompany.objects.all()
    return render(request, 'view_company.html', {'udata': udata})


def edit_company(request, pk):
    udata = get_object_or_404(AddCompany, id=pk)
    if request.method == "POST":
        company_name = request.POST.get('t1')
        company_address = request.POST.get('t2')
        company_gst = request.POST.get('t3')
        company_number = request.POST.get('t4')
        udata = AddCompany.objects.filter(id=pk).update(
            Company_name=company_name,
            Company_address=company_address,
            Company_GST=company_gst,
            Company_number=company_number
        )
        base_url = reverse('view_company')
        return redirect(base_url)
    return render(request, 'edit_company.html', {'udata': udata})


def delete_company(request, pk):
    udata = get_object_or_404(AddCompany, id=pk)
    udata.delete()
    base_url = reverse('view_company')
    return redirect(base_url)


def add_order(request):
    if request.method == 'GET':
        table_name = request.GET.get('table', '')  # Fetch the table name from the URL parameter

        # Get the last order's bill number (if exists) and generate the next one
        last_order = Orders.objects.order_by('-bill_no').first()
        if last_order:
            bill_no = int(last_order.bill_no) + 1
        else:
            bill_no = 1000

        # Render the add bill form with the table name and generated bill number
        context = {
            'Table_name': table_name,
            'Bill_no': bill_no,
        }
        return render(request, 'add_order.html', context)

    elif request.method == 'POST':
        # Handle form submission (optional: you can process form data as needed)
        return redirect('admin_home')


def add_order_user(request):
    if request.method == 'GET':
        table_name = request.GET.get('table', '')  # Fetch the table name from the URL parameter

        # Get the last order's bill number (if exists) and generate the next one
        last_order = Orders.objects.order_by('-bill_no').first()

        if last_order:
            last_bill_no = last_order.bill_no
            bill_no = str(int(last_bill_no) + 1)
        else:
            BASE_NUMBER = 1001
            bill_no = str(BASE_NUMBER)
        # Render the add bill form with the table name and generated bill number
        context = {
            'Table_name': table_name,
            'Bill_no': bill_no,
        }
        return render(request, 'add_order_user.html', context)

    elif request.method == 'POST':
        # Handle form submission (optional: you can process form data as needed)
        return redirect('userHome')


@require_http_methods(["GET"])
def fetch_item_details(request, item_code):
    try:
        # Use `iexact` for case-insensitive matching
        item = AddItem.objects.get(Item_code__iexact=item_code)
        data = {
            'item_name': item.Item_name,
            'price': item.Item_price,
            'item_cat': item.item_cat,

        }
        return JsonResponse(data)
    except AddItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


from datetime import datetime, timedelta


@require_http_methods(["POST"])
def save_order(request):
    now = datetime.now().replace(microsecond=0)
    current_time = now.strftime("%H:%M:%S")

    # Adjust the bill date logic for the 2 AM to 2 AM cycle
    if now.hour < 2:
        # If the current time is before 2 AM, consider the bill date as the previous day
        bill_date = (now - timedelta(days=1)).date()
    else:
        # Otherwise, use the current date
        bill_date = now.date()

    data = json.loads(request.body)
    bill_details = data['billDetails']
    bill_items = data['billItems']

    table_name = bill_details['table_name']
    bill_no = bill_details['bill_no']

    for item in bill_items:
        item_code = item['item_code']
        item_cat = item['item_cat']
        item_name = item['item_name']
        price = float(item['price'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total = float(item['total'])

        # Create or update the item order, but allow duplicate entries (don't check if it exists)
        ItemOrder.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )

        # Create or update the corresponding record in the Orders table
        Orders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )

        # Add entry to Printorders table
        Printorders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )
        if item_cat != 'food':

            try:
                add_item = AddItem.objects.get(Item_code=item_code)

                # Check if the item has enough stock
                if add_item.qty >= qty:

                    # Decrease qty
                    add_item.qty -= qty

                    # If dqty is None, initialize it to 0
                    if add_item.dqty is None:
                        add_item.dqty = 0

                    # Add the quantity to dqty
                    add_item.dqty += qty

                    # Save the updated item
                    add_item.save()
                else:
                    return JsonResponse({
                        'success': False,
                        'error': f"Insufficient stock for item: {item_name}"
                    }, status=400)

            except AddItem.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f"Item with code {item_code} not found in AddItem table."
                }, status=404)
        else:
            # For food items, skip stock check and show a log message (only for debugging)
            print(f"Skipping stock check for food item: {item_name}")

    return JsonResponse({'success': True, 'redirect_url': reverse('admin_home')})


@require_http_methods(["POST"])
def save_order_user(request):
    now = datetime.now().replace(microsecond=0)
    current_time = now.strftime("%H:%M:%S")

    # Adjust the bill date logic for the 2 AM to 2 AM cycle
    if now.hour < 2:
        # If the current time is before 2 AM, consider the bill date as the previous day
        bill_date = (now - timedelta(days=1)).date()
    else:
        # Otherwise, use the current date
        bill_date = now.date()

    data = json.loads(request.body)
    bill_details = data['billDetails']
    bill_items = data['billItems']

    table_name = bill_details['table_name']
    bill_no = bill_details['bill_no']

    for item in bill_items:
        item_code = item['item_code']
        item_cat = item['item_cat']
        item_name = item['item_name']
        price = float(item['price'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total = float(item['total'])

        # Create or update the item order, but allow duplicate entries (don't check if it exists)
        ItemOrder.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )

        # Create or update the corresponding record in the Orders table
        Orders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )

        # Add entry to Printorders table
        Printorders.objects.create(
            table_name=table_name,
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_cat=item_cat,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total
        )
        if item_cat != 'food':

            try:
                add_item = AddItem.objects.get(Item_code=item_code)

                # Check if the item has enough stock
                if add_item.qty >= qty:

                    # Decrease qty
                    add_item.qty -= qty

                    # If dqty is None, initialize it to 0
                    if add_item.dqty is None:
                        add_item.dqty = 0

                    # Add the quantity to dqty
                    add_item.dqty += qty

                    # Save the updated item
                    add_item.save()
                else:
                    return JsonResponse({
                        'success': False,
                        'error': f"Insufficient stock for item: {item_name}"
                    }, status=400)

            except AddItem.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f"Item with code {item_code} not found in AddItem table."
                }, status=404)
        else:
            # For food items, skip stock check and show a log message (only for debugging)
            print(f"Skipping stock check for food item: {item_name}")


    return JsonResponse({'success': True, 'redirect_url': reverse('userHome')})


@require_http_methods(["GET"])
def fetch_table_data(request):
    table_name = request.GET.get('table')
    if not table_name:
        return JsonResponse({'error': 'Table name is required'})

    items = ItemOrder.objects.filter(table_name=table_name).values(
        'item_code', 'item_cat', 'item_name', 'price', 'gst', 'qty', 'tax_amt', 'total_gst', 'total', 'bill_no',
        'bill_date')

    if items.exists():
        bill = items.first()
        response_data = {
            'bill_no': bill['bill_no'],
            'bill_date': bill['bill_date'],
            'items': list(items)
        }
        print("Fetched data: ", response_data)  # Debug print statement
        return JsonResponse(response_data)
    else:
        print("No items found for table: ", table_name)  # Debug print statement
        return JsonResponse({'error': 'Table data not found'})


def edit_table(request, pk):
    rdata = get_object_or_404(AddTable, id=pk)
    if request.method == "POST":
        table_name = request.POST.get('t1')
        cat = request.POST.get('t2')
        AddTable.objects.filter(id=pk).update(
            Table_name=table_name,
            Category=cat
        )
        base_url = reverse('view_table')
        return redirect(base_url)
    return render(request, 'edit_table.html', {'rdata': rdata})


def exchange_tbl(request):
    table = AddTable.objects.all()
    if request.method == "POST":
        old_table = request.POST.get('oldTable')
        new_table = request.POST.get('newTable')

        # Update only the items associated with the old table
        ItemOrder.objects.filter(table_name=old_table).update(table_name=new_table)

        base_url = reverse('admin_home')
        return redirect(base_url)

    return render(request, 'exchange_tbl.html', {'table': table})


def print_table(request):
    # Get distinct table names from ItemOrder
    tableName = Printorders.objects.values('table_name').distinct()
    return render(request, 'print_table.html', {'tableName': tableName})


# views.py

def print_bill(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

    if selected_table_name:
        # Fetch related ItemOrder objects
        item_orders = Printorders.objects.filter(table_name=selected_table_name)
        table_data = {
            'table_name': selected_table_name,
            'items': []
        }

        for item_order in item_orders:
            item_data = {
                'table_name': item_order.table_name,
                'bill_no': item_order.bill_no,
                'bill_date': item_order.bill_date,
                'bill_time': item_order.bill_time,
                'item_name': item_order.item_name,
                'qty': item_order.qty,
            }
            table_data['items'].append(item_data)

        return render(request, 'print_bill.html', {'table_data': table_data, 'company': company})
    else:
        error_message = "Please select a table name."
        return render(request, 'print_bill.html', {'error_message': error_message})

    return render(request, 'print_bill.html')


def settle_table(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table.html', {'tableName': tableName})


def settle_bill(request, table_name):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and table_name:
        company = AddCompany.objects.all()

        if table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=table_name)
            table_data = {
                'table_name': table_name,
                'items': [],
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.tax_amt

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'settle_bill.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'settle_bill.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'settle_bill.html')


def parcel(request):
    return render(request, 'parcel.html')


@require_http_methods(["POST"])
def save_pracel_user(request):
    now = datetime.now().replace(microsecond=0)
    current_time = now.strftime("%H:%M:%S")

    # Adjust the bill date logic for the 2 AM to 2 AM cycle
    if now.hour < 2:
        # If the current time is before 2 AM, consider the bill date as the previous day
        bill_date = (now - timedelta(days=1)).date()
    else:
        # Otherwise, use the current date
        bill_date = now.date()

    data = json.loads(request.body)
    bill_items = data['billItems']
    parcel_charge = float(data.get('parcelCharge', 0.0))  # Note the key should match what you use in JS

    # Get the current date

    # Determine the next bill_no
    last_pracel = Pracel.objects.all().order_by('-bill_no').first()
    if last_pracel:
        bill_no = int(last_pracel.bill_no) + 1
    else:
        bill_no = 1000

    for item in bill_items:
        item_code = item['item_code']
        item_name = item['item_name']
        price = float(item['price'])
        qty = int(item['qty'])
        tax_amt = float(item['tax_amt'])
        total = float(item['total'])
        Pracel.objects.create(
            bill_no=bill_no,
            bill_date=bill_date,
            bill_time=current_time,
            item_code=item_code,
            item_name=item_name,
            price=price,
            qty=qty,
            tax_amt=tax_amt,
            total=total,
            pracel_charge=parcel_charge  # Ensure this matches your model field
        )
        try:
            add_item = AddItem.objects.get(Item_code=item_code)

            # Check if the item has enough stock
            if add_item.qty >= qty:

                # Decrease qty
                add_item.qty -= qty

                # If dqty is None, initialize it to 0
                if add_item.dqty is None:
                    add_item.dqty = 0

                # Add the quantity to dqty
                add_item.dqty += qty

                # Save the updated item
                add_item.save()
            else:
                return JsonResponse({
                    'success': False,
                    'error': f"Insufficient stock for item: {item_name}"
                }, status=400)

        except AddItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f"Item with code {item_code} not found in AddItem table."
            }, status=404)

    return JsonResponse({'success': True, 'bill_no': bill_no, 'redirect_url': reverse('userHome')})


def print_pracel(request, bill_no):
    # Fetch the pracels for the given bill_no
    pracels = Pracel.objects.filter(bill_no=bill_no)

    # Calculate totals and aggregates
    total_qty = pracels.aggregate(total_qty=Sum('qty'))['total_qty'] or 0
    subtotal = pracels.aggregate(subtotal=Sum('tax_amt'))['subtotal'] or 0

    # Calculate CGST and SGST amounts
    for pracel in pracels:
        price = pracel.price
        qty = pracel.qty
        tax_amt = pracel.tax_amt

    # Get parcel charge from the first item (assuming all items have the same parcel charge)
    parcel_charge = pracels.first().pracel_charge if pracels.exists() else 0

    # Calculate grand total
    grand_total = subtotal + parcel_charge

    # Fetch company details
    company = AddCompany.objects.all()

    context = {
        'pracels': pracels,
        'total_qty': total_qty,
        'subtotal': subtotal,
        'parcel_charge': parcel_charge,
        'grand_total': grand_total,
        'company': company
    }

    return render(request, 'print_pracel.html', context)


from .models import Orders, Billpending # Adjust the import based on your project structure


def sales_report(request):
    category = AddItem.objects.values('item_cat').distinct()
    selected_month = request.POST.get('salesmonth')
    selectedcat = request.POST.get('selectedcat')

    sales_data = []
    total_amount = 0  # Initialize total amount

    if request.method == 'POST' and selected_month:
        # Extract year and month from the selected month

        # Filter orders by year and month

        salesreport = Orders.objects.all()

        if selected_month:
            salesreport = salesreport.filter(bill_date=selected_month)
        if selectedcat and selectedcat.strip() != "":
            salesreport = salesreport.filter(item_cat=selectedcat)

        # Create a dictionary to store the grouped data
        grouped_sales = defaultdict(lambda: {
            'bill_no': None,
            'bill_date': None,
            'items': [],
            'quantities': [],
            'total': 0,
            'status': None
        })

        # Iterate through each sale and group by bill_no
        for sales in salesreport:
            bill_no = sales.bill_no
            grouped_sales[bill_no]['bill_no'] = sales.bill_no
            grouped_sales[bill_no]['bill_date'] = sales.bill_date
            grouped_sales[bill_no]['items'].append(sales.item_name)
            grouped_sales[bill_no]['quantities'].append(str(sales.qty))
            grouped_sales[bill_no]['total'] += sales.total

            # Fetch status from Billpending if it exists (handle multiple Billpending records)
            bill_pending_records = Billpending.objects.filter(billNo=bill_no)
            if bill_pending_records.exists():
                # If there are multiple Billpending records, handle them as needed
                # For example, you can take the first one or aggregate some fields
                bill_pending = bill_pending_records.first()  # Get the first matching record
                grouped_sales[bill_no]['status'] = bill_pending.satus
            else:
                grouped_sales[bill_no]['status'] = "Not Found"

        # Prepare the sales data for rendering
        for key, value in grouped_sales.items():
            # Join items and quantities with commas
            items = ', '.join(value['items'])
            quantities = ', '.join(value['quantities'])
            sales_data.append({
                'bill_no': value['bill_no'],
                'bill_date': value['bill_date'],
                'items': items,
                'quantities': quantities,
                'total': value['total'],
                'status': value['status'],  # Include the status in the sales data
            })
            total_amount += value['total']  # Add to total amount

    return render(
        request,
        'sales_report.html',
        {
            'sales_data': sales_data,
            'selected_month': selected_month,
            'total_amount': total_amount,  # Pass total amount to the template
            'category': category,
            'selectedcat': selectedcat
        }
    )


def item_report(request):
    # Get distinct categories from AddItem
    category = AddItem.objects.values('item_cat').distinct()
    selectedmonth = None
    selectedcat = None
    orders = None  # Initialize orders
    grand_total_amount = 0  # Initialize grand total amount
    grand_total_qty = 0  # Initialize grand total quantity

    if request.method == 'POST':
        selectedmonth = request.POST.get('salesmonth')
        selectedcat = request.POST.get('selectedcat')

        # Query the Orders table based on the selected month and category
        orders = Orders.objects.all()

        if selectedmonth:
            orders = orders.filter(bill_date=selectedmonth)
        if selectedcat and selectedcat.strip() != "":
            orders = orders.filter(item_cat=selectedcat)  # Adjust the field based on your actual schema

        # Aggregate quantities, totals, and item prices for the same item_name
        orders = orders.values('item_name', 'price').annotate(
            total_qty=Sum('qty'),
            total_amount=Sum('total')
        ).order_by('item_name')

        # Calculate the grand total amount and quantity
        grand_total_amount = orders.aggregate(grand_total=Sum('total_amount'))['grand_total'] or 0
        grand_total_qty = orders.aggregate(grand_qty=Sum('total_qty'))['grand_qty'] or 0

    return render(request, 'item_report.html', {
        'category': category,
        'orders': orders if request.method == 'POST' else None,
        'selectedmonth': selectedmonth,
        'selectedcat': selectedcat,
        'grand_total_amount': grand_total_amount,  # Pass grand total amount to the template
        'grand_total_qty': grand_total_qty,  # Pass grand total quantity to the template
    })


def daily_report(request):
    # Default to today's date in case no date is selected
    selected_date = datetime.now().date()

    if request.method == 'POST':
        selected_date_input = request.POST.get('date')
        if selected_date_input:
            # Convert the selected date to a datetime object for querying
            selected_date = datetime.strptime(selected_date_input, '%Y-%m-%d').date()
            orders = Orders.objects.filter(bill_date=selected_date)

            # Calculate the grand total by summing up the total field
            grand_total = orders.aggregate(grand_total=Sum('total'))['grand_total'] or 0
        else:
            orders = Orders.objects.none()  # No data if no date is selected
            grand_total = 0

        return render(request, 'daily_report.html', {
            'selected_date': selected_date,  # Pass the selected date to the frontend
            'orders': orders,
            'grand_total': grand_total
        })

    # If it's a GET request or no date is selected, use today's date as default
    return render(request, 'daily_report.html', {
        'selected_date': selected_date  # Pass selected_date to the template
    })


def print_bill_delete(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = Printorders.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('admin_home'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('admin_home'))


def print_bill_delete_user(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = Printorders.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('userHome'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('userHome'))


def settle_bill_delete(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = ItemOrder.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('admin_home'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('admin_home'))


def settle_bill_delete_user(request, bill_no):
    # Get all the Printorder records with the specified bill_no
    print_orders = ItemOrder.objects.filter(bill_no=bill_no)

    # Check if any records were found
    if print_orders.exists():
        # Delete all the records with the same bill_no
        print_orders.delete()
        # Optionally, provide feedback or redirect to the print bill page
        return redirect(reverse('userHome'))
    else:
        # Handle case where no records are found (optional)
        return redirect(reverse('userHome'))


def exchange_tbl_user(request):
    table = AddTable.objects.all()
    if request.method == "POST":
        old_table = request.POST.get('oldTable')
        new_table = request.POST.get('newTable')

        # Update only the items associated with the old table
        ItemOrder.objects.filter(table_name=old_table).update(table_name=new_table)

        base_url = reverse('userHome')
        return redirect(base_url)

    return render(request, 'exchange_tbl_user.html', {'table': table})


def print_table_user(request):
    # Get distinct table names from ItemOrder
    tableName = Printorders.objects.values('table_name').distinct()
    return render(request, 'print_table_user.html', {'tableName': tableName})


# views.py

def print_bill_user(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

    if selected_table_name:
        # Fetch related ItemOrder objects
        item_orders = Printorders.objects.filter(table_name=selected_table_name)
        table_data = {
            'table_name': selected_table_name,
            'items': []
        }

        for item_order in item_orders:
            item_data = {
                'table_name': item_order.table_name,
                'bill_no': item_order.bill_no,
                'bill_date': item_order.bill_date,
                'bill_time': item_order.bill_time,
                'item_name': item_order.item_name,
                'qty': item_order.qty,
            }
            table_data['items'].append(item_data)

        return render(request, 'print_bill_user.html', {'table_data': table_data, 'company': company})
    else:
        error_message = "Please select a table name."
        return render(request, 'print_bill_user.html', {'error_message': error_message})
 


def settle_table_user(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table_user.html', {'tableName': tableName})


def settle_bill_user(request, table_name):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and table_name:
        company = AddCompany.objects.all()

        if table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=table_name)
            table_data = {
                'table_name': table_name,
                'items': [],
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                item_data = {
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.tax_amt

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'settle_bill_user.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'settle_bill_user.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'settle_bill_user.html')


def checkTables(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'checkTables.html', {'tableName': tableName})


def checkItems(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        # Fetch all company information
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects for the selected table_name
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],  # To store individual item details
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            # Loop through each item order for the selected table
            for item_order in item_orders:
                item_data = {
                    'id': item_order.id,
                    'item_code': item_order.item_code,
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'qty': item_order.qty,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,  # Fetch tax_amt from ItemOrder
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Calculate taxsubtotal
                    'total': item_order.total  # Assuming 'total' includes all charges
                }
                table_data['items'].append(item_data)

                # Update the aggregate values for the table
                table_data['subtotal'] += item_order.total  # Update the subtotal for all items
                table_data['total_qty'] += item_order.qty  # Update the total quantity
                table_data['taxsubtotal'] += item_order.tax_amt * item_order.qty  # Update taxsubtotal
                table_data['total'] += item_order.tax_amt  # Update total amount (including all taxes)

            # Render the data to the template
            return render(request, 'checkItems.html', {'table_data': table_data, 'company': company})

        else:
            # If no table_name is selected, show an error message
            error_message = "Please select a table name."
            return render(request, 'checkItems.html', {'error_message': error_message})

    # Handle other cases or default GET request
    return render(request, 'checkItems.html')


def checkTablesUser(request):
    # Get distinct table names from ItemOrder
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'checkTablesUser.html', {'tableName': tableName})


def checkItemsUser(request):
    selected_table_name = request.GET.get('table_name')

    if request.method == 'GET' and selected_table_name:
        company = AddCompany.objects.all()

        if selected_table_name:
            # Fetch related ItemOrder objects
            item_orders = ItemOrder.objects.filter(table_name=selected_table_name)
            table_data = {
                'table_name': selected_table_name,
                'items': [],
                'taxsubtotal': 0,  # Initialize taxsubtotal
                'subtotal': 0,  # Initialize subtotal
                'total_qty': 0,  # Initialize total quantity
                'total': 0,  # Initialize total
            }

            for item_order in item_orders:
                item_data = {
                    'id': item_order.id,
                    'table_name': item_order.table_name,
                    'bill_no': item_order.bill_no,
                    'bill_date': item_order.bill_date,
                    'bill_time': item_order.bill_time,
                    'item_name': item_order.item_name,
                    'item_code': item_order.item_code,
                    'qty': item_order.qty,
                    'price': item_order.price,
                    'tax_amt': item_order.tax_amt,
                    'total_gst': item_order.total_gst,
                    'taxsubtotal': item_order.tax_amt * item_order.qty,  # Update taxsubtotal per item
                    'total': item_order.total
                }
                table_data['items'].append(item_data)

                table_data['subtotal'] += item_order.total  # Assuming total is the item total
                table_data['total_qty'] += item_order.qty
                table_data['taxsubtotal'] += item_order.tax_amt
                table_data['total'] += item_order.tax_amt  # Update total amount (including all taxes)

            # Delete ItemOrder objects for the selected table_name after displaying details

            return render(request, 'checkItemsUser.html', {'table_data': table_data, 'company': company})
        else:
            error_message = "Please select a table name."
            return render(request, 'checkItemsUser.html', {'error_message': error_message})

    # Handle GET request or any other cases here if needed
    return render(request, 'checkItemsUser.html')


def index1(request):
    tdata = AddTable.objects.all()
    saved_table_name = request.GET.get('table', None)  # Extract from URL parameter
    stored_tables = [item.table_name for item in ItemOrder.objects.all()]  # List of stored table names
    return render(request, 'index1.html',
                  {'tdata': tdata, 'saved_table_name': saved_table_name, 'stored_tables': stored_tables})


def addExpenses(request):
    return render(request, 'expenses.html')


def saveExpenses(request):
    if request.method == 'POST':
        # Parse and validate date
        date_str = request.POST.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")  # Debugging statement
            return redirect('adminExpenses')
        amount = request.POST.get('amt')
        reason = request.POST.get('reason')

        Expenses.objects.create(
            Date=date,
            Reason=reason,
            Amount=amount,
        )

    else:
        print("No username found in session.")  # Debugging statement

        return redirect('addExpenses')  # Replace with your desired success URL

    return render(request, 'expenses.html')


def viewExpenses(request):
    expenses = []
    grand_total = 0  # Initialize the grand total to 0

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        # Initialize the filter query
        filters = {}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter

            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        # Query the Expenses model with the combined filters
        expenses = Expenses.objects.filter(**filters)

        # Calculate the grand total of Amount
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0  # Aggregate sum of Amount

    return render(request, 'viewExpenses.html', {'expenses': expenses, 'grand_total': grand_total})


def get_staff_name(request):
    query = request.GET.get('query', '')
    if query:
        username = UserReg.objects.filter(username__icontains=query).values_list('username', flat=True)
        print('username numbers:', list(username))  # Debugging: check the data in the terminal
        return JsonResponse(list(username), safe=False)
    return JsonResponse([], safe=False)


def salary(request):
    return render(request, 'salary.html')


def saveSalary(request):
    if request.method == 'POST':
        # Parse and validate date
        date_str = request.POST.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")  # Debugging statement
            return redirect('adminExpenses')
        amount = request.POST.get('amt')
        reason = request.POST.get('reason')
        salaryDetails = request.POST.get('salaryDetails')

        Salary.objects.create(
            Date=date,
            desc=reason,
            Amount=amount,
            staffname=salaryDetails,
        )

    else:
        print("No username found in session.")  # Debugging statement

        return redirect('salary')  # Replace with your desired success URL

    return render(request, 'salary.html')


def viewSalary(request):
    # Fetch all salary records initially
    expenses = Salary.objects.all()
    grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0  # Grand total for unfiltered data

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        staffname = request.POST.get('staffname')

        # Initialize the filter query
        filters = {}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter
            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        if staffname:
            filters['staffname__icontains'] = staffname

        # Apply the filters to the Salary queryset
        expenses = Salary.objects.filter(**filters)

        # Recalculate the grand total for the filtered data
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0

    return render(request, 'viewSalary.html', {'expenses': expenses, 'grand_total': grand_total})




def profit_report(request):
    # Get the from_date and to_date from the request (if provided)
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    from_date = parse_date(from_date_str) if from_date_str else None
    to_date = parse_date(to_date_str) if to_date_str else None

    # Query all consignments, expenses, salaries, and pending bills
    consignments = Orders.objects.all()
    expenses = Expenses.objects.all()
    salaries = Salary.objects.all()
    pending_bills = pendingBill.objects.all()

    # Filter by date range if provided
    if from_date and to_date:
        consignments = consignments.filter(bill_date__range=[from_date, to_date])
        expenses = expenses.filter(Date__range=[from_date, to_date])
        salaries = salaries.filter(Date__range=[from_date, to_date])
        pending_bills = pending_bills.filter(date__range=[from_date, to_date])

    # Track already processed track_ids
    processed_track_ids = set()
    unique_consignments = []

    # Ensure only unique consignments based on bill_no
    for consignment in consignments:
        track_id = consignment.bill_no
        if track_id not in processed_track_ids:
            processed_track_ids.add(track_id)
            unique_consignments.append(consignment)

    # Group consignments by date and calculate total cost
    consignments_grouped = (
        Orders.objects.filter(id__in=[c.id for c in unique_consignments])
        .values('bill_date')
        .annotate(total=Sum('total'))
        .order_by('bill_date')
    )

    # Group expenses, salaries, and pending bills
    expenses_grouped = expenses.values('Date', 'Reason').annotate(
        total_amount=Sum('Amount')
    ).order_by('Date', 'Reason')

    salaries_grouped = salaries.values('Date', 'staffname').annotate(
        total_salary=Sum('Amount')
    ).order_by('Date', 'staffname')

    pending_bills_grouped = pending_bills.values('date', 'name').annotate(
        total_pending=Sum('amount')
    ).order_by('date', 'name')

    # Calculate grand totals
    grand_total_consignment = sum(item['total'] for item in consignments_grouped)
    grand_total_expenses = sum(item['total_amount'] for item in expenses_grouped)
    grand_total_salaries = sum(item['total_salary'] for item in salaries_grouped)
    grand_total_pending = sum(item['total_pending'] for item in pending_bills_grouped)

    # Calculate combined grand totals
    combined_grand_total = (
        grand_total_consignment + grand_total_pending
        + grand_total_expenses + grand_total_salaries
    )

    # Calculate profit or loss
    total_balance = (
            grand_total_consignment - (grand_total_pending
            + grand_total_expenses + grand_total_salaries)
    )

    profit = total_balance if total_balance > 0 else 0
    loss = abs(total_balance) if total_balance < 0 else 0

    # Pass the grouped data and totals to the template
    return render(request, 'profit_report.html', {
        'consignments': consignments_grouped,
        'expenses': expenses_grouped,
        'salaries': salaries_grouped,
        'pending_bills': pending_bills_grouped,
        'grand_total_consignment': grand_total_consignment,
        'grand_total_expenses': grand_total_expenses,
        'grand_total_salaries': grand_total_salaries,
        'grand_total_pending': grand_total_pending,
        'combined_grand_total': combined_grand_total,
        'profit': profit,
        'loss': loss,
        'from_date': from_date_str,
        'to_date': to_date_str,
    })




def billPending(request):
    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")
        # Handle form submission
        bill_no = request.POST.get('bill_no')
        name = request.POST.get('name')
        status = request.POST.get('status')
        amount = request.POST.get('amount')
        table_name = request.POST.get('tablename')

        # Save data in Billpending table
        Billpending.objects.create(
            billNo=bill_no,
            name=name,
            satus=status,
            amount=amount,
            table=table_name,
            date=con_date
        )
        return redirect('settle_bill', table_name=table_name)  # Replace with the correct name of your view

    # Fetch table names
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table.html', {'tableName': tableName})


def billPendingUser(request):
    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")
        # Handle form submission
        bill_no = request.POST.get('bill_no')
        name = request.POST.get('name')
        status = request.POST.get('status')
        amount = request.POST.get('amount')
        table_name = request.POST.get('tablename')

        # Save data in Billpending table
        Billpending.objects.create(
            billNo=bill_no,
            name=name,
            satus=status,
            amount=amount,
            date=con_date
        )
        return redirect('settle_bill_user', table_name=table_name)  # Replace with the correct name of your view

    # Fetch table names
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'settle_table.html', {'tableName': tableName})


from django.db.models import Sum

def get_table_details(request):
    table_name = request.GET.get('table_name')

    if not table_name:
        return JsonResponse({'error': 'Table name not provided'}, status=400)

    # Filter by table_name and calculate the total amount
    item_orders = ItemOrder.objects.filter(table_name=table_name)
    total_tax_amt = item_orders.aggregate(Sum('tax_amt'))['tax_amt__sum'] or 0  # Sum up the 'tax_amt' column

    if item_orders.exists():
        # Get the first item's details (e.g., bill_no) if needed
        first_item = item_orders.first()
        data = {
            'amount': total_tax_amt,  # Total amount for the table
            'bill_no': first_item.bill_no,
            'table_name': table_name
        }
    else:
        # If no entries are found, return N/A
        data = {
            'amount': 0,
            'bill_no': 'N/A',
            'table_name': table_name
        }

    return JsonResponse(data)

def delete_item(request, item_id):
    if request.method == 'POST':
        # Fetch the item from ItemOrder using the item_id
        item = get_object_or_404(ItemOrder, id=item_id)
        itemorder = get_object_or_404(Orders, id=item_id)

        # Get the remark from POST data
        remark = request.POST.get('remark', '')

        # Save the deleted item details and remark in Deletedata
        Deletedata.objects.create(
            date=item.bill_date,
            billNo=item.bill_no,
            item=item.item_name,
            item_code=item.item_code,
            qty=item.qty,
            price=item.price,
            taxAmt=item.tax_amt,
            remark=remark
        )
        # Update the quantity in AddItem table, excluding 'food' category
        try:
            add_item = AddItem.objects.get(Item_code=item.item_code)

            # Exclude items where item_cat is 'food'
            if add_item.item_cat != 'food':
                add_item.qty += item.qty
                add_item.dqty -= item.qty
                add_item.save()

        except AddItem.DoesNotExist:
            print(f"Item with code {item.item_code} not found in AddItem table.")

        # Delete the item from ItemOrder and Orders
        item.delete()
        itemorder.delete()

        # Return a generic success response
        return JsonResponse({'success': True})

    return HttpResponse("Method not allowed", status=405)


def delete_item_user(request, item_id):
    if request.method == 'POST':
        # Fetch the item from ItemOrder using the item_id
        item = get_object_or_404(ItemOrder, id=item_id)
        itemorder = get_object_or_404(Orders, id=item_id)

        # Get the remark from POST data
        remark = request.POST.get('remark', '')

        # Save the deleted item details and remark in Deletedata
        Deletedata.objects.create(
            date=item.bill_date,
            billNo=item.bill_no,
            item=item.item_name,
            item_code=item.item_code,
            qty=item.qty,
            price=item.price,
            taxAmt=item.tax_amt,
            remark=remark
        )
        # Update the quantity in AddItem table, excluding 'food' category
        try:
            add_item = AddItem.objects.get(Item_code=item.item_code)

            # Exclude items where item_cat is 'food'
            if add_item.item_cat != 'food':
                add_item.qty += item.qty
                add_item.dqty -= item.qty
                add_item.save()

        except AddItem.DoesNotExist:
            print(f"Item with code {item.item_code} not found in AddItem table.")

        # Delete the item from ItemOrder and Orders
        item.delete()
        itemorder.delete()

        # Return a generic success response
        return JsonResponse({'success': True})

    return HttpResponse("Method not allowed", status=405)


def editStaff(request, pk):
    rdata = get_object_or_404(UserReg, id=pk)
    original_email = rdata.email

    if request.method == "POST":
        email = request.POST.get('t1')
        number = request.POST.get('t2')
        password = request.POST.get('t3')
        username = request.POST.get('t4')
        utype = request.POST.get('utype')
        UserReg.objects.filter(id=pk).update(
            username=username,
            email=email,
            number=number,
            password=password,
            usertype=utype
        )
        # Update the Login record using the original staffPhone
        user = UserLogin.objects.filter(
            username=original_email).first()  # Fetch the user with the original phone number
        if user:
            user.username = email  # Update username to the new phone number
            user.password = password
            user.save()
        base_url = reverse('register_list')
        return redirect(base_url)
    return render(request, 'editStaff.html', {'rdata': rdata})


def viewSalaryHistory(request, pk):
    # Fetch all expenses for the given staff (before applying filters)
    expenses = Salary.objects.filter(staffname=pk)
    grand_total = expenses.aggregate(total_amount=Sum('Amount'))[
                      'total_amount'] or 0  # Calculate grand total for all records initially

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')
        staffname = request.POST.get('staffname')

        # Initialize the filter query
        filters = {'staffname': pk}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter
            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        if staffname:
            filters['staffname__icontains'] = staffname

        # Query the Salary model with the combined filters
        expenses = Salary.objects.filter(**filters)

        # Recalculate the grand total of filtered Amount
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0

    return render(request, 'viewSalaryHistory.html', {
        'expenses': expenses,
        'grand_total': grand_total,
        'staffname': pk,
    })


def pendingReport(request):
    data = Billpending.objects.filter(satus='Pending')
    grand_total = 0

    if request.method == 'POST':
        # Get filter inputs from the request
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        name = request.POST.get('name')

        # Apply filters
        filters = Q(satus='Pending')  # Initial filter for pending status

        if from_date:
            # Convert string to datetime for filtering
            filters &= Q(date__gte=datetime.strptime(from_date, '%Y-%m-%d'))
        if to_date:
            # Convert string to datetime for filtering
            filters &= Q(date__lte=datetime.strptime(to_date, '%Y-%m-%d'))
        if name:
            filters &= Q(name__icontains=name)

        # Apply the filters to the query
        data = Billpending.objects.filter(filters)

    # Calculate grand total of the amount field
    grand_total = data.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(
        request,
        'pendingReport.html',
        {
            'data': data,
            'grand_total': grand_total,
            'from_date': from_date if request.method == 'POST' else '',
            'to_date': to_date if request.method == 'POST' else '',
            'name': name if request.method == 'POST' else ''
        }
    )


def get_name(request):
    query = request.GET.get('query', '')
    if query:
        username = Billpending.objects.filter(name__icontains=query).values_list('name', flat=True)
        print('username numbers:', list(username))  # Debugging: check the data in the terminal
        return JsonResponse(list(username), safe=False)
    return JsonResponse([], safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_bill_status(request, bill_id):
    if request.method == 'POST':
        try:
            bill = get_object_or_404(Billpending, id=bill_id)
            data = json.loads(request.body)
            entered_amount = float(data.get('entered_amount', 0))

            if entered_amount <= 0 or entered_amount > bill.amount:
                return JsonResponse({'success': False, 'error': 'Invalid amount entered'}, status=400)

            bill.amount -= entered_amount
            if bill.amount == 0:
                bill.satus = 'Paid'
            bill.save()

            return JsonResponse({'success': True, 'new_amount': bill.amount, 'status': bill.satus})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


from collections import defaultdict


def purchaseReport(request):
    # Initialize filters
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    selected_cat = request.POST.get('selectedcat')

    # Apply filters to the Purchase and AddItem queryset
    userdata = Purchase.objects.all()
    userdata1 = AddItem.objects.all()

    if from_date and to_date:
        userdata = userdata.filter(date__range=[from_date, to_date])

    if selected_cat:
        userdata = userdata.filter(Item_name=selected_cat)
        userdata1 = userdata1.filter(Item_name=selected_cat)

    grand_total = 0
    grand_item_total = 0
    grand_tax_amount = 0
    final_grand_tax_amount = 0
    userdata_with_totals = defaultdict(lambda: {
        'Item_code': None,
        'Item_name': None,
        'qty': 0,
        'item_qty': 0,
        'purchase_item_price': 0,
        'additem_item_price': 0,
        'item_total': 0,
        'tax_amount': 0
    })

    for item in userdata:
        # Fetch the Item_price from the Purchase table
        purchase_item_price = item.Item_price if item.Item_price is not None else 0

        # Filter the AddItem table to get the matching item based on Item_code
        matching_item = userdata1.filter(Item_code=item.Item_code).first()

        # Fetch the Item_price from the AddItem table, or default to 0 if no match is found
        additem_item_price = matching_item.Item_price if matching_item and matching_item.Item_price is not None else 0

        # Get the qty (dqty) from the AddItem table, or default to 0 if no match is found
        item_qty = matching_item.dqty if matching_item and matching_item.dqty is not None else 0

        # Calculate item total using qty from the Purchase table and its Item_price
        item_total = item.qty * purchase_item_price
        grand_total += item_total

        # Calculate tax amount using item_qty (from AddItem) and AddItem.Item_price
        tax_amount = item_qty * additem_item_price
        grand_tax_amount += tax_amount

        # Add to the grouped data
        group = userdata_with_totals[item.Item_code]
        group['Item_code'] = item.Item_code
        group['Item_name'] = item.Item_name
        group['qty'] += item.qty
        group['item_qty'] = item_qty
        group['purchase_item_price'] = purchase_item_price
        group['additem_item_price'] = additem_item_price
        group['item_total'] += item_total
        group['tax_amount'] += tax_amount

    # Calculate the final grand tax amount
    for group in userdata_with_totals.values():
        final_grand_tax_amount += group['tax_amount']

    # Convert grouped data to a list for rendering
    grouped_data = list(userdata_with_totals.values())

    return render(request, 'purchaseReport.html', {
        'userdata': grouped_data,
        'grand_total': grand_total,
        'grand_item_total': grand_item_total,
        'grand_tax_amount': grand_tax_amount,
        'final_grand_tax_amount': final_grand_tax_amount,
        'userdata1': userdata1
    })


def parcelReport(request):
    selected_month = request.POST.get('salesmonth')
    sales_data = []
    total_amount = 0  # Initialize total amount
    grand_total = 0  # Initialize grand total

    if request.method == 'POST' and selected_month:
        # Extract year and month from the selected month
        year, month = selected_month.split('-')

        # Filter orders by year and month
        salesreport = Pracel.objects.filter(
            Q(bill_date__year=year) & Q(bill_date__month=month)
        )

        # Create a dictionary to store the grouped data
        grouped_sales = defaultdict(lambda: {
            'bill_no': None,
            'bill_date': None,
            'pracel_charge': None,
            'items': [],
            'quantities': [],
            'total': 0,
            'status': None
        })

        # Iterate through each sale and group by bill_no
        for sales in salesreport:
            bill_no = sales.bill_no
            grouped_sales[bill_no]['bill_no'] = sales.bill_no
            grouped_sales[bill_no]['bill_date'] = sales.bill_date
            grouped_sales[bill_no]['pracel_charge'] = sales.pracel_charge  # Corrected line
            grouped_sales[bill_no]['items'].append(sales.item_name)
            grouped_sales[bill_no]['quantities'].append(str(sales.qty))
            grouped_sales[bill_no]['total'] += sales.total

            # Fetch status from Billpending if it exists
            try:
                bill_pending = Billpending.objects.get(billNo=bill_no)
                grouped_sales[bill_no]['status'] = bill_pending.satus
            except Billpending.DoesNotExist:
                grouped_sales[bill_no]['status'] = "Not Found"

        # Prepare the sales data for rendering
        for key, value in grouped_sales.items():
            # Add parcel_charge to total for grand total calculation
            total_with_charge = value['total'] + (value['pracel_charge'] or 0)
            sales_data.append({
                'bill_no': value['bill_no'],
                'pracel_charge': value['pracel_charge'],
                'bill_date': value['bill_date'],
                'items': ', '.join(value['items']),
                'quantities': ', '.join(value['quantities']),
                'total': value['total'],
                'total_with_charge': total_with_charge,  # Add this line for total with parcel_charge
                'status': value['status'],  # Include the status in the sales data
            })
            total_amount += value['total']  # Add to total amount
            grand_total += total_with_charge  # Add total with parcel_charge to grand total

    return render(
        request,
        'parcelList.html',
        {
            'sales_data': sales_data,
            'selected_month': selected_month,
            'total_amount': total_amount,  # Pass total amount to the template
            'grand_total': grand_total  # Pass grand total to the template
        }
    )


def userExpenses(request):
    return render(request, 'userExpenses.html')


def usersaveExpenses(request):
    if request.method == 'POST':
        # Parse and validate date
        date_str = request.POST.get('date')
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format.")  # Debugging statement
            return redirect('adminExpenses')
        amount = request.POST.get('amt')
        reason = request.POST.get('reason')

        Expenses.objects.create(
            Date=date,
            Reason=reason,
            Amount=amount,
        )

    else:
        print("No username found in session.")  # Debugging statement

        return redirect('userExpenses')  # Replace with your desired success URL

    return render(request, 'userExpenses.html')


def userViewExpenses(request):
    expenses = []
    grand_total = 0  # Initialize the grand total to 0

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        # Initialize the filter query
        filters = {}

        if from_date_str and to_date_str:
            try:
                # Parse the date strings into datetime objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                filters['Date__range'] = (from_date, to_date)  # Date filter

            except ValueError:
                print("Invalid date format.")  # Handle invalid date formats

        # Query the Expenses model with the combined filters
        expenses = Expenses.objects.filter(**filters)

        # Calculate the grand total of Amount
        grand_total = expenses.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0  # Aggregate sum of Amount

    return render(request, 'userViewExpenses.html', {'expenses': expenses, 'grand_total': grand_total})


def deleteReport(request):
    from collections import defaultdict

    sales_data = []
    total_amount = 0  # Initialize total amount

    if request.method == 'POST':
        # Get the from_date and to_date from the form
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # Validate that at least one date is provided
        if from_date or to_date:
            # Filter orders by the provided date range
            filters = Q()
            if from_date:
                filters &= Q(date__gte=from_date)
            if to_date:
                filters &= Q(date__lte=to_date)

            salesreport = Deletedata.objects.filter(filters)

            # Create a dictionary to store the grouped data
            grouped_sales = defaultdict(lambda: {
                'items': defaultdict(lambda: {'qty': 0, 'price': 0}),  # Store quantities and prices
                'total': 0,
                'status': None
            })

            # Iterate through each sale and group by item name
            for sales in salesreport:
                item_name = sales.item
                grouped_sales[item_name]['items'][item_name]['qty'] += sales.qty  # Aggregate quantity
                grouped_sales[item_name]['items'][item_name]['price'] = sales.price  # Fetch and store price
                grouped_sales[item_name]['total'] += sales.taxAmt

            # Prepare the sales data for rendering
            for item_name, value in grouped_sales.items():
                # Format quantities and prices
                quantities = value['items'][item_name]['qty']
                price = value['items'][item_name]['price']
                sales_data.append({
                    'item_name': item_name,
                    'quantities': quantities,
                    'price': price,
                    'total': value['total'],
                    'status': value['status'],  # Include the status in the sales data
                })
                total_amount += value['total']  # Add to total amount

    return render(
        request,
        'deleteReport.html',
        {
            'sales_data': sales_data,
            'total_amount': total_amount,  # Pass total amount to the template
        }
    )


def usersalesReport(request):
    category = AddItem.objects.values('item_cat').distinct()
    selected_month = request.POST.get('salesmonth')
    selectedcat = request.POST.get('selectedcat')

    sales_data = []
    total_amount = 0  # Initialize total amount

    if request.method == 'POST' and selected_month:
        # Extract year and month from the selected month

        # Filter orders by year and month

        salesreport = Orders.objects.all()

        if selected_month:
            salesreport = salesreport.filter(bill_date=selected_month)
        if selectedcat and selectedcat.strip() != "":
            salesreport = salesreport.filter(item_cat=selectedcat)

        # Create a dictionary to store the grouped data
        grouped_sales = defaultdict(lambda: {
            'bill_no': None,
            'bill_date': None,
            'items': [],
            'quantities': [],
            'total': 0,
            'status': None
        })

        # Iterate through each sale and group by bill_no
        for sales in salesreport:
            bill_no = sales.bill_no
            grouped_sales[bill_no]['bill_no'] = sales.bill_no
            grouped_sales[bill_no]['bill_date'] = sales.bill_date
            grouped_sales[bill_no]['items'].append(sales.item_name)
            grouped_sales[bill_no]['quantities'].append(str(sales.qty))
            grouped_sales[bill_no]['total'] += sales.total

            # Fetch status from Billpending if it exists (handle multiple Billpending records)
            bill_pending_records = Billpending.objects.filter(billNo=bill_no)
            if bill_pending_records.exists():
                # If there are multiple Billpending records, handle them as needed
                # For example, you can take the first one or aggregate some fields
                bill_pending = bill_pending_records.first()  # Get the first matching record
                grouped_sales[bill_no]['status'] = bill_pending.satus
            else:
                grouped_sales[bill_no]['status'] = "Not Found"

        # Prepare the sales data for rendering
        for key, value in grouped_sales.items():
            # Join items and quantities with commas
            items = ', '.join(value['items'])
            quantities = ', '.join(value['quantities'])
            sales_data.append({
                'bill_no': value['bill_no'],
                'bill_date': value['bill_date'],
                'items': items,
                'quantities': quantities,
                'total': value['total'],
                'status': value['status'],  # Include the status in the sales data
            })
            total_amount += value['total']  # Add to total amount

    return render(
        request,
        'usersalesReport.html',
        {
            'sales_data': sales_data,
            'selected_month': selected_month,
            'total_amount': total_amount,  # Pass total amount to the template
            'category': category,
            'selectedcat': selectedcat
        }
    )


def purchaseUpdate(request):
    # Fetch all items from AddItem, excluding item_cat='food'
    userdata = AddItem.objects.exclude(item_cat='food')

    # Fetch all purchases from Purchase
    userdata1 = Purchase.objects.all()

    grand_total = 0
    userdata_with_totals = []

    for item in userdata:
        # Filter the Purchase table to get the matching purchase based on Item_code
        matching_purchase = userdata1.filter(Item_code=item.Item_code).first()  # Get the first match

        # If no matching purchase is found, skip the item
        if not matching_purchase:
            continue

        # Get the purchase quantity from the matching Purchase, or default to 0 if no match is found
        purchase_qty = matching_purchase.qty if matching_purchase else 0

        # Fetch the Item_price from the Purchase table (assuming Purchase has this field)
        item_price = matching_purchase.Item_price if matching_purchase else 0

        # Calculate item total using the Item_price from the Purchase table
        item_total = purchase_qty * item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': item.id,
            'Item_code': item.Item_code,
            'item_cat': item.item_cat,
            'Item_name': item.Item_name,
            'qty': item.qty,
            'purchase_qty': purchase_qty,  # Qty from Purchase model
            'Item_price': item_price,  # Item_price from Purchase model
            'item_total': item_total  # Add item total
        })

    return render(request, 'purchaseUpdate.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total  # Grand total based on Purchase data
    })


from django.db.models import Sum


def tableReport(request):
    # Get distinct categories from AddItem
    tables = AddTable.objects.all()
    selectedmonth = None
    selectedcat = None
    orders = None  # Initialize orders
    grand_total_amount = 0  # Initialize grand total amount
    grand_total_qty = 0  # Initialize grand total quantity

    if request.method == 'POST':
        selectedmonth = request.POST.get('salesmonth')
        selectedcat = request.POST.get('selectedcat')

        # Query the Orders table based on the selected month and category
        orders = Orders.objects.all()

        if selectedmonth:
            orders = orders.filter(bill_date=selectedmonth)
        if selectedcat and selectedcat.strip() != "":
            orders = orders.filter(table_name=selectedcat)  # Adjust the field based on your actual schema

        # Group by bill_no and aggregate total_qty and total_amount for each bill_no
        orders = orders.values('bill_no').annotate(
            total_qty=Sum('qty'),
            total_amount=Sum('total')
        ).order_by('bill_no')

        # Calculate the grand total amount and quantity
        grand_total_amount = orders.aggregate(grand_total=Sum('total_amount'))['grand_total'] or 0
        grand_total_qty = orders.aggregate(grand_qty=Sum('total_qty'))['grand_qty'] or 0

    return render(request, 'tableReport.html', {
        'tables': tables,
        'orders': orders if request.method == 'POST' else None,
        'selectedmonth': selectedmonth,
        'selectedcat': selectedcat,
        'grand_total_amount': grand_total_amount,  # Pass grand total amount to the template
        'grand_total_qty': grand_total_qty,  # Pass grand total quantity to the template
    })


def itemReportUser(request):
    # Get distinct categories from AddItem
    category = AddItem.objects.values('item_cat').distinct()
    selectedmonth = None
    selectedcat = None
    orders = None  # Initialize orders
    grand_total_amount = 0  # Initialize grand total amount
    grand_total_qty = 0  # Initialize grand total quantity

    if request.method == 'POST':
        selectedmonth = request.POST.get('salesmonth')
        selectedcat = request.POST.get('selectedcat')

        # Query the Orders table based on the selected month and category
        orders = Orders.objects.all()

        if selectedmonth:
            orders = orders.filter(bill_date=selectedmonth)
        if selectedcat and selectedcat.strip() != "":
            orders = orders.filter(item_cat=selectedcat)  # Adjust the field based on your actual schema

        # Aggregate quantities, totals, and item prices for the same item_name
        orders = orders.values('item_name', 'price').annotate(
            total_qty=Sum('qty'),
            total_amount=Sum('total')
        ).order_by('item_name')

        # Calculate the grand total amount and quantity
        grand_total_amount = orders.aggregate(grand_total=Sum('total_amount'))['grand_total'] or 0
        grand_total_qty = orders.aggregate(grand_qty=Sum('total_qty'))['grand_qty'] or 0

    return render(request, 'itemReportUser.html', {
        'category': category,
        'orders': orders if request.method == 'POST' else None,
        'selectedmonth': selectedmonth,
        'selectedcat': selectedcat,
        'grand_total_amount': grand_total_amount,  # Pass grand total amount to the template
        'grand_total_qty': grand_total_qty,  # Pass grand total quantity to the template
    })


def purchaseUser(request):
    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")
        item_name = request.POST.get('t2')
        item_code = request.POST.get('t1')
        qty = int(request.POST.get('qty'))  # Ensure qty is an integer
        item_price = request.POST.get('t4')
        selling = request.POST.get('selling')
        item_cat = request.POST.get('t5')

        # Attempt to find an existing item by Item_code
        try:
            item = AddItem.objects.get(Item_code=item_code)

            # Add the new qty to the existing qty and dqty
            item.qty += qty

            # Save the updated item
            item.save()

            message = 'Item updated successfully with new quantity!'
        except AddItem.DoesNotExist:
            # If item does not exist, create a new one
            item = AddItem.objects.create(
                Item_code=item_code,
                Item_name=item_name,
                qty=qty,
                Item_price=selling,
                item_cat=item_cat
            )
            message = 'New item added successfully!'

        # Now create a purchase record (a new entry)
        purchase = Purchase.objects.create(
            qty=qty,
            Item_name=item_name,
            Item_price=item_price,
            date=con_date,
            Item_code=item_code,
            item_cat=item_cat
        )

        return render(request, 'purchaseUser.html', {'msg': message})

    return render(request, 'purchaseUser.html')


def purchaseListUser(request):
    # Fetch all items from AddItem
    userdata = Purchase.objects.all()
    # Fetch all purchases from Purchase
    userdata1 = AddItem.objects.all()

    grand_total = 0
    userdata_with_totals = []

    for item in userdata:
        # Filter the Purchase table to get the matching qty based on Item_code
        matching_item = userdata1.filter(Item_code=item.Item_code).first()  # Get the first match

        # Get the qty from the matching Purchase, or default to 0 if no match is found
        item_qty = matching_item.qty if matching_item else 0

        # Calculate item total
        item_total = item.qty * item.Item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': item.id,
            'date': item.date,
            'Item_code': item.Item_code,
            'Item_name': item.Item_name,
            'item_cat': item.item_cat,
            'qty': item.qty,
            'item_qty': item_qty,  # Qty from Purchase model
            'Item_price': item.Item_price,
            'item_total': item_total  # Add item total
        })

    return render(request, 'purchaseListUser.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total,
        'userdata1': userdata1
    })


def purchaseUpdateUser(request):
    # Fetch all items from AddItem, excluding item_cat='food'
    userdata = AddItem.objects.exclude(item_cat='food')

    # Fetch all purchases from Purchase
    userdata1 = Purchase.objects.all()

    grand_total = 0
    userdata_with_totals = []

    for item in userdata:
        # Filter the Purchase table to get the matching purchase based on Item_code
        matching_purchase = userdata1.filter(Item_code=item.Item_code).first()  # Get the first match

        # If no matching purchase is found, skip the item
        if not matching_purchase:
            continue

        # Get the purchase quantity from the matching Purchase, or default to 0 if no match is found
        purchase_qty = matching_purchase.qty if matching_purchase else 0

        # Fetch the Item_price from the Purchase table (assuming Purchase has this field)
        item_price = matching_purchase.Item_price if matching_purchase else 0

        # Calculate item total using the Item_price from the Purchase table
        item_total = purchase_qty * item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': item.id,
            'Item_code': item.Item_code,
            'item_cat': item.item_cat,
            'Item_name': item.Item_name,
            'qty': item.qty,
            'purchase_qty': purchase_qty,  # Qty from Purchase model
            'Item_price': item_price,  # Item_price from Purchase model
            'item_total': item_total  # Add item total
        })

    return render(request, 'purchaseUpdateUser.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total  # Grand total based on Purchase data
    })





def updatestockUser(request, pk):
    # Fetch the existing item details
    rdata = get_object_or_404(AddItem, id=pk)

    if request.method == "POST":
        now = datetime.now()
        con_date = now.strftime("%Y-%m-%d")

        # Retrieve data from the POST request
        item_code = request.POST.get('t1')
        item_name = request.POST.get('t2')
        new_qty = int(request.POST.get('t5'))  # New quantity to be added
        item_price = request.POST.get('t4')
        selling = request.POST.get('selling')

        # Add the new quantity to the existing quantity
        updated_qty = rdata.qty + new_qty

        # Update the AddItem record
        AddItem.objects.filter(id=pk).update(
            Item_code=item_code,
            Item_name=item_name,
            qty=updated_qty,
            Item_price=selling,
        )

        # Record the purchase in the Purchase table
        Purchase.objects.create(
            qty=new_qty,  # Save only the newly added quantity
            Item_name=item_name,
            Item_price=item_price,
            date=con_date,
            Item_code=item_code,
            item_cat=rdata.item_cat,  # Fetch and save item_cat
        )

        # Redirect to the view item page
        base_url = reverse('purchaseUpdateUser')
        return redirect(base_url)

    return render(request, 'updatestockUser.html', {'rdata': rdata})



def deleteTable(request):
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'delete_table.html', {'tableName': tableName})


def delete_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')

        # Step 1: Get the bill_no from ItemOrder for the given table
        item_order = ItemOrder.objects.filter(table_name=table_name)
        if item_order.exists():
            bill_no = item_order.first().bill_no

            # Step 2: Delete related records in the Order table
            Orders.objects.filter(bill_no=bill_no).delete()

            # Step 3: Delete all entries from the ItemOrder table for the given table
            item_order.delete()

            return JsonResponse({'success': True, 'message': 'Table and associated data deleted successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Table not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=405)


def staffdeleteTable(request):
    tableName = ItemOrder.objects.values('table_name').distinct()
    return render(request, 'staffdelete.html', {'tableName': tableName})


def staffdelete_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')

        # Step 1: Get the bill_no from ItemOrder for the given table
        item_order = ItemOrder.objects.filter(table_name=table_name)
        if item_order.exists():
            bill_no = item_order.first().bill_no

            # Step 2: Delete related records in the Order table
            Orders.objects.filter(bill_no=bill_no).delete()

            # Step 3: Delete all entries from the ItemOrder table for the given table
            item_order.delete()

            return JsonResponse({'success': True, 'message': 'Table and associated data deleted successfully'}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Table not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=405)


def delete_table_record(request, pk):
    table = get_object_or_404(AddTable, pk=pk)
    table.delete()
    return redirect('view_table')


from django.db.models import Q


def itempurchaseReport(request):
    category = AddItem.objects.values('item_cat').distinct()

    # Initialize filters and data
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    selected_category = request.GET.get('selectedcat')

    # Fetch all purchases and items
    purchases = Purchase.objects.all()
    items = AddItem.objects.all()

    # Apply filters if provided
    if from_date:
        purchases = purchases.filter(date__gte=from_date)
    if to_date:
        purchases = purchases.filter(date__lte=to_date)
    if selected_category:
        purchases = purchases.filter(item_cat=selected_category)

    grand_total = 0
    userdata_with_totals = []

    for purchase in purchases:
        # Filter the AddItem table to get the matching qty based on Item_code
        matching_item = items.filter(Item_code=purchase.Item_code).first()  # Get the first match

        # Get the qty from the matching AddItem, or default to 0 if no match is found
        item_qty = matching_item.qty if matching_item else 0

        # Calculate item total
        item_total = purchase.qty * purchase.Item_price
        grand_total += item_total

        # Append details to the list
        userdata_with_totals.append({
            'id': purchase.id,
            'date': purchase.date,
            'Item_code': purchase.Item_code,
            'Item_name': purchase.Item_name,
            'item_cat': purchase.item_cat,
            'qty': purchase.qty,
            'item_qty': item_qty,  # Qty from AddItem model
            'Item_price': purchase.Item_price,
            'item_total': item_total  # Add item total
        })

    # Fetch unique categories for the dropdown
    categories = AddItem.objects.values_list('item_cat', flat=True).distinct()

    return render(request, 'itempurchaseReport.html', {
        'userdata': userdata_with_totals,
        'grand_total': grand_total,
        'categories': categories,  # Pass categories to the template
        'from_date': from_date,  # To prepopulate the date filters
        'to_date': to_date,
        'selected_category': selected_category,  # To prepopulate the category filter
        'category': category
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def update_qty(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_qty = data.get('qty')

        try:
            # Fetch the ItemOrder entry
            item = ItemOrder.objects.get(id=item_id)

            # Calculate the new tax amount (Price * Qty)
            new_tax_amt = item.price * new_qty

            # Update the quantity and tax amount in ItemOrder table
            item.qty = new_qty
            item.tax_amt = round(new_tax_amt, 2)
            item.save()

            # Update corresponding Orders record if it exists
            order = Orders.objects.filter(bill_no=item.bill_no, item_name=item.item_name).first()
            if order:
                order.qty = new_qty
                order.tax_amt = round(new_tax_amt, 2)
                order.save()

            return JsonResponse({'success': True, 'new_tax_amt': round(new_tax_amt, 2)})
        except ItemOrder.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# View for listing, searching, editing, and deleting bills
from django.db.models import Sum

def pending_bills_view(request):
    table = AddTable.objects.all()
    query = request.GET.get('q')  # Get the search query

    if query:
        bills = pendingBill.objects.filter(
            billNo__icontains=query
        ) | pendingBill.objects.filter(
            name__icontains=query
        ) | pendingBill.objects.filter(
            table__icontains=query
        ) | pendingBill.objects.filter(
            status__icontains=query
        ) | pendingBill.objects.filter(
            amount__icontains=query
        ) | pendingBill.objects.filter(
            phone__icontains=query
        ) | pendingBill.objects.filter(
            date__icontains=query
        )
    else:
        bills = pendingBill.objects.all()

    # Calculate the grand total of the amount field
    grand_total = bills.aggregate(Sum('amount'))['amount__sum'] or 0

    # Add new bill
    if request.method == 'POST':

        con_date = request.POST.get('date')
        bill_no = request.POST.get('billNo')
        name = request.POST.get('name')
        phone = request.POST.get('phone') or None
        table = request.POST.get('table')
        status = request.POST.get('status')
        amount = request.POST.get('amount')

        pendingBill.objects.create(
            billNo=bill_no,
            name=name,
            phone=phone,
            table=table,
            status=status,
            date=con_date,
            amount=amount
        )
        return redirect('pending_bills')

    return render(request, 'pending_bills.html', {'bills': bills, 'table': table, 'grand_total': grand_total})


# Edit bill
def edit_bill(request, pk):
    bill = get_object_or_404(pendingBill, pk=pk)
    if request.method == 'POST':
        bill.billNo = request.POST.get('billNo')
        bill.name = request.POST.get('name')
        bill.phone = request.POST.get('phone')
        bill.table = request.POST.get('table')
        bill.status = request.POST.get('status')
        bill.amount = request.POST.get('amount')
        bill.save()
        return redirect('pending_bills')

    return render(request, 'edit_bill.html', {'bill': bill})


# Delete bill
def delete_bill(request, pk):
    bill = get_object_or_404(pendingBill, pk=pk)
    bill.delete()
    return redirect('pending_bills')

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import AddTable # Replace with your actual model name

#room booking

#admin register

def adminregister(request):
    return render(request,'adminregister.html')

def adminlogin(request):
    return render(request,'adminlogin.html')


from .models import admin_register

def admin_reg(request):
    if request.method == "POST":
        admin_name = request.POST.get('adminname')
        mobile_number= request.POST.get('number')
        admin_id = request.POST.get('adminid')
        password = request.POST.get('password')

        add_trip=admin_register(
            admin_name=admin_name,
            mobile_number=mobile_number,
            admin_id=admin_id,
            password=password
        )
        add_trip.save()
        return redirect('adminlogin')
    return redirect('adminregister')

# LOGIN
from.models import admin_register

def admin_login(request):
    if request.method != "POST":
        return redirect('adminlogin')
    admin_name = request.POST.get('adminname', '').strip()
    password = request.POST.get('password', '')

    admin=admin_register.objects.filter(admin_name=admin_name,password=password).first()

    if admin:
        request.session['adminname']=admin.admin_name
        return render(request,'admin_home.html')
    else:
        return HttpResponse('invalid username or password')

def admins(request):
    products=admin_register.objects.all()
    return render(request,'admins.html',{'products':products})

def delete_admins(request,id):
    admins= get_object_or_404(admin_register,id=id)
    admins.delete()
    return redirect('admins')

def edit_admin(request,id):
    admin = get_object_or_404(admin_register, id=id)
    if request.method == "POST":
        admin_name = request.POST.get('adminname')
        mobile_number = request.POST.get('number')
        admin_id=request.POST.get('number')
        password = request.POST.get('password')

        # Update the Items object
        admin.admin_name = admin_name
        admin.mobile_number = mobile_number
        admin.admin_id=admin_id
        admin.password = password
        admin.save()
        # Redirect to a different URL after a successful update
        return redirect('admins')
    return render(request, 'edit_admin.html', {'admin': admin})

#user register

def userlogin(request):
    return render(request,'userlogin.html')

def userregister(request):
    return render(request,'userregister.html')

def user_reg(request):
    if request.method != "POST":
        return redirect('userregister')
    user_name = request.POST.get('username', '').strip()
    mobil_number = request.POST.get('number', '').strip()
    password = request.POST.get('password', '')

    add_trip=user_register(
        user_name=user_name,
        mobil_number=mobil_number,
        password=password,
    )
    add_trip.save()
    return redirect('userlogin')

#LOGIN
from.models import user_register

def user_login(request):
    if request.method != "POST":
        return redirect('userlogin')
    user_name = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    user=user_register.objects.filter(user_name=user_name,password=password).first()

    if user:
        request.session['username']=user.user_name
        return redirect('userHome')
    else:
        return HttpResponse('invalid username or password')

def users(request):
    products=user_register.objects.all()
    return render(request,'users.html',{'products':products})

def delete_users(request, id):
    users = get_object_or_404(user_register, id=id)
    users.delete()
    return redirect('users')

def edit_user(request,id):
    user = get_object_or_404(user_register, id=id)
    if request.method == "POST":
        user_name = request.POST.get('username')
        mobil_number = request.POST.get('number')
        password = request.POST.get('password')

        # Update the Items object
        user.user_name = user_name
        user.mobil_number = mobil_number
        user.password = password
        user.save()
        # Redirect to a different URL after a successful update
        return redirect('users')
    return render(request, 'edit_user.html', {'user': user})


def index2(request):
    return render(request,'index2.html')

def bookregister(request):
    return render(request,'bookregister.html')

# views.py
from django.shortcuts import render, redirect
from .models import BookRegister

def bookregister_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        # Save to database
        BookRegister.objects.create(name=name, mobile=mobile, password=password)

        return redirect('booklogin')  # Redirect after successful insert

    return render(request, 'booklogin.html')


def bookregister_list(request):
    records = BookRegister.objects.all()
    return render(request, 'bookregister_list.html', {'records': records})

def bookregister_edit(request, pk):
    record = get_object_or_404(BookRegister, pk=pk)
    if request.method == 'POST':
        record.name = request.POST.get('name')
        record.mobile = request.POST.get('mobile')
        record.password = request.POST.get('password')
        record.save()
        return redirect('bookregister_list')
    return render(request, 'bookregister_edit.html', {'record': record})

def bookregister_delete(request, pk):
    record = get_object_or_404(BookRegister, pk=pk)
    record.delete()
    return redirect('bookregister_list')

def booklogin(request):
    return render(request,'booklogin.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user_register  # Use your actual model name

def book_login(request):
    if request.method != "POST":
        return redirect('booklogin')

    name = request.POST.get('name', '').strip()
    password = request.POST.get('password', '')
    user = BookRegister.objects.filter(name=name, password=password).first()

    if user:
        request.session['name']=user.name
        return render(request,'room_register.html')
    else:
        return HttpResponse('invalid username or password')

#room booking

from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomBooking

def register_room(request):
    if request.method == "POST":
        check_in = parse_date(request.POST.get('check_in', ''))
        check_out = parse_date(request.POST.get('check_out', ''))
        if not check_in or not check_out or check_out <= check_in:
            return render(request, 'room_register.html', {
                'error': 'Check-out date must be after the check-in date.',
                'form_data': request.POST,
            })
        RoomBooking.objects.create(
            first_name=request.POST.get('first_name', '').strip(),
            last_name=request.POST.get('last_name', '').strip(),
            email=request.POST.get('email', '').strip(),
            mobile_number=request.POST.get('mobile_number', '').strip(),
            check_in=check_in,
            check_out=check_out,
            room_type=request.POST.get('room_type'),
            category=request.POST.get('category'),
        )
        return redirect('booking_success')
    return render(request, 'room_register.html')


def room_list(request):
    bookings = RoomBooking.objects.all()
    return render(request, 'room_list.html', {'bookings': bookings})


def delete_booking(request, pk):
    booking = get_object_or_404(RoomBooking, pk=pk)
    booking.delete()
    return redirect('room_list')


def edit_booking(request, pk):
    booking = get_object_or_404(RoomBooking, pk=pk)
    if request.method == 'POST':
        booking.first_name = request.POST['first_name']
        booking.last_name = request.POST['last_name']
        booking.email = request.POST['email']
        booking.mobile_number = request.POST['mobile_number']
        check_in = parse_date(request.POST.get('check_in', ''))
        check_out = parse_date(request.POST.get('check_out', ''))
        if not check_in or not check_out or check_out <= check_in:
            return render(request, 'room_edit.html', {
                'booking': booking,
                'error': 'Check-out date must be after the check-in date.',
            })
        booking.check_in = check_in
        booking.check_out = check_out
        booking.room_type = request.POST['room_type']
        booking.category = request.POST['category']
        booking.save()
        return redirect('room_list')
    return render(request, 'room_edit.html', {'booking': booking})

def room_register(request):
    return render(request,'room_register.html')

def booking_success(request):
    return render(request,'booking_success.html')

# add room and view

def addroom(request):
    return render(request,'addroom.html')

from .models import add_room

def admin_room(request):
    if request.method == "POST":
        room_no= request.POST.get('roomno')
        catagory = request.POST.get('category')
        type= request.POST.get('category1')

        add_trip = add_room(
            room_no=room_no,
            catagory=catagory,
            type=type
        )
        add_trip.save()
        return redirect('room')
    return redirect('addroom')

def room(request):
    products=add_room.objects.all()
    return render(request,'room.html',{'products':products})

def delete_inventory_room(request, id):
    room= get_object_or_404(add_room,id=id)
    room.delete()
    return redirect('room')

def edit_inventory_room(request, id):
    room = get_object_or_404(add_room, id=id)
    if request.method == "POST":
        room_no = request.POST.get('roomno')
        catagory= request.POST.get('category')
        type = request.POST.get ('category1')
        # Update the Items object
        room.room_no=room_no
        room.catagory=catagory
        room.type=type
        room.save()
        return redirect('room')
    return render(request,'edit_room.html',{'room':room})


