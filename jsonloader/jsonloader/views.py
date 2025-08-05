import json
from datetime import datetime
from django.shortcuts import render
from .forms import UploadJsonForm
from .models import JsonItem

def main(request):
    return render(request, "main.html")

def upload_json(request):
    errors = []
    json_items = []
    uploaded = False

    if request.method == 'POST':
        form = UploadJsonForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['file']
            
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                errors.append("Invalid JSON")
                return render(request, 'load_file.html', {'form': form,'errors': errors,'uploaded': uploaded})

            if not isinstance(data, list):
                errors.append("JSON must be a list")
                return render(request, 'load_file.html', {'form': form,'errors': errors,'uploaded': uploaded})


            for i, item in enumerate(data):
                name = item.get("name")
                raw_date = item.get("date")

                if name is None or raw_date is None:
                    errors.append(f"Missing field in {i+1} element")
                    continue

                if len(name) >= 50:
                    errors.append(f"Name is too long in {i+1} element")
                    
                try:
                    date = datetime.strptime(raw_date, '%Y-%m-%d_%H:%M')
                except ValueError:
                    errors.append(f"Invalid date format in {i+1} element")
                    

                json_items.append(JsonItem(name=name, date=date))

            if not errors:
                JsonItem.objects.bulk_create(json_items)
                uploaded = True

    else:
        form = UploadJsonForm()

    return render(request, 'load_file.html', {
        'form': form,
        'errors': errors,
        'uploaded': uploaded
    })

def view_items(request):
    return render(request, "items.html", {"items": JsonItem.objects.all()})