from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django_tables2 import SingleTableMixin
from supermarket.forms import * 
from supermarket.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from django_tables2.views import SingleTableMixin, SingleTableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from supermarket.filters import *
from django.db.models import Count
from django.shortcuts import get_object_or_404

def home_page(request): 
  return render(request, 'supermarket/home_page.html')

def items_home(request):
  return render(request, 'item/items_home.html')

# Items
class ItemListView(SingleTableMixin, FilterView):
  form_class = ItemInfoForm
  model = Item
  template_name = "item/view_items.html"
  filterset_class = OrderFilter

@login_required
def data_analytics(request):
  context = {}
  form = DataAnalyticsForm(request.POST)
  context.update({'form': form})
  if request.method == "POST":
    """Calculate Total Quantity as total_count"""
    instanceName_html = request.POST.get("instanceName")
    name_to_present = Item.objects.filter(id = instanceName_html).values_list("itemName")
    context.update({"instanceName": name_to_present[0][0]})
    filtered_model = ItemInstance.objects.filter(instanceName = instanceName_html).values()
    inst_quantity = ItemInstance.objects.filter(instanceName = instanceName_html).values_list("quantity")
    if filtered_model.exists():
      range_value = filtered_model.count()
      total_count = 0
      for i in range(range_value):
        total_count += inst_quantity[i][0]
      
      """Calculate Availability Rate"""
      availability_filtered_model = ItemInstance.objects.filter(instanceName = instanceName_html, status__status = "AVAILABLE").values()
      availability_range_value = availability_filtered_model.count()
      availability_filtered_model_quantity = ItemInstance.objects.filter(instanceName = instanceName_html, status__status="AVAILABLE").values_list("quantity")
      availability_count = 0
      for i in range(availability_range_value):
        availability_count = availability_filtered_model_quantity[i][0]
      availability_rate = f"{availability_count}%"
      context.update({'availability_rate': availability_rate})

      """Calculate Availability Rate by Month"""
      month_html = request.POST.get("entry_date")[5:7]
      context.update({'entry_month': month_html})
      month_filtered_model = ItemInstance.objects.filter(instanceName = instanceName_html, entry_date__month = month_html).values()
      month_range = month_filtered_model.count()
      month_filtered_model_quantity = ItemInstance.objects.filter(instanceName = instanceName_html, entry_date__month = month_html).values_list('quantity')
      month_count = 0
      for i in range(month_range):
        month_count = month_filtered_model_quantity[i][0]
      month_rate = f"{month_count}%"
      context.update({'month_rate': month_rate})
      return render(request, "stock/data_analytics_result.html", context)
  return render(request, "stock/data_analytics.html", context)

"""@login_required
def add_items(request):
  form = ItemInfoForm(request.POST)
  if request.method=="POST":
    if form.is_valid():
      message = form.save(commit=False)
      message.save()
      return redirect('view_items')
  else:
    form = ItemInfoForm
  return render(request, 'item/add_items.html', {'form': form})"""

@login_required
def update_view(request, id):
  context = {}
  obj = get_object_or_404(Item, id=id)
  form = ItemInfoForm(request.POST or None, instance = obj)
  if form.is_valid() & ('update_item' in request.POST):
    form.save()
    return redirect("/items/view_items")
  elif form.is_valid() & ('delete_item' in request.POST):
    obj.delete()
    return redirect("/items/view_items")
  context["form"] = form
  return render(request, "item/update_view.html", context)

@login_required
def delete_items(request, itemName):
  context = {}
  obj = get_object_or_404(Item, itemName=itemName)
  if request.method == "POST":
    obj.delete()
    return redirect("/items/view_items")
  return render(request, "item/delete_items.html", context)

# Item Instance
class ItemInstanceView(SingleTableMixin, FilterView, LoginRequiredMixin):
  form_class = ItemInstanceForm
  model = ItemInstance
  def get_queryset(model):
    model = ItemInstance.objects.all().filter(status__status = "AVAILABLE")    
    return model
  template_name = "stock/stock_home.html"
  filterset_class = InstanceFilter

"""@login_required
def add_to_stock(request):
  form = ItemInstanceForm(request.POST)
  if request.method=="POST":
    if form.is_valid():
      message = form.save()
      message.save()
      return redirect('/item_instance')
  else:
    form = ItemInstanceForm
  return render(request, "stock/add_to_stock.html", {'form': form})"""
  
@login_required
def update_stock(request, id, status):
  context = {}
  obj = get_object_or_404(ItemInstance, instanceId=id, status__status=status)
  if status == "AVAILABLE":
    form = ItemInstanceForm(request.POST or None, instance = obj)
    if form.is_valid() & ('update_item' in request.POST):
      form.save()
      return redirect("/item_instance")
    elif form.is_valid() & ('delete_item' in request.POST):
      obj.delete()
      return redirect("/item_instance")
    context["form"] = form
    return render(request, "stock/update_stock.html", context)
  else:
    return redirect("/item_instance")

# Stock-taking Jobs

class StockTakingJobsView(LoginRequiredMixin, FilterView, SingleTableMixin):
  form_class = ItemInstanceForm
  def get_queryset(self):
    model = ItemInstance.objects.all().filter(user = self.request.user)
    return model
  template_name = "iteminstance/view_jobs.html"
  filterset_class = InstanceFilter

def delete_jobs(request, id, status):
  context = {}
  status_to_check = Status.objects.get(status = "AVAILABLE")
  obj = get_object_or_404(ItemInstance, instanceId=id, status__status=status, user = request.user)
  if status == "OUT OF STOCK":
    form = ItemInstanceForm(request.POST or None, instance = obj)
    check_value = ItemInstance.objects.filter(instanceId = id, status__status = status_to_check).exists()
    if form.is_valid() & ('return_item' in request.POST):
      if check_value:
        """If the item with status = AVAILABLE exists!! """
        existing_model = get_object_or_404(ItemInstance, instanceId = id, status__status = status_to_check, user = None)
        new_quantity = obj.quantity + existing_model.quantity
        existing_model.quantity = new_quantity
        existing_model.save()
        obj.delete()
        return redirect("/stock_taking")
      else:
        """If the item with status = AVAILABLE does not exist"""
        obj.user = None
        obj.status = status_to_check
        obj.save()
        return redirect("/stock_taking")
    elif form.is_valid() & ('delete_item' in request.POST):
      obj.delete()
      return redirect("/stock_taking")
    context["form"] = form
    return render(request, "stock/update_stock.html", context)

def create_jobs(request):
  quantity_html = int(request.POST.get('quantity', 1))
  name = request.POST.get('instanceName', '')
  model = ItemInstance
  number_of_instances = 0
  for i in range(model.objects.all().count()):
    obj = model.objects.annotate(Count('instanceName'))
    if obj[i] == name:
      number_of_instances += 1
  form = AddStockForm(request.POST or None)

  if request.method=='POST':
    model_to_count = ItemInstance.objects.filter(instanceName = name , status__status = "AVAILABLE").values()
    inst_quantity = []
    inst_quantity.append(ItemInstance.objects.filter(instanceName = name , status__status = "AVAILABLE").values_list('quantity'))
    """ Note that as status changes, the inst_quantity quertset changes"""
    range_value = ItemInstance.objects.filter(instanceName = name , status__status = "AVAILABLE").values().count()
    total_count = 0
    for i in range(range_value):
      total_count += inst_quantity[0][i][0]

    if type(total_count) != int:
      messages.error(request, "Not Enough Stock! Total Stock: 0")
      return render(request, 'iteminstance/create_jobs.html', {'form': form})

    """quantity_html --> from HTML / inst_quantity --> from django model / total_count --> sum of quantity"""
    if quantity_html <= total_count:
      original_status = Status.objects.get(status = "AVAILABLE")
      test_value = [quantity_html]
      for i in range(range_value):
        if i == 0:
          add_to_test_value = test_value[i]
        else:
          add_to_test_value = test_value[i] - inst_quantity[0][0][0]
        test_value.append(add_to_test_value - inst_quantity[0][0][0])
        if test_value[i] <= inst_quantity[0][0][0]:  
          if test_value[i] == inst_quantity[0][0][0]:
            id = model_to_count[0]["instanceId"]
            status_to_change = Status.objects.get(status = "OUT OF STOCK")
            obj = ItemInstance.objects.filter(instanceId = id, instanceName = name, status = original_status).update(status = status_to_change, user = request.user)
            return redirect("/stock_taking")

          elif test_value[i] > 0 and test_value[i] < inst_quantity[0][0][0] :
            """Variables to use..."""
            id = model_to_count[0]["instanceId"] 
            production_date_input = model_to_count[0]["production_date"]
            expiry_date_input = model_to_count[0]["expiry_date"]
            status_to_change = Status.objects.get(status = "OUT OF STOCK")
            quantity_new = inst_quantity[0][0][0] - test_value[i]
            
            obj = ItemInstance.objects.filter(instanceId = id, instanceName = name, status = original_status)
            obj.update(status = status_to_change, user = request.user, quantity = test_value[i])
            
            """--------------------------------------------------------------------------------------------------------------"""
            name = request.POST.get('instanceName')
            name_to_change = Item.objects.get(id = name)
            "How to put instanceName!!"
            new_obj = ItemInstance.objects.create(
              instanceName = name_to_change,
              instanceId = id,
              status = original_status,
              expiry_date = expiry_date_input,
              production_date = production_date_input,
              quantity = quantity_new
            )

            return redirect("/stock_taking")

          elif test_value[i] > inst_quantity[0][0][0]:
            """new model --> same instance, decreased quantity"""
            """existing model --> same instance, with out of stock / user"""
            id = model_to_count[0]["instanceId"]
            status_to_change = Status.objects.get(status = "OUT OF STOCK")
            obj = ItemInstance.objects.filter(instanceId = id, instanceName = name, status = original_status).update(status = status_to_change, user = request.user)
            
        else:
          """new model --> same instance, decreased quantity"""
          """existing model --> same instance, with out of stock / user"""
          id = model_to_count[i]["instanceId"]
          status_to_change = Status.objects.get(status = "OUT OF STOCK")
          obj = ItemInstance.objects.filter(instanceId = id, instanceName = name, status = original_status).update(status = status_to_change, user = request.user)
    else:
      messages.error(request, "Not Enough Stock! Total Stock: " f'{total_count}')
  return render(request, 'iteminstance/create_jobs.html', {'form': form})

# login / signup
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login = (request, new_user)
            messages.success(request, 'Your account is set up!')
            return redirect("login")
        else:
            return render(request, 'registration/adduser.html', {'form':form})
    else:
        form = UserForm()
        return render(request, 'registration/adduser.html', {'form':form})

@login_required
def view_personal_information(request):
  user = User.objects.filter(username = request.user.username)
  return render(request, "registration/view_account_information.html", {'user':user})

# Change Information
@login_required
def change_personal_information(request):
    if request.method == 'POST':
        user_change_form = UserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('confirm.html', request.user.username)
        else:
            messages.error(request, 'Try again')
    else:
        user_change_form = UserChangeForm(instance = request.user)
        messages.error(request, "Try again")
    return render(request, 'registration/change_personal_information.html', {'user_change_form':user_change_form})
  
@login_required
def change_password(request):
  if request.method == "POST":
    user = request.user
    origin_password = request.POST["origin_password"]
    if check_password(origin_password, user.password):
      new_password = request.POST["new_password"]
      confirm_password = request.POST["confirm_password"]
      if new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("login")
      else:
        messages.error(request, 'Password not same')
    else:
      messages.error(request, 'Password not correct')
    return render(request, 'registration/change_password.html')
  else:
    return render(request, 'registration/change_password.html')