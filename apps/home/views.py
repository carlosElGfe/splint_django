# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import io
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
import numpy as np
from matplotlib import pyplot
from stl import mesh
from django.core.files import File
from .models import Splint, User
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import proj3d
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import time
import os
import subprocess
def latest_splint():
    figure = Figure()
    axes = mplot3d.Axes3D(figure)
    count = Splint.objects.all().count()
    splint = Splint.objects.all()[count-1]  
    your_mesh = mesh.Mesh.from_file(splint.splint_file.path)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)
    output = io.BytesIO()
    canvas = FigureCanvas(figure)
    canvas.print_png(output)
    img_str = base64.b64encode(output.getvalue())
    data_url = 'data:image/jpg;base64,' + base64.b64encode(output.getvalue()).decode()
    return data_url
    
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['total_users'] = User.objects.all().count()
    context['total_splints'] = Splint.objects.all().count()
    context['image']=latest_splint()
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def new_splint(request):
    context = {'segment':'icons'}
    scale_factor_x = float(request.POST.get("input1"))/ 100
    scale_factor_y = float(request.POST.get("input2"))/ 100

    # Load the STL file into a mesh object
    your_mesh = mesh.Mesh.from_file('/home/ubuntu/django/myproject/ferula.stl')
    print("-----")

    print(np.meshgrid(your_mesh))
    limit = 3
    cont = 0
    #scale the mesh
    for v in your_mesh.vectors:
        print(str(v))
        v[0][0] = v[0][0] * scale_factor_x
        v[1][0] = v[1][0] * scale_factor_x
        v[2][0] = v[2][0] * scale_factor_x
        v[0][1] = v[0][1] * scale_factor_y
        v[1][1] = v[1][1] * scale_factor_y
        v[2][1] = v[2][1] * scale_factor_y
        #print(str(v))

    print("-----")

    print(np.meshgrid(your_mesh))
    your_mesh.save('/home/ubuntu/django/myproject/apps/home/media/splints/new_ferula_' + str(Splint.objects.all().count()) +'.stl')
    counts_splints = Splint.objects.all().count()
    Splint.objects.create(
        id_splint = str(counts_splints) + request.user.username,
        splint_file = '/home/ubuntu/django/myproject/apps/home/media/splints/new_ferula_' + str(Splint.objects.all().count()) +'.stl',
        id_user = request.user
    )
    context['splint_code'] = str(counts_splints) + request.user.username
    context['msg'] = "your splint was created successfully and the code to search it will be: "+str(counts_splints) + request.user.username 
    figure = Figure()
    axes = mplot3d.Axes3D(figure)
    splint = Splint.objects.filter(id_splint = str(counts_splints) + request.user.username).first()         
    print("this is the file of the mesh" + str(splint.splint_file.path))
    your_mesh = mesh.Mesh.from_file(splint.splint_file.path)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    
    axes.auto_scale_xyz(scale, scale, scale)
    #axis.plot(axes)
    output = io.BytesIO()
    canvas = FigureCanvas(figure)
    canvas.print_png(output)
    img_str = base64.b64encode(output.getvalue())
    data_url = 'data:image/jpg;base64,' + base64.b64encode(output.getvalue()).decode()
    context['image'] = data_url
    return render(request, "home/splint_creator.html", context)
    

def visualize(request,code):
    input_splint_code = code
    splint = Splint.objects.filter(id_splint = input_splint_code).first()
    if splint:
        print("fund a matching splint")
        figure = Figure()
        axes = mplot3d.Axes3D(figure)         
        your_mesh = mesh.Mesh.from_file(splint.splint_file.path)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors * 1))
        # Auto scale to the mesh size
        scale = your_mesh.points.flatten()
        
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        print(np.meshgrid(your_mesh))
        print("-----")
        #axis.plot(axes)
        output = io.BytesIO()
        canvas = FigureCanvas(figure)
        canvas.print_png(output)
        img_str = base64.b64encode(output.getvalue())
        data_url = 'data:image/jpg;base64,' + base64.b64encode(output.getvalue()).decode()
        return render(request, "home/icons.html", {'image': data_url })
    return render(request,'home/icons.html',{})

def search_splint(request):
    input_splint_code = request.GET.get("input_splint_code")
    splint = Splint.objects.filter(id_splint = input_splint_code).first()
    if splint:
        print("fund a matching splint")
    return render(request,'home/icons.html',{})

def data_base(request):
    #create_gcode()
    if request.method == "GET":        
        splints = Splint.objects.all()
        context = {}
        context['splints'] = splints
        return render(request,'home/tables.html',context)

def create_gcode():
    result = subprocess.run(['cd mandoline-py','ls'], stdout=subprocess.PIPE)
    print(result)
    result.stdout
    '''os.system("cd /etc/mandoline-py/test-models")
    os.system("cd ..")'''

def down_stl(request,code):
    try:
        splint = Splint.objects.filter(id_splint=code).first()
    finally:
        return 0
        

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
