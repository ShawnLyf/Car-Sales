from django.shortcuts import render
from django.views.generic import ListView
from .models import Post,Seller,Carmodel,PostTag,Tag
from .forms import FilterForm
from django.http import JsonResponse

# def home(request):
#     return render(request,'today/home.html')

# def list(request):
#     return render(request,'today/list.html')

def single(request,id):
    post = Post.objects.get(pk=id)
    user = Seller.objects.get(pk=post.seller_username)
    user.phones = user.phones
    phone = user.phones[0]
    random_posts = Post.objects.order_by('?')[:6]

    # modify the object
    if post.fueltype == "柴油":
        post.fueltype = "Diesel"
    else:
        post.fueltype = "Petrol"
    if post.is_auto == True:
        post.is_auto = "Automatic"
    else:
        post.is_auto = "Manual"
    if post.boughtyear == None:
        post.boughtyear = "Unknown"
    if post.carmodel.model == "other":
        post.carmodel.model = "Unknown"
    if "分钟" in post.updatetime:
        post.updatetime = post.updatetime.replace("分钟", " minutes")
    elif "小时" in post.updatetime:
        post.updatetime = post.updatetime.replace("小时", " hours")
    post.updatetime = post.updatetime.replace("前", " ago")
    print(post.id)
    tags = Tag.objects.filter(posttag__postid=post.id)
    
    
    return render(request,'today/detail.html',
        {
            "post":post,
            "user":user,
            "phone":phone,
            "tags":tags,
            "random_posts":random_posts
        })

class GridView(ListView):
    template_name = 'today/home.html'
    model = Post   
    context_object_name = 'posts'
    paginate_by = 8
    brands =[]
    locations=[]
    num_posts = 0 # num of poster after filtered

     
    
    def get_queryset(self):
        
        queryset = super(GridView, self).get_queryset()
        # Get the distinct brands from the queryset.
        brands = list(queryset.values_list('carmodel__brand', flat=True).distinct())
        # Use list comprehension to replace "other" with "Unknown".
        brands = ['Unknown' if brand == 'other' else brand for brand in brands]
        # Sort the brands, but keep "Unknown" at the end if it exists.
        brands = sorted([brand for brand in brands if brand != 'Unknown'])
        if 'Unknown' in brands:
            brands.append('Unknown')
        self.brands = brands

        locations = list(queryset.values_list('suburb', flat=True).distinct())
        self.locations = sorted(locations)

        # post filters 
        # transmission filter
        transmissions = self.request.GET.getlist('transmission')  # Get a list of selected transmissions
        if transmissions:
            # Mapping frontend values to database values
            transmission_mapping = {
                'Automatic': 't',
                'Manual': 'f'
            }
            db_transmission_values = [transmission_mapping.get(t) for t in transmissions if t in transmission_mapping]

            # Note: Assuming the column name in your model is 'is_auto' and it stores values like 't' and 'f'.
            queryset = queryset.filter(is_auto__in=db_transmission_values)


        # Fueltype filter
        fuel_types = self.request.GET.getlist('fueltype')  # Notice this is 'getlist', not 'get'
        if fuel_types:
            # Mapping frontend values to database values
            fueltype_mapping = {
                'Petrol': '汽油',
                'Diesel': '柴油',
                'Hybrid': '混合动力'
            }

            db_fuel_values = [fueltype_mapping.get(f) for f in fuel_types if f in fueltype_mapping]

            # Filtering using the __in filter
            queryset = queryset.filter(fueltype__in=db_fuel_values)

        # mileage range filter
        mileage_from = self.request.GET.get('mileage_from', None)
        mileage_to = self.request.GET.get('mileage_to', None)
        if mileage_from:
            queryset = queryset.filter(mileage__gte=mileage_from)
        if mileage_to:
            queryset = queryset.filter(mileage__lte=mileage_to)

        # mileage range filter
        price_from = self.request.GET.get('price_from', None)
        price_to = self.request.GET.get('price_to', None)
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)

        for post in queryset: 
            if post.carmodel.model == "other":
                post.carmodel.model = "Unknown"

        # Brand and model filter 
        brand = self.request.GET.get('brand', None)
        model = self.request.GET.get('cmodel', None)
        if brand:
            queryset = queryset.filter(carmodel__brand=brand)
        if model:
            queryset = queryset.filter(carmodel__model=model)

        # year filter
        fromYear = self.request.GET.get('fromyear', None)
        toYear = self.request.GET.get('toyear', None)
        if fromYear:
            queryset = queryset.filter(year__gte=fromYear)
        if toYear:
            queryset = queryset.filter(year__lte=toYear)
       

        # locations filter
        location = self.request.GET.get("location",None)
        print(location)
        if location:
            queryset = queryset.filter(suburb=location)


        
        
        for post in queryset:
            # modify transmission value
            if post.is_auto == True:
                post.is_auto = "Automatic"
            else:
                post.is_auto = "Manual"

            # modify fuel type value
            if post.fueltype == "柴油":
                post.fueltype = "Diesel"
            else:
                post.fueltype = "Petrol"

        # sorting       
        sort_by = self.request.GET.get('sort_by', None)
        print(sort_by)
        if sort_by == "newest":
            queryset = queryset.order_by('-createtime')
        elif sort_by == "most_views":
            queryset = queryset.order_by('-views')
        elif sort_by == "price_asc":
            queryset = queryset.order_by('price')
        elif sort_by == "price_desc":
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-createtime')

        self.num_posts = queryset.count()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # total_posts = Post.objects.all().count()
        context['total_posts'] = self.num_posts
        context['brands'] = self.brands
        context['locations']=self.locations
        context['years']=range(2023, 1899, -1)

        # retain the user filter after refresh 

        return context
    

def get_models_for_brand(request):
    brand = request.GET.get('brand')
    print(brand)
    if brand == "Unknown":
        brand = "other"
    # Get the distinct models for the selected brand.
    models = list(Post.objects.filter(carmodel__brand=brand).values_list('carmodel__model', flat=True).distinct())
    # Use list comprehension to replace "other" with "Unknown".
    models = ['Unknown' if model == 'other' else model for model in models]
    # Sort the models, but keep "Unknown" at the end if it exists.
    models_sorted = sorted([model for model in models if model != 'Unknown'])
    if 'Unknown' in models:
        models_sorted.append('Unknown')
    models = models_sorted

    return JsonResponse(list(models), safe=False)

